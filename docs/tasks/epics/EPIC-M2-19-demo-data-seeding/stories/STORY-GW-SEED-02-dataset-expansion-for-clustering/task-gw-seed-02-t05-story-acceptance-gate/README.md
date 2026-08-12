# task-gw-seed-02-t05

## Meta
- **Story:** [STORY-GW-SEED-02](../STORY-GW-SEED-02-dataset-expansion-for-clustering.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000037
- **Skill declared:** python-pro
- **Depends on:** T01–T04

## Purpose
Story acceptance gate: all parent AC verified; dataset expansion + local clustering verify complete.

## Code Facts
- Parent AC — [`STORY-GW-SEED-02-dataset-expansion-for-clustering.md`](../STORY-GW-SEED-02-dataset-expansion-for-clustering.md) §Acceptance Criteria
- Active pkg — [`pkg-000037-20260622-gw-seed-02-dataset-expansion-for-clustering.yaml`](../../../../../../gateway-active-packages/pkg-000037-20260622-gw-seed-02-dataset-expansion-for-clustering.yaml)
- Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)

## Acceptance / DoD
- All 4 parent AC PASS in [`story-acceptance-gate-STORY-GW-SEED-02.md`](./story-acceptance-gate-STORY-GW-SEED-02.md)
- `builder_resolve_queue --project gateway --verify` → ok 5 paths
- T01–T04 acceptance artifacts referenced in gate
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- `story-acceptance-gate-STORY-GW-SEED-02.md` (gate Date after live verify only)
- `bullrun-launch-index.md` story row

## Out of scope
- E2E hosted board verify (SEED-03)
- Application code (`src/core/`)

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
# Evidence from T01–T04 artifacts referenced in gate
```
