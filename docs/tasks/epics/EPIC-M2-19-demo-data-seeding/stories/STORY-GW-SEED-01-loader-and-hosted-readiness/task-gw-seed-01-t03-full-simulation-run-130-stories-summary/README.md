# task-gw-seed-01-t03

## Meta
- **Story:** [STORY-GW-SEED-01](../STORY-GW-SEED-01-loader-and-hosted-readiness.md)
- **Type:** verify
- **Status:** ⚪ Todo
- **Package:** pkg-000036
- **Skill declared:** python-pro
- **Depends on:** T02

## Purpose
Полный прогон 130 историй; сводка success/failed.

## Code Facts
- Loader full run — [`tests/simulation_runner.py`](../../../../../../../tests/simulation_runner.py) — default all canvas items (130)
- Canvas count — [`dogestonia_simulation_canvas_v0_1.json`](../../../../../../../tests/sandbox/dogestonia_simulation_canvas_v0_1.json) — 130 stories per [`interview-seed-demo-data-2026-06-20.md`](../../../../../../analysis/interview-seed-demo-data-2026-06-20.md)
- Manual — [`simulation-runner-manual.md`](../../../../../../runtime-docs/testing/simulation-runner-manual.md)

## Acceptance / DoD
- Traces parent AC: полный прогон → сводка зафиксирована (AC3)
- Full run `python tests/simulation_runner.py` (no `--max`) against hosted
- Summary artifact: total/success/failed counts in this task folder
- Exit 0 or documented partial failures with root cause
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- Task artifacts: full-run summary JSON/markdown in this task folder

## Out of scope
- SQL row count verify (T04)
- Board/card verification (SEED-03)
- Dataset expansion (SEED-02)

## Verification commands
```bash
cd doge-complaints-gateway
python tests/simulation_runner.py
# Expected: 130 stories processed; summary captured in task artifact
```
