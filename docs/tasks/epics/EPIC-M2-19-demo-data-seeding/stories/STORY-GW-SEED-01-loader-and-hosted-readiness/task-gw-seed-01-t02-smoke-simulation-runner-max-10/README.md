# task-gw-seed-01-t02

## Meta
- **Story:** [STORY-GW-SEED-01](../STORY-GW-SEED-01-loader-and-hosted-readiness.md)
- **Type:** verify
- **Status:** ⚪ Todo
- **Package:** pkg-000036
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Smoke-прогон загрузчика `--max 10` против hosted; зафиксировать результат (intake 200/202).

## Code Facts
- Loader — [`tests/simulation_runner.py`](../../../../../../../tests/simulation_runner.py) — `--max` arg [:150-152](../../../../../../../tests/simulation_runner.py#L150-L152); POST `/intake/stories`
- Env — [`.env.test`](../../../../../../../.env.test) — `GATEWAY_URL`, `GATEWAY_API_TOKEN` (secrets not committed)
- Manual — [`simulation-runner-manual.md`](../../../../../../runtime-docs/testing/simulation-runner-manual.md)
- Canvas — [`dogestonia_simulation_canvas_v0_1.json`](../../../../../../../tests/sandbox/dogestonia_simulation_canvas_v0_1.json) (130 items)

## Acceptance / DoD
- Traces parent AC: Smoke `--max 10` → все приняты (partial AC3)
- `python tests/simulation_runner.py --max 10` exits 0 against hosted `GATEWAY_URL`
- All 10 intake responses 200/202; no errors in stdout
- Smoke summary artifact saved in this task folder
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- Task artifacts: smoke run log/summary in this task folder
- **Not** `src/core/` unless unexpected intake failure

## Out of scope
- Full 130 run (T03)
- SQL verification (T04)
- Hosted readiness (T01)

## Verification commands
```bash
cd doge-complaints-gateway
python tests/simulation_runner.py --max 10
# Expected: 10/10 accepted; exit 0
```
