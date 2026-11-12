# -*- coding: utf-8 -*-
"""qgis_cli_server.py — QGIS Processing CLI 后端（stdio MCP，纯标准库）。

与现有 qgis in-app 桥分开：本后端只做 qgis_process 无头执行，不冒充
打开工程/图层视图能力。工具面仅 ping / discover / run_processing。
"""
import io
import json
import os
import re
import subprocess
import sys
import time

QGIS_BAT = os.environ.get(
    "GIS_QGIS_BAT",
    r"C:\Program Files\QGIS 3.44.15\bin\qgis_process-qgis-ltr.bat")
PROTOCOL_VERSION = "2024-11-05"
ALG_RE = re.compile(r"^[a-z0-9_]+:[a-z0-9_]+$")
BLOCKED = {"qgis:executesql", "gdal:executesql"}
_TOOLS = ["qgis_ping", "qgis_discover", "qgis_run_processing"]


def _fail(code, message, **extra):
    d = {"ok": False, "error_code": code, "message": message}
    d.update(extra)
    return d


def _run(args, timeout=240):
    if not os.path.exists(QGIS_BAT):
        return _fail("QGIS_NOT_FOUND", "找不到 qgis_process launcher：%s"
                     % QGIS_BAT)
    cmd = ["cmd", "/c", QGIS_BAT] + [str(a) for a in args]
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace",
                           timeout=timeout)
    except subprocess.TimeoutExpired:
        return _fail("QGIS_TIMEOUT", "qgis_process 超过 %ss" % timeout)
    except Exception as e:  # noqa: BLE001
        return _fail("QGIS_EXEC_ERROR", str(e))
    return {"ok": p.returncode == 0, "returncode": p.returncode,
            "stdout": p.stdout or "", "stderr": p.stderr or "",
            "duration_s": round(time.time() - t0, 2),
            "command": " ".join(cmd)}


def _param_text(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return ",".join(_param_text(v) for v in value)
    raise ValueError("参数值只支持标量/字符串列表：%r" % (value,))


def qgis_ping(args):
    r = _run(["--version"], timeout=120)
    if not r.get("ok"):
        return r
    first = (r["stdout"].strip().splitlines() or [""])[0]
    return {"ok": True, "version": first, "mode": "qgis_process-cli",
            "launcher": QGIS_BAT, "duration_s": r["duration_s"]}


def qgis_discover(args):
    r = _run(["--version"], timeout=120)
    if not r.get("ok"):
        return r
    lines = r["stdout"].strip().splitlines()
    return {"ok": True, "version": lines[0] if lines else "",
            "mode": "qgis_process-cli", "tools": _TOOLS,
            "note": "无头 Processing 通道；不提供打开工程/图层视图能力",
            "launcher": QGIS_BAT, "duration_s": r["duration_s"]}


def qgis_run_processing(args):
    alg = args.get("algorithm")
    params = args.get("params") or {}
    if not isinstance(alg, str) or not ALG_RE.match(alg):
        return _fail("INVALID_ARGUMENT", "algorithm 须为 provider:name 形式")
    if alg in BLOCKED:
        return _fail("DEFER_BLOCKED", "算法 %s 在硬拦截名单内" % alg)
    if not isinstance(params, dict):
        return _fail("INVALID_ARGUMENT", "params 必须是对象")
    out_param = params.get("OUTPUT") or params.get("output")
    if out_param and isinstance(out_param, str) and os.path.exists(out_param):
        return _fail("TARGET_EXISTS", "OUTPUT 已存在，拒绝覆盖：%s" % out_param)
    cli = ["run", alg, "--json", "--"]
    try:
        for k, v in params.items():
            if v is None:
                continue
            if not re.match(r"^[A-Za-z0-9_]+$", str(k)):
                return _fail("INVALID_ARGUMENT", "参数名不合法：%r" % (k,))
            cli.append("%s=%s" % (k, _param_text(v)))
    except ValueError as e:
        return _fail("INVALID_ARGUMENT", str(e))
    r = _run(cli)
    if not r.get("ok"):
        return _fail("QGIS_ERROR", (r.get("stderr") or r.get("stdout") or "")
                     .strip()[-2000:], returncode=r.get("returncode"),
                     command=r.get("command"))
    try:
        parsed = json.loads(r["stdout"])
    except Exception:
        parsed = None
    target = out_param if isinstance(out_param, str) else None
    if target and (not os.path.exists(target) or os.path.getsize(target) == 0):
        return _fail("QGIS_NO_OUTPUT", "算法返回 0 但 OUTPUT 未生成或为空",
                     target=target, stdout_tail=r["stdout"][-1200:])
    out = {"ok": True, "algorithm": alg, "target": target,
           "size_bytes": (os.path.getsize(target)
                          if target and os.path.exists(target) else None),
           "duration_s": r["duration_s"], "command": r["command"]}
    if isinstance(parsed, dict):
        out["results"] = parsed.get("results")
        out["algorithm_name"] = (parsed.get("algorithm_details") or {}).get(
            "name")
        if parsed.get("log"):
            out["log"] = parsed["log"]
    return out


_HANDLERS = {
    "qgis_ping": qgis_ping,
    "qgis_discover": qgis_discover,
    "qgis_run_processing": qgis_run_processing,
}


def _tool_defs():
    return [{"name": n, "description": "QGIS Processing CLI backend tool",
             "inputSchema": {"type": "object", "properties": {}}}
            for n in _TOOLS]


def handle(msg):
    method = msg.get("method")
    mid = msg.get("id")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "qgis-cli-bridge", "version": "0.1.0"}}}
    if method in ("notifications/initialized", "notifications/cancelled"):
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid,
                "result": {"tools": _tool_defs()}}
    if method == "tools/call":
        params = msg.get("params") or {}
        name = params.get("name") or ""
        args = params.get("arguments") or {}
        if name not in _HANDLERS:
            payload = _fail("UNKNOWN_TOOL", "qgis-cli 没有工具：%s" % name)
        else:
            try:
                payload = _HANDLERS[name](args)
            except Exception as e:  # noqa: BLE001
                payload = _fail("QGIS_EXEC_ERROR", "%s: %s" % (name, e))
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "content": [{"type": "text",
                         "text": json.dumps(payload, ensure_ascii=False)}],
            "isError": payload.get("ok") is False,
            "structuredContent": payload}}
    return {"jsonrpc": "2.0", "id": mid,
            "error": {"code": -32601,
                      "message": "method not found: %s" % method}}


def _lock_stdio_utf8():
    for name in ("stdout", "stdin"):
        stream = getattr(sys, name, None)
        buf = getattr(stream, "buffer", None)
        if buf is None or getattr(stream, "encoding", None) == "utf-8":
            continue
        try:
            setattr(sys, name, io.TextIOWrapper(
                buf, encoding="utf-8", errors="replace"))
        except Exception:  # noqa: BLE001
            pass


def main():
    _lock_stdio_utf8()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except Exception:
            continue
        resp = handle(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
