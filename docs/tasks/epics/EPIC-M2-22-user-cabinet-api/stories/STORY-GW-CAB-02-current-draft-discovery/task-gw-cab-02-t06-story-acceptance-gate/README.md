# task-gw-cab-02-t06-story-acceptance-gate

## Meta
- **Story:** [STORY-GW-CAB-02](../STORY-GW-CAB-02-current-draft-discovery.md)
- **Type:** gate
- **Status:** 🟢 Done
- **Package:** pkg-000053
- **Skill declared:** python-pro
- **Depends on:** T01–T05

## Purpose
Story acceptance gate: live verify all AC (including AC-6 offline suite), sign [`story-acceptance-gate-STORY-GW-CAB-02.md`](./story-acceptance-gate-STORY-GW-CAB-02.md), update bullrun story row.

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Parent AC verbatim — pipeline story §Acceptance Criteria
- pkg — `pkg-000053-20260714-gw-cab-02-current-draft-discovery.yaml`

## Acceptance / DoD
- [x] All AC-1..AC-6 PASS in gate doc with evidence
- [x] `--verify --check-dates` ok for pkg-000053
- [x] Offline pytest green
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-cab-02-t06.md`](./acceptance-verification-gw-cab-02-t06.md) signed

## Where to change
- [`story-acceptance-gate-STORY-GW-CAB-02.md`](./story-acceptance-gate-STORY-GW-CAB-02.md)
- [`bullrun-launch-index.md`](../../../../bullrun-launch-index.md) — story row Done

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"
```
