# task-gw-rc-07-t05

## Meta
- **Story:** [STORY-GW-RC-07](../STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000047
- **Skill declared:** python-pro
- **Depends on:** T01–T04

## Purpose
Story acceptance gate: hosted board API restored; all parent AC verified.

## Code Facts
- Parent AC — [`STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md`](../STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md) §Acceptance Criteria
- Active pkg — [`pkg-000047-20260710-gw-rc-07-hosted-tallinn-issues-internal-error.yaml`](../../../../../../gateway-active-packages/pkg-000047-20260710-gw-rc-07-hosted-tallinn-issues-internal-error.yaml)
- Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)

## Acceptance / DoD
- All 4 parent AC PASS in [`story-acceptance-gate-STORY-GW-RC-07.md`](./story-acceptance-gate-STORY-GW-RC-07.md)
- Live `GET /tallinn/issues` → valid issues JSON (not INTERNAL_ERROR)
- `builder_resolve_queue --project gateway --verify` → ok 5 paths
- T01–T04 acceptance artifacts referenced in gate
- BULLRUN phases complete
- Gate Date only after live verify in P3/P6

## Where to change
- `story-acceptance-gate-STORY-GW-RC-07.md` (gate Date after live verify only)
- `bullrun-launch-index.md` story row

## Out of scope
- SEED-03 full E2E (follows after gate PASS)

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
curl -sS "https://dogestonia-tallinn.up.railway.app/tallinn/issues"
```
