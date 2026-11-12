# Contributing — the Completion Initiative

This project's capability ledger (`leaves-full.json`) is deliberately incomplete:
21 leaves are marked `unverified`, and a few integrations are deferred. They are
open invitations.

## How to complete a leaf

1. Pick a leaf with status `unverified` from `leaves-full.json`
   (or one of the deferred integrations listed in the README).
2. Run the matching backend/probe in **your** environment — e.g. a local
   SuperMap iServer instance, a desktop QGIS session, a production PostGIS.
3. Open a PR that includes:
   - software versions (backend, OS, gateway commit),
   - the exact commands you ran,
   - the raw output (logs welcome; redact credentials and private paths),
   - your proposed status change for the leaf.

## The one rule

**Statuses change only on evidence.** A leaf moves from `unverified` to `ok`
only when a reviewer can reproduce the result from your PR. "It should work"
is not evidence, and neither is a screenshot of a success toast.

Negative results are contributions too: if a leaf fails in your environment,
report it — a well-documented failure upgrades everyone's map.

## Safety

Destructive operations behind the gateway's confirmation gates stay gated.
Do not weaken confirmation checks to make a test pass.
