## Task workspace — `task-m2-18-01-t03-zone-j-clustering-pipeline-contract`

- Story: [`../STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md`](../STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md)
- Decision Ref: [`../../../../../../requirements/39-cross-layer-contract-testing.md`](../../../../../../requirements/39-cross-layer-contract-testing.md) — Zone **J**

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000020`  
---

## Task: tests — Clustering pipeline stitch contract

### Цель
Clustering pipeline stitch contract (Zone **J**). Offline contract tests; дополняют REQ acceptance suites, не заменяют `test_req24_*` / `test_req40_*` без решения оператора.

### Факты из кода
1. `StoryClusterOrchestrator.process_all_pending()` — used in `tests/test_req24_tallinn_issues_read_api.py` L56+.
2. REQ-39 examples mention `POST /clustering/trigger` — **route not in** `src/core/api/` (as-is: orchestrator call).
3. `CLUSTER_MIN_SIZE`, `issue_projection_store` / read store after clustering.

### Gap / Проблема
Clustering → `doge_issues` stitch can break without cross-layer test.

### AC/DoD
- [x] (P0) J-01..J-04 per REQ-39 §J adapted to `process_all_pending()`.
- [x] (P0) `CLUSTER_MIN_SIZE=1`, `APP_PROFILE=demo`, cache clear pattern from req24 tests.
- [x] (P1) Idempotency: no duplicate `issue_id` on second `process_all_pending()`.

### Где менять код
- `tests/test_clustering_pipeline_contract.py` (new)

### Out of scope
New HTTP clustering endpoint; Supabase live.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_clustering_pipeline_contract.py
```
