# task-gw-seed-01-t05

## Meta
- **Story:** [STORY-GW-SEED-01](../STORY-GW-SEED-01-loader-and-hosted-readiness.md)
- **Type:** tests
- **Status:** ⚪ Todo
- **Package:** pkg-000036
- **Skill declared:** python-pro
- **Depends on:** T01–T04

## Purpose
Story acceptance gate: all parent AC verified; hosted loader + readiness complete.

## Code Facts
- Parent AC — [`STORY-GW-SEED-01-loader-and-hosted-readiness.md`](../STORY-GW-SEED-01-loader-and-hosted-readiness.md) §Acceptance Criteria
- Active pkg — [`pkg-000036-20260621-gw-seed-01-loader-and-hosted-readiness.yaml`](../../../../../../gateway-active-packages/pkg-000036-20260621-gw-seed-01-loader-and-hosted-readiness.yaml)
- Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)

## Acceptance / DoD
- All 4 parent AC PASS in [`story-acceptance-gate-STORY-GW-SEED-01.md`](./story-acceptance-gate-STORY-GW-SEED-01.md)
- `builder_resolve_queue --project gateway --verify` → ok 5 paths
- T01–T04 acceptance artifacts referenced in gate
- BULLRUN phases complete
- Acceptance file signed (Date only after live hosted verify in P3/P6)

## Where to change
- `story-acceptance-gate-STORY-GW-SEED-01.md` (gate Date after live verify only)
- `bullrun-launch-index.md` story row

## Out of scope
- Dataset expansion (SEED-02)
- E2E board runbook (SEED-03)
- Application code

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
# Hosted verify evidence from T01–T04 referenced in gate
```
