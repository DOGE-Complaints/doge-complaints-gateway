## Task workspace — `task-m2-18-03-t22-audit-gap41-01-pytest-asyncio-dev-install`

- Story: [`../STORY-M2-18-03-local-real-http-smoke-req41.md`](../STORY-M2-18-03-local-real-http-smoke-req41.md)
- Decision Ref: [`../../../../../../analysis/audit-req41-production-coverage-target-state-2026-05-18.md`](../../../../../../analysis/audit-req41-production-coverage-target-state-2026-05-18.md) §9 GAP-AUDIT-REQ41-01; [`../../../../../../requirements/41-testing-production-coverage-target-state.md`](../../../../../../requirements/41-testing-production-coverage-target-state.md) AC-41-4

---
**Приоритет:** P1  
**Сложность:** S  
**Оценка времени:** ~20 мин  
**Статус:** Done  
**Wave:** audit override (`run_mode=story18_audit_req41_followup`)  
---

## Task: dev install — pytest-asyncio for AC-41-4 async smoke

### Цель
Гарантировать установку `pytest-asyncio` из dev extras в рабочем venv и зафиксировать проверку AC-41-4 (`tests/smoke/test_local_server_async_read.py`), чтобы async smoke не давал false pass/skip из-за отсутствия плагина.

### Почему это важно (риск)
Зависимость объявлена в `pyproject.toml`, но без `pip install -e ".[dev]"` плагин может отсутствовать в venv — `@pytest.mark.asyncio` не выполняется корректно (аудит §9).

### Факты из кода
1. [`pyproject.toml`](../../../../../../../pyproject.toml) L19–22 — `pytest-asyncio>=0.24.0` в `[project.optional-dependencies] dev`.
2. [`pyproject.toml`](../../../../../../../pyproject.toml) L31–32 — `asyncio_mode = "auto"`.
3. [`tests/smoke/test_local_server_async_read.py`](../../../../../../../tests/smoke/test_local_server_async_read.py) L30 — `@pytest.mark.asyncio` (AC-01..AC-03).

### Gap / Проблема
**GAP-AUDIT-REQ41-01:** `pytest-asyncio` в `pyproject.toml`, но не установлен в venv → AC-41-4 под риском.

### AC/DoD
- [x] (P0) `pip install -e ".[dev]"` (или эквивалент) в venv проекта; `python -c "import pytest_asyncio"` успешен.
- [x] (P0) `pytest tests/smoke/test_local_server_async_read.py -q` без missing-plugin / asyncio warnings (при `LOCAL_SERVER_URL` — полный прогон; без URL — ожидаемые skip, не false pass).
- [x] (P1) REQ-41 §7: `pip install -e ".[dev]"` перед smoke/async (вместо корневого README — docs-only ветка).
- [x] (P1) [`.github/workflows/test-offline.yml`](../../../../../../../.github/workflows/test-offline.yml) — уже `pip install -e ".[dev]"`.

### Acceptance
- [`acceptance-verification-m2-18-03-t22.md`](./acceptance-verification-m2-18-03-t22.md) — PASS (2026-05-19)

### Где менять (P5)
- Оператор: venv install (обязательно).
- Опционально: [`README.md`](../../../../../../../README.md), [`.github/workflows/test-offline.yml`](../../../../../../../.github/workflows/test-offline.yml).

### Out of scope
- Изменение логики smoke-тестов.
- `pkg-000021` YAML; новый `pkg-*`.

### Команды проверки
```bash
cd doge-complaints-gateway && pip install -e ".[dev]"
python -c "import pytest_asyncio; print(pytest_asyncio.__version__)"
python3 -m pytest -q tests/smoke/test_local_server_async_read.py
```
