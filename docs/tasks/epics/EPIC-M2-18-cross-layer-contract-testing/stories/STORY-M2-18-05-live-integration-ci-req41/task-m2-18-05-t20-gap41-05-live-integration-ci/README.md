## Task workspace — `task-m2-18-05-t20-gap41-05-live-integration-ci`

- Story: [`../STORY-M2-18-05-live-integration-ci-req41.md`](../STORY-M2-18-05-live-integration-ci-req41.md)
- Decision Ref: [`../../../../../../requirements/41-testing-production-coverage-target-state.md`](../../../../../../requirements/41-testing-production-coverage-target-state.md) §3 GAP-41-05; PS-13, PS-14

---
**Приоритет:** P0  
**Сложность:** M  
**Оценка времени:** ~3–5 ч  
**Статус:** Done  
**Wave:** `pkg-000021`  
---

## Task: CI — live Supabase integration workflow

### Цель
Marker `live_integration`; `.github/workflows/integration-live.yml`; mark existing [`tests/integration/supabase/*`](../../../../../../../tests/integration/supabase/).

### Почему это важно (риск)
Live tests skip without `SUPABASE_TEST_URL`; no CI gate; no pytest marker separation from offline suite.

### Факты из кода
1. [`tests/integration/supabase/test_supabase_live.py`](../../../../../../../tests/integration/supabase/test_supabase_live.py) — skip pattern `SUPABASE_TEST_URL`.
2. Gateway: **no** `.github/workflows/` (glob 0).
3. [`pyproject.toml`](../../../../../../../pyproject.toml) — no `live_integration` marker yet.

### Gap / Проблема
**GAP-41-05:** live integration not in CI pipeline.

### AC/DoD
- [x] (P0) Register `live_integration` marker in `pyproject.toml` `[tool.pytest.ini_options]`.
- [x] (P0) `live_integration` on supabase tests via `tests/conftest.py` → `pytest_collection_modifyitems`.
- [x] (P0) Workflow: secrets `SUPABASE_TEST_URL`, `SUPABASE_TEST_SERVICE_ROLE_KEY`; `pytest -m live_integration`.
- [x] (P0) Default offline CI excludes `-m live_integration` (`.github/workflows/test-offline.yml`).
- [x] (P1) Document required secrets in workflow comments / arch doc cross-ref.

### Где менять код
- [`pyproject.toml`](../../../../../../../pyproject.toml)
- `tests/integration/supabase/*.py`
- `.github/workflows/integration-live.yml` (new)

### Out of scope
- Provisioning Supabase project; editing `pkg-000020`.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q -m live_integration --collect-only
# With env:
SUPABASE_TEST_URL=... python3 -m pytest -q -m live_integration
```
