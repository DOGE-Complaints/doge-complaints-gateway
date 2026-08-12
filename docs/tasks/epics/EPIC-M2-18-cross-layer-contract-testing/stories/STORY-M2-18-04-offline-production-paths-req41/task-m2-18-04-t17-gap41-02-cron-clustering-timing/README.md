## Task workspace — `task-m2-18-04-t17-gap41-02-cron-clustering-timing`

- Story: [`../STORY-M2-18-04-offline-production-paths-req41.md`](../STORY-M2-18-04-offline-production-paths-req41.md)
- Decision Ref: [`../../../../../../requirements/41-testing-production-coverage-target-state.md`](../../../../../../requirements/41-testing-production-coverage-target-state.md) §3 GAP-41-02; PS-03, PS-04

---
**Приоритет:** P1  
**Сложность:** M  
**Оценка времени:** ~2–4 ч  
**Статус:** Done  
**Wave:** `pkg-000021`  
---

## Task: tests — full-stack cron clustering timing contract

### Цель
`tests/test_cron_clustering_timing_contract.py` (CT-01..03): real `StoryClusterOrchestrator` + ASGI lifespan cron, not `_OrchestratorStub`.

### Почему это важно (риск)
[`test_cluster_cron_job.py`](../../../../../../../tests/test_cluster_cron_job.py) L22–30 stubs orchestrator; production path is intake → wait interval → `process_all_pending()` → `doge_issues`.

### Факты из кода
1. [`test_cluster_cron_job.py`](../../../../../../../tests/test_cluster_cron_job.py) — `_OrchestratorStub`, `sleep(1.2)` only tests job loop.
2. [`test_clustering_pipeline_contract.py`](../../../../../../../tests/test_clustering_pipeline_contract.py) — real orchestrator via `get_api_dependencies()` + TestClient intake pattern.
3. REQ-41 CT-01: `CLUSTER_CRON_INTERVAL_S=1`, `CLUSTER_MIN_SIZE=1`; after `sleep(1.5)` ≥ 1 issue in store.

### Gap / Проблема
**GAP-41-02:** no temporal window test for cron-triggered clustering.

### AC/DoD
- [x] (P0) CT-01: after `sleep(1.5)` with 2 stories intaken → `doge_issues` / projections ≥ 1.
- [x] (P0) CT-02: before interval (`sleep(0.3)`) → no issue yet.
- [x] (P0) CT-03: `CLUSTER_CRON_ENABLED=false` → no issue after `sleep(1.5)`.
- [x] (P1) CT-01 completes in &lt; 5s (REQ-41 AC-41-2).

### Где менять код
- `tests/test_cron_clustering_timing_contract.py` (new)

### Out of scope
- Replacing [`test_cluster_cron_job.py`](../../../../../../../tests/test_cluster_cron_job.py); prod scheduler rewrite.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_cron_clustering_timing_contract.py
```
