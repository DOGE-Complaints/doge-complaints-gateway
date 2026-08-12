# task-gw-rc-02-t06

## Meta
- **Story:** [STORY-GW-RC-02](../STORY-GW-RC-02-type-canonical-on-read.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000031
- **Skill declared:** python-pro
- **Depends on:** T01–T05

## Purpose
Закрыть `story-acceptance-gate-STORY-GW-RC-02.md` — rollup всех parent AC с evidence и live verification (AC-4: тест-суит без регрессий).

## Code Facts
- `story-acceptance-gate-STORY-GW-RC-02.md` — gate scaffold (этот таск)
- Parent story AC checklist (4 items verbatim from backlog)

## Acceptance / DoD
- Traces: all parent AC signed in story gate
- `builder_resolve_queue.py --project gateway --verify` ok 6 paths
- Full unit suite pass (`--ignore=tests/integration --ignore=tests/smoke`)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `story-acceptance-gate-STORY-GW-RC-02.md`
- `acceptance-verification-gw-rc-02-t06.md`

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_02_type_canonical_on_read.py -q
cd doge-complaints-gateway && python3 -m pytest --ignore=tests/integration --ignore=tests/smoke -q
```
