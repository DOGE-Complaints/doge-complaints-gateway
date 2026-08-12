## Task workspace — `task-m2-06-06-t08-req24-acceptance-tests-and-openapi`

- Story: [`../STORY-M2-06-06-tallinn-issues-read-api-req24.md`](../STORY-M2-06-06-tallinn-issues-read-api-req24.md)
- Decision Ref: REQ-24 §7, §6 step 12; GAP-24-08

---
**Приоритет:** P0  
**Сложность:** L  
**Оценка времени:** ~3–4 ч  
**Статус:** ready  
**Wave:** `pkg-000019`  
---

## Task: tests — REQ-24 acceptance and OpenAPI

### Цель
Добавить `tests/test_req24_tallinn_issues_read_api.py` (AC-1..AC-20), обновить OpenAPI (AC-13), закрыть story gate.

### Факты из кода
1. REQ-24 §7 — AC-1 asserts table `doge_issues` (not `tallinn_issues_projections`).
2. Pattern: [`tests/test_req40_geo_propagation.py`](../../../../../../../tests/test_req40_geo_propagation.py) — dedicated REQ acceptance file.
3. [`docs/runtime-docs/api-reference/openapi.yaml`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) — paths без `/tallinn/issues` (verify at implementation).
4. E2E patterns: [`tests/test_e2e_story_cluster_issue_pipeline.py`](../../../../../../../tests/test_e2e_story_cluster_issue_pipeline.py) + `TestClient`.

### Gap / Проблема
**GAP-24-08:** нет regression suite и contract doc для read API.

### AC/DoD
- [ ] (P0) `tests/test_req24_tallinn_issues_read_api.py` covers AC-1..AC-20 (skip Supabase live where needed).
- [ ] (P0) AC-1: `doge_issues` table exists (SQLite assertion).
- [ ] (P0) AC-3..4, AC-5..8, AC-9..12 HTTP via TestClient.
- [ ] (P0) AC-13: OpenAPI three endpoints; POST security Bearer.
- [ ] (P0) `acceptance-verification-m2-06-06-t08.md` + story gate PASS.
- [ ] (P1) `pytest -q` full suite green.

### Где менять код
- [`tests/test_req24_tallinn_issues_read_api.py`](../../../../../../../tests/test_req24_tallinn_issues_read_api.py) (new)
- [`docs/runtime-docs/api-reference/openapi.yaml`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml)
- [`story-acceptance-gate-STORY-M2-06-06.md`](../story-acceptance-gate-STORY-M2-06-06.md) (new at close)

### Out of scope
- SPA changes
- REQ-24 requirements doc table-name sync (optional follow-up)

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_req24_tallinn_issues_read_api.py
cd /Users/eslinko/Development/DOGEstonia && python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify
```
