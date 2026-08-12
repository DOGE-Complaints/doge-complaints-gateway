# task-gw-rc-04-t09

## Meta
- **Story:** [STORY-GW-RC-04](../STORY-GW-RC-04-columnar-model-migration.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000033
- **Skill declared:** python-pro
- **Depends on:** T01–T08

## Purpose
Story acceptance gate: all parent AC verified; full unit suite green.

## Code Facts
- Parent AC — [`STORY-GW-RC-04-columnar-model-migration.md`](../STORY-GW-RC-04-columnar-model-migration.md) §Acceptance Criteria
- Active pkg — [`pkg-000033-20260619-gw-rc-04-columnar-model-migration.yaml`](../../../../../../gateway-active-packages/pkg-000033-20260619-gw-rc-04-columnar-model-migration.yaml)

## Acceptance / DoD
- All 5 parent AC PASS in [`story-acceptance-gate-STORY-GW-RC-04.md`](./story-acceptance-gate-STORY-GW-RC-04.md)
- `builder_resolve_queue --project gateway --verify` → ok 9 paths
- Unit suite without regressions
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `story-acceptance-gate-STORY-GW-RC-04.md` (gate Date after live pytest only)
- `bullrun-launch-index.md` story row

## Out of scope
- New feature work

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest --ignore=tests/integration --ignore=tests/smoke -q
```
