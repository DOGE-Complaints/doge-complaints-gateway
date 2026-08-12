# task-gw-rc-05-t05

## Meta
- **Story:** [STORY-GW-RC-05](../STORY-GW-RC-05-status-vocabulary-canonicalization.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000034
- **Skill declared:** python-pro
- **Depends on:** T01–T04

## Purpose
Story acceptance gate: all parent AC verified; full unit suite green.

## Code Facts
- Parent AC — [`STORY-GW-RC-05-status-vocabulary-canonicalization.md`](../STORY-GW-RC-05-status-vocabulary-canonicalization.md) §Acceptance Criteria
- Active pkg — [`pkg-000034-20260620-gw-rc-05-status-vocabulary-canonicalization.yaml`](../../../../../../gateway-active-packages/pkg-000034-20260620-gw-rc-05-status-vocabulary-canonicalization.yaml)
- Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)

## Acceptance / DoD
- All 5 parent AC PASS in [`story-acceptance-gate-STORY-GW-RC-05.md`](./story-acceptance-gate-STORY-GW-RC-05.md)
- `builder_resolve_queue --project gateway --verify` → ok 5 paths
- Unit suite without regressions
- BULLRUN phases complete
- Acceptance file signed (Date only after live pytest in P3/P6)

## Where to change
- `story-acceptance-gate-STORY-GW-RC-05.md` (gate Date after live pytest only)
- `bullrun-launch-index.md` story row

## Out of scope
- New feature work
- Hosted data migration (GW-RC-06)

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest --ignore=tests/integration --ignore=tests/smoke -q
```
