# task-gw-seed-02-t03

## Meta
- **Story:** [STORY-GW-SEED-02](../STORY-GW-SEED-02-dataset-expansion-for-clustering.md)
- **Type:** verify
- **Status:** 🟢 Done
- **Package:** pkg-000037
- **Skill declared:** python-pro
- **Depends on:** T02

## Purpose
Локальная проверка: загрузка v0_2 (`SIMULATION_CANVAS_PATH`) + кластеризация/промоушн при **`CLUSTER_MIN_SIZE=8`** (не понижать, D-SEED-2). Подтвердить формирование issue projections.

**Note:** backlog-черновик T03 допускал «временно min_size меньше» — **в этой story запрещено** (D-SEED-2). Верификация только при prod-like порогах.

## Code Facts
- Cron batch — [`cluster_orchestrator.py:156-197`](../../../../../../../src/core/application/cluster_orchestrator.py#L156-L197) `process_all_pending`
- Issue created log — [`cluster_orchestrator.py:368-380`](../../../../../../../src/core/application/cluster_orchestrator.py#L368-L380) `story_cluster_issue_created`
- Promotion gates — [`gates.py:17-37`](../../../../../../../src/core/promotion/gates.py#L17-L37)
- Simulation runner — [`tests/simulation_runner.py`](../../../../../../../tests/simulation_runner.py)
- Canvas v0_2 — [`tests/sandbox/dogestonia_simulation_canvas_v0_2.json`](../../../../../../../tests/sandbox/dogestonia_simulation_canvas_v0_2.json)

## Acceptance / DoD
- Traces parent AC: на прогоне формируются проекции issue (локально подтверждено)
- Env for verify: `CLUSTER_MIN_SIZE=8`, `CLUSTER_READINESS_THRESHOLD` per prod-like (88 or documented in matrix)
- Artifact [`cluster-verify-summary.md`](./cluster-verify-summary.md): ready count, cluster sizes ≥8, `created_issue_count` > 0, sample issue_ids
- Pre-check: offline cluster size ≥8 per T01 targets before live run
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- Task artifact: `cluster-verify-summary.md`
- Optional: `tests/test_gw_seed_02_cluster_density.py` (fixture smoke; v0_1 tests stay green)
- `.env.test.example` — hint `SIMULATION_CANVAS_PATH=tests/sandbox/dogestonia_simulation_canvas_v0_2.json`
- **No** `src/core/` changes

## Out of scope
- Hosted Railway/Supabase prod verify (SEED-03)
- Lowering `CLUSTER_MIN_SIZE` for convenience
- Manual cron trigger (none exists)

## Verification commands
```bash
cd doge-complaints-gateway
# Load v0_2 (sqlite or supabase per .env.test) then cluster batch:
# SIMULATION_CANVAS_PATH=tests/sandbox/dogestonia_simulation_canvas_v0_2.json \
# CLUSTER_MIN_SIZE=8 make simulate  # or documented subset
# Then via API deps or logs:
# orchestrator.process_all_pending() -> len(issue_ids) > 0
python3 -m pytest -q tests/ -k "seed_02"  # if test added in this task
```
