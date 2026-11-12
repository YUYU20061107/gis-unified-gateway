# gis-unified-gateway

**One verb contract, many GIS engines.**

A unified gateway that lets AI agents (or any client) operate heterogeneous GIS backends — SuperMap, ArcGIS Pro, ArcMap, QGIS, qgis-cli (headless Processing), GDAL, PostGIS, GeoServer, istSOS, SuperMap iServer, plus a data catalog — through a single set of **40 semantic verbs** and one registry, instead of learning each platform's private tool dialect.

Platform-specific capabilities are not flattened away: they are exposed as extensions and **honestly labeled**.

## The honest ledger

Every capability in this repository carries an evidence-based status. Statuses change only when evidence changes — never by declaration.

| Metric | Value (v0.3.0) |
|---|---|
| Backends | 10 + data catalog |
| Capability leaves | 208 |
| — verified working (`ok`) | 165 |
| — not yet verified (`unverified`) | 21 |
| — not supported (`not_supported`) | 22 |
| Offline protocol self-test | 154 / 154 passing |

The full ledger lives in `leaves-full.json`; per-backend calibration levels and their evidence references live in `code/backends.json`. Phase reports (`PHASE0-REPORT.md` … `PHASE5-REPORT.md`) document how each number was earned, including the failures.

Run the self-test yourself:

```bash
python code/selftest.py   # offline protocol self-check — not a live calibration
```

## The Completion Initiative

**21 leaves are still `unverified`, and three integrations are deferred — not because they failed, but because nobody with the right environment has run them yet:**

- **SuperMap iServer** — verified only against the public demo instance; needs a run against a local/intranet instance.
- **QGIS in-app bridge** — the headless `qgis-cli` channel is calibrated; the live in-app bridge is not.
- **PostGIS production DSN** — verified on an isolated local cluster (templates 38/38, gateway 21/21); production instances untested.

If you have any of these environments, you can finish a leaf. Pick an `unverified` leaf from `leaves-full.json`, run the corresponding probe against your instance, and open a PR with the evidence (versions, commands, raw output). A leaf is upgraded only on reproducible evidence — that rule is the whole point of this project. See `CONTRIBUTING.md`.

## Where this sits

- **gis-agent-bridges** — per-platform agent bridges (the compatibility layer this gateway routes to).
- **Definitio** — an agent-native GIS protocol and reference runtime, designed from scratch for agents rather than adapted from desktop GIS. Coming December 2026. This gateway is its compatibility layer and test bench.

## Status

v0.3.0 — engineering line closed on 2026-11-12 with the ledger above. Deferred items reopen as small stages when someone (maybe you) brings the environment.

## License

Apache License 2.0. See `LICENSE`.

---

作者：Huangyu Rao（[@YUYU20061107](https://github.com/YUYU20061107)）。设计原则只有一条：**状态只许按证据改**——没验过的就写没验过。
