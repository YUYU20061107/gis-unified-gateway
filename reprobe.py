# -*- coding: utf-8 -*-
"""
reprobe.py — 能力账本复探与漂移降级（v0.4 补充修复单，2026-11-14）。

把 leaves-full.json 从一次性快照变成活账本：
  * 遍历 status=ok 的叶子（--include-unverified 时含 unverified），逐叶复探；
  * 逐叶三态：pass / fail（后端可达但登记能力已不在）/ unreachable
    （后端环境不可达——起不来、无应答、或后端自带 ping 报告其实机
    运行时缺失；与 fail 严格区分，不据此降级）；
  * fail 自动降级 unverified 并记 history；unreachable 只记录不降级，
    连续 3 次在报告里标 stale；升回 ok 只许复探 pass（且须显式
    --include-unverified 才探 unverified 叶子）；
  * 每叶 additive 字段 last_verified_at / last_probe_result / history[]，
    v0.3 消费者（build_mapping / selftest / gateway）读新账本不受影响；
  * 每次运行在 reports/ 落一份漂移报告（.json + .md）：总数、三态清单、
    stale、人工复探清单、与上次账本的逐叶 diff；
  * 退出码：有降级为 1，全过（无降级）为 0，参数/IO 错误为 2。

探针口径（不新造弱探针、不放行写探针）：
  * 服务器型叶子：复用 backends.json 登记的后端 MCP 服务本身——spawn 后
    做 initialize + tools/list，再调用后端自带的 *_ping 健康检查工具；
    登记 native 工具不在工具面内 = fail。复探只调用 tools/list 与
    *_ping，从不执行叶子工具本身，故无任何写副作用。
  * 通道类叶子（kind=gp_channel / processing_channel）：工具面校验之外，
    算法级实机执行属写操作，列入报告的「人工复探清单」，不自动执行。
  * registry 型叶子（V03/V04，native 为空）：能力由网关读注册表数据
    提供，复探即校验其数据源文件仍可解析、非空且动词仍在 verbs.json。
  * PostGIS 生产 DSN 未配置维持 deferred：其后端命令在本机无法启动时
    记 unreachable（证据注明 DSN/运行时未配置），不在本工具内解决。

用法：
  python3 reprobe.py [--ledger PATH] [--backends PATH] [--init]
                     [--include-unverified] [--backend NAME]
                     [--timeout SEC] [--reports-dir DIR] [--dry-run]
"""
import argparse
import copy
import datetime
import json
import os
import select
import subprocess
import sys

PROBE_VERSION = "reprobe-1.0+mcp-surface"
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.join(HERE, "code")
REGISTRY_SOURCES = {
    "qgis": "processing_registry.json",
    "qgis-cli": "processing_registry.json",
    "supermap": "processing_registry.json",
    "arcgis-pro": "gp_registry.json",
    "postgis": "postgis_templates.json",
}


def now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def leaf_key(leaf):
    return "%s|%s|%s|%s" % (leaf.get("vid"), leaf.get("verb"),
                            leaf.get("backend"), leaf.get("variant", ""))


# ---------------- 最小 MCP stdio 客户端（行式 JSON-RPC） ----------------

class McpSession(object):
    def __init__(self, cmd, timeout):
        self.timeout = timeout
        self.proc = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=True, encoding="utf-8",
            errors="replace", bufsize=1)
        self.buf = ""
        self.next_id = 0

    def close(self):
        try:
            self.proc.kill()
        except Exception:
            pass

    def _readline(self, deadline):
        while "\n" not in self.buf:
            remain = deadline - datetime.datetime.now().timestamp()
            if remain <= 0:
                raise TimeoutError("read timeout")
            r, _, _ = select.select([self.proc.stdout], [], [], remain)
            if not r:
                raise TimeoutError("read timeout")
            chunk = os.read(self.proc.stdout.fileno(), 65536)
            if not chunk:
                raise EOFError("backend closed stdout")
            self.buf += chunk.decode("utf-8", "replace")
        line, self.buf = self.buf.split("\n", 1)
        return line

    def request(self, method, params=None):
        self.next_id += 1
        rid = self.next_id
        msg = {"jsonrpc": "2.0", "id": rid, "method": method}
        if params is not None:
            msg["params"] = params
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()
        deadline = datetime.datetime.now().timestamp() + self.timeout
        while True:
            line = self._readline(deadline)
            try:
                obj = json.loads(line)
            except ValueError:
                continue  # 后端在 stdout 上的非协议输出，跳过
            if obj.get("id") == rid:
                if "error" in obj:
                    raise RuntimeError("rpc error: %s" % obj["error"])
                return obj.get("result")

    def notify(self, method):
        self.proc.stdin.write(json.dumps(
            {"jsonrpc": "2.0", "method": method}) + "\n")
        self.proc.stdin.flush()


def substitute(cmd, backends_cfg):
    root = backends_cfg.get("bridges_root", "")
    out = []
    for part in cmd:
        out.append(part.replace("{python}", sys.executable)
                       .replace("{here}", CODE)
                       .replace("{bridges}", os.path.expanduser(root))
                       .replace("{catalog}", os.path.join(HERE, "data-catalog")))
    return out


def probe_backend(name, backends_cfg, timeout):
    """返回 (state, tools, evidence)。state ∈ {"up","unreachable"}。"""
    spec = backends_cfg.get("backends", {}).get(name)
    if spec is None:
        return "unreachable", [], "backends.json 无此后端登记"
    cmd = substitute(spec["command"], backends_cfg)
    try:
        sess = McpSession(cmd, timeout)
    except Exception as e:  # noqa: BLE001 - 起不来即不可达
        return "unreachable", [], "后端进程启动失败：%r" % (e,)
    try:
        sess.request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "reprobe", "version": "1.0"}})
        sess.notify("notifications/initialized")
        result = sess.request("tools/list", {})
        tools = [t.get("name") for t in result.get("tools", [])]
        ping = None
        for t in tools:
            if t == "ping" or t.endswith("_ping"):
                ping = t
                break
        if ping is not None:
            res = sess.request("tools/call", {"name": ping, "arguments": {}})
            if res and res.get("isError"):
                return ("unreachable", tools,
                        "%s 报告运行时不可用（isError）" % ping)
            text = ""
            for c in (res or {}).get("content", []):
                if c.get("type") == "text":
                    text += c.get("text", "")
            payload = None
            try:
                payload = json.loads(text)
            except ValueError:
                payload = None
            if isinstance(payload, dict) and payload.get("ok") is False:
                return ("unreachable", tools,
                        "%s 报告运行时不可用：%s"
                        % (ping, payload.get("error_code")
                           or payload.get("message") or "ok=false"))
        return "up", tools, ""
    except Exception as e:  # noqa: BLE001 - 无应答/协议失败即不可达
        return "unreachable", [], "后端无应答：%r" % (e,)
    finally:
        sess.close()


def probe_registry_leaf(leaf):
    """registry 型叶子：校验网关据以提供能力的数据源。返回 (result, evidence)。"""
    src_name = REGISTRY_SOURCES.get(leaf.get("backend"))
    if src_name is None:
        return "fail", "无登记的注册表数据源"
    path = os.path.join(CODE, src_name)
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        nonempty = bool(data) and (
            len(data) > 0 if hasattr(data, "__len__") else True)
    except Exception as e:  # noqa: BLE001
        return "fail", "注册表数据源 %s 不可用：%r" % (src_name, e)
    try:
        with open(os.path.join(CODE, "verbs.json"), encoding="utf-8") as f:
            verbs = json.load(f)
        verb_known = leaf.get("verb") in json.dumps(verbs, ensure_ascii=False)
    except Exception:  # noqa: BLE001
        verb_known = False
    if nonempty and verb_known:
        return "pass", "数据源 %s 可解析且非空，动词在 verbs.json" % src_name
    return "fail", "数据源 %s 非空=%s，动词登记=%s" % (
        src_name, nonempty, verb_known)


# ---------------- 主流程 ----------------

def ensure_fields(leaf):
    leaf.setdefault("last_verified_at", None)
    leaf.setdefault("last_probe_result", None)
    leaf.setdefault("history", [])


def trailing_unreachable(leaf):
    n = 0
    for h in reversed(leaf.get("history", [])):
        if h.get("result") == "unreachable":
            n += 1
        else:
            break
    return n


def main(argv=None):
    ap = argparse.ArgumentParser(description="能力账本复探与漂移降级")
    ap.add_argument("--ledger", default=os.path.join(HERE, "leaves-full.json"))
    ap.add_argument("--backends", default=os.path.join(CODE, "backends.json"))
    ap.add_argument("--reports-dir", default=os.path.join(HERE, "reports"))
    ap.add_argument("--init", action="store_true",
                    help="只补 additive 字段并保存，不复探")
    ap.add_argument("--include-unverified", action="store_true",
                    help="同时复探 unverified 叶子（pass 可升回 ok）")
    ap.add_argument("--backend", default=None, help="只探指定后端")
    ap.add_argument("--timeout", type=float, default=25.0)
    ap.add_argument("--dry-run", action="store_true",
                    help="复探并出报告，但不回写账本")
    args = ap.parse_args(argv)

    try:
        with open(args.ledger, encoding="utf-8") as f:
            ledger = json.load(f)
        with open(args.backends, encoding="utf-8") as f:
            backends_cfg = json.load(f)
    except Exception as e:  # noqa: BLE001
        print("ERROR 读账本/后端配置失败：%r" % (e,))
        return 2

    before = copy.deepcopy(ledger)
    for leaf in ledger:
        ensure_fields(leaf)

    if args.init:
        if not args.dry_run:
            with open(args.ledger, "w", encoding="utf-8", newline="\n") as f:
                json.dump(ledger, f, ensure_ascii=False, indent=1)
        print("init 完成：%d 叶已补 last_verified_at/last_probe_result/history"
              % len(ledger))
        return 0

    targets = []
    for leaf in ledger:
        if args.backend and leaf.get("backend") != args.backend:
            continue
        if leaf.get("status") == "ok":
            targets.append(leaf)
        elif leaf.get("status") == "unverified" and args.include_unverified:
            targets.append(leaf)

    # 按后端分组探活（每后端只 spawn 一次）
    backend_state = {}
    server_targets = [l for l in targets if l.get("kind") != "registry"]
    for name in sorted(set(l["backend"] for l in server_targets)):
        state, tools, evidence = probe_backend(name, backends_cfg, args.timeout)
        backend_state[name] = (state, tools, evidence)
        print("backend %-12s %s（tools=%d）%s"
              % (name, state, len(tools), (" :: " + evidence) if evidence else ""))

    stamp = now_iso()
    results = {"pass": [], "fail": [], "unreachable": []}
    demotions, promotions, stale = [], [], []
    manual = []
    for leaf in targets:
        key = leaf_key(leaf)
        if leaf.get("kind") in ("gp_channel", "processing_channel"):
            manual.append(key)
        if leaf.get("kind") == "registry":
            result, evidence = probe_registry_leaf(leaf)
        else:
            state, tools, bev = backend_state[leaf["backend"]]
            if state == "unreachable":
                result, evidence = "unreachable", bev
            elif leaf.get("native") in tools:
                result, evidence = "pass", "工具面含 %s（%d 工具）" % (
                    leaf.get("native"), len(tools))
            else:
                result, evidence = "fail", "后端可达但工具面已无 %s（现 %d 工具）" % (
                    leaf.get("native"), len(tools))
        old_status = leaf.get("status")
        leaf["last_verified_at"] = stamp
        leaf["last_probe_result"] = result
        leaf["history"].append({
            "at": stamp, "probe": PROBE_VERSION,
            "result": result, "evidence": evidence})
        if result == "fail" and old_status == "ok":
            leaf["status"] = "unverified"
            demotions.append(key)
        elif result == "pass" and old_status == "unverified":
            leaf["status"] = "ok"
            promotions.append(key)
        if trailing_unreachable(leaf) >= 3:
            stale.append(key)
        results[result].append(key)
        print("%-12s %s -> %s%s" % (result.upper(), key, leaf["status"],
                                    "（降级）" if key in demotions else
                                    "（升回）" if key in promotions else ""))

    # 漂移 diff：与运行前账本逐叶对比
    diff = []
    for old, new in zip(before, ledger):
        if old.get("status") != new.get("status"):
            diff.append({"leaf": leaf_key(new), "field": "status",
                         "from": old.get("status"), "to": new.get("status")})
    field_only = sum(1 for old, new in zip(before, ledger)
                     if old != new and old.get("status") == new.get("status"))

    os.makedirs(args.reports_dir, exist_ok=True)
    _now = datetime.datetime.now()
    ts = _now.strftime("%Y%m%d-%H%M%S") + "-%03d" % (_now.microsecond // 1000)
    record = {
        "at": stamp, "probe": PROBE_VERSION, "ledger": args.ledger,
        "targets": len(targets),
        "counts": {k: len(v) for k, v in results.items()},
        "pass": results["pass"], "fail": results["fail"],
        "unreachable": results["unreachable"],
        "demotions": demotions, "promotions": promotions,
        "stale": stale, "manual_reprobe": manual,
        "status_diff": diff,
        "field_only_updates": field_only,
        "backends": {k: {"state": v[0], "tools": len(v[1]), "evidence": v[2]}
                     for k, v in backend_state.items()},
    }
    with open(os.path.join(args.reports_dir, "reprobe-%s.json" % ts),
              "w", encoding="utf-8", newline="\n") as f:
        json.dump(record, f, ensure_ascii=False, indent=1)
    lines = [
        "# 复探漂移报告 %s" % stamp, "",
        "探针：%s；目标叶子 %d（ok%s）；pass %d / fail %d / unreachable %d。"
        % (PROBE_VERSION, len(targets),
           "＋unverified" if args.include_unverified else "",
           len(results["pass"]), len(results["fail"]),
           len(results["unreachable"])), "",
        "## 降级（fail → unverified）", "",
    ]
    lines += ["- %s" % k for k in demotions] or ["（无）"]
    lines += ["", "## 升回（unverified → ok）", ""]
    lines += ["- %s" % k for k in promotions] or ["（无）"]
    lines += ["", "## fail 清单", ""]
    lines += ["- %s" % k for k in results["fail"]] or ["（无）"]
    lines += ["", "## unreachable 清单（只记录、不降级）", ""]
    lines += ["- %s" % k for k in results["unreachable"]] or ["（无）"]
    lines += ["", "## stale（连续 ≥3 次 unreachable）", ""]
    lines += ["- %s" % k for k in stale] or ["（无）"]
    lines += ["", "## 人工复探清单（通道类：仅工具面校验，算法级实机需人工）", ""]
    lines += ["- %s" % k for k in manual] or ["（无）"]
    lines += ["", "## 状态 diff", ""]
    lines += ["- %s：%s → %s" % (d["leaf"], d["from"], d["to"])
              for d in diff] or ["（无状态变化）"]
    lines += ["", "仅字段更新（时间戳/最近结果/history）的叶子：%d" % field_only]
    with open(os.path.join(args.reports_dir, "reprobe-%s.md" % ts),
              "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    if not args.dry_run:
        with open(args.ledger, "w", encoding="utf-8", newline="\n") as f:
            json.dump(ledger, f, ensure_ascii=False, indent=1)

    print("复探完成：pass %d / fail %d / unreachable %d；降级 %d，升回 %d；"
          "报告 reports/reprobe-%s.{json,md}"
          % (len(results["pass"]), len(results["fail"]),
             len(results["unreachable"]), len(demotions), len(promotions), ts))
    return 1 if demotions else 0


if __name__ == "__main__":
    sys.exit(main())
