# task-gw-rc-03-t05

## Meta
- **Story:** [STORY-GW-RC-03](../STORY-GW-RC-03-contract-guarantee-and-legacy-data.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000032
- **Skill declared:** python-pro
- **Depends on:** T01–T04 (T03 N/A if T02 defer)

## Purpose
Story acceptance gate — rollup всех parent AC с evidence и live verification (AC-4: тест-суит без регрессий).

## Code Facts
- `story-acceptance-gate-STORY-GW-RC-03.md` — gate scaffold (этот таск)
- Parent story AC checklist (4 items verbatim from backlog)

## Acceptance / DoD
- Traces: all parent AC signed in story gate
- `builder_resolve_queue.py --project gateway --verify` ok 5 paths
- Full unit suite pass (`--ignore=tests/integration --ignore=tests/smoke`)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `story-acceptance-gate-STORY-GW-RC-03.md`
- `acceptance-verification-gw-rc-03-t05.md`

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_03_contract_guarantee.py -q
cd doge-complaints-gateway && python3 -m pytest --ignore=tests/integration --ignore=tests/smoke -q
```
