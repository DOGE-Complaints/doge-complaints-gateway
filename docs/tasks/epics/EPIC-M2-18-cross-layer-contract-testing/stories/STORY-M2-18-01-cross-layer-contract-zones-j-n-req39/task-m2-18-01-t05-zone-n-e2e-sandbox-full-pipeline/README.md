## Task workspace — `task-m2-18-01-t05-zone-n-e2e-sandbox-full-pipeline`

- Story: [`../STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md`](../STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md)
- Decision Ref: [`../../../../../../requirements/39-cross-layer-contract-testing.md`](../../../../../../requirements/39-cross-layer-contract-testing.md) — Zone **N**

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000020`  
---

## Task: tests — E2E sandbox canvas full pipeline

### Цель
E2E sandbox canvas full pipeline (Zone **N**). Offline contract tests; дополняют REQ acceptance suites, не заменяют `test_req24_*` / `test_req40_*` без решения оператора.

### Факты из кода
1. Canvas: `tests/sandbox/dogestonia_simulation_canvas_v0_1.json`.
2. `test_e2e_simulation_canvas_intake.py` — intake-only today.
3. Clustering: `process_all_pending()` after canvas intake (not HTTP trigger).

### Gap / Проблема
Demo can break between clustering and `GET /tallinn/issues` undetected.

### AC/DoD
- [x] (P0) N-01..N-06 per REQ-39 §N (intake all scenarios, issues exist, GET list, status filter, required fields, geo filter).
- [x] (P0) `TestClient` + demo env fixtures.
- [x] (P1) Depends on T03 clustering pattern.

### Где менять код
- `tests/test_e2e_sandbox_full_pipeline.py` (new)

### Out of scope
Changing canvas JSON; live Supabase.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_e2e_sandbox_full_pipeline.py
```
