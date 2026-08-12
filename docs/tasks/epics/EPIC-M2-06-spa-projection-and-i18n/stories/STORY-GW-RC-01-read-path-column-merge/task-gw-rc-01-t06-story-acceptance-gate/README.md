# task-gw-rc-01-t06

## Meta
- **Story:** [STORY-GW-RC-01](../STORY-GW-RC-01-read-path-column-merge.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000030
- **Skill declared:** python-pro
- **Depends on:** T01–T05

## Purpose
Закрыть `story-acceptance-gate-STORY-GW-RC-01.md` — rollup всех parent AC с evidence и live verification.

## Code Facts
- `story-acceptance-gate-STORY-GW-RC-01.md` — gate scaffold (этот таск)
- Parent story AC checklist (5 items verbatim from backlog)

## Acceptance / DoD
- Traces: all parent AC signed in story gate
- `builder_resolve_queue.py --project gateway --verify` ok 6 paths
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `story-acceptance-gate-STORY-GW-RC-01.md`

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_01_read_path_column_merge.py -q
cd doge-complaints-gateway && python3 -m pytest tests/ -q --ignore=tests/smoke --ignore=tests/integration
```
