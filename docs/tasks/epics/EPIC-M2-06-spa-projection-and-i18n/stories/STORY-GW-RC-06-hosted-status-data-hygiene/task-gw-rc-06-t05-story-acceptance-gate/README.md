# task-gw-rc-06-t05

## Meta
- **Story:** [STORY-GW-RC-06](../STORY-GW-RC-06-hosted-status-data-hygiene.md)
- **Type:** tests
- **Status:** ⚪ Todo
- **Package:** pkg-000035
- **Skill declared:** python-pro
- **Depends on:** T01–T04

## Purpose
Story acceptance gate: all parent AC verified; hosted data hygiene complete.

## Code Facts
- Parent AC — [`STORY-GW-RC-06-hosted-status-data-hygiene.md`](../STORY-GW-RC-06-hosted-status-data-hygiene.md) §Acceptance Criteria
- Active pkg — [`pkg-000035-20260620-gw-rc-06-hosted-status-data-hygiene.yaml`](../../../../../../gateway-active-packages/pkg-000035-20260620-gw-rc-06-hosted-status-data-hygiene.yaml)
- Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)

## Acceptance / DoD
- All 3 parent AC PASS in [`story-acceptance-gate-STORY-GW-RC-06.md`](./story-acceptance-gate-STORY-GW-RC-06.md)
- `builder_resolve_queue --project gateway --verify` → ok 5 paths
- T01–T04 acceptance artifacts referenced in gate
- BULLRUN phases complete
- Acceptance file signed (Date only after live hosted verify in P3/P6)

## Where to change
- `story-acceptance-gate-STORY-GW-RC-06.md` (gate Date after live verify only)
- `bullrun-launch-index.md` story row

## Out of scope
- New feature work
- Application code (RC-05)

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
# Hosted verify evidence from T04 referenced in gate
```
