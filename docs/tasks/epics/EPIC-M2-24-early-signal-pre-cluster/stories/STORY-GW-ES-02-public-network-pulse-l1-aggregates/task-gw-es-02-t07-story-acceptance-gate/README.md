# task-gw-es-02-t07-story-acceptance-gate

## Meta
- **Story:** [STORY-GW-ES-02](../STORY-GW-ES-02-public-network-pulse-l1-aggregates.md)
- **Type:** gate
- **Status:** 🟢 Done
- **Package:** pkg-000059
- **Skill declared:** python-pro
- **Depends on:** T00–T06 Done
- **decision_ref:** backlog ES-02 Acceptance Criteria; [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)

## Purpose
Story acceptance-verification: все AC ES-02 PASS с evidence; заполнить `story-acceptance-gate-STORY-GW-ES-02.md` по template. **Date:** только после live pytest + `--verify` в сессии выполнения (не при P1 scaffold).

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Pipeline story AC — [`STORY-GW-ES-02-….md`](../STORY-GW-ES-02-public-network-pulse-l1-aggregates.md)
- Backlog source — [`backlog-stories/…/STORY-GW-ES-02-….md`](../../../../../../backlog-stories/early-signal-pre-cluster/STORY-GW-ES-02-public-network-pulse-l1-aggregates.md)

## Acceptance / DoD
- [x] All story AC checked with evidence paths
- [x] `story-acceptance-gate-STORY-GW-ES-02.md` Result PASS|FAIL
- [x] `acceptance-verification-gw-es-02-t07.md` signed
- [x] Live: `pytest` ES-02 + Issues regression + `--project gateway --verify`
- [x] Gate Date from `--print-utc-now` after live verify (not scaffold time)
- [x] BULLRUN phases complete; sync bullrun/INDEX on Done

## Where to change
- This task folder only: gate + acceptance artifacts

## Out of scope
- New product scope; ES-03; invent path

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_es_02_*.py tests/test_gw_public_01_public_issues_regression.py
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now
```
