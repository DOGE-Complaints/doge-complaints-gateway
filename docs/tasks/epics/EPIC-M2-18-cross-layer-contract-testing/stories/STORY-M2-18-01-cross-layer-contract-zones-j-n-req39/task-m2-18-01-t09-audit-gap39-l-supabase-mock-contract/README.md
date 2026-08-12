## Task workspace — `task-m2-18-01-t09-audit-gap39-l-supabase-mock-contract`

- Story: [`../STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md`](../STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md)
- Decision Ref: [`../../../../../../analysis/audit-req39-cross-layer-contract-testing-2026-05-18.md`](../../../../../../analysis/audit-req39-cross-layer-contract-testing-2026-05-18.md) §6 GAP-39-L-SUPA; Zone L

---
**Приоритет:** P1  
**Сложность:** M  
**Оценка времени:** ~2–4 ч  
**Статус:** ready  
**Wave:** audit override (`run_mode=story18_audit_req39_followup`)  
---

## Task: tests — offline mock contract for SupabaseIssueProjectionStore (Zone L)

### Цель
Добавить offline-покрытие `SupabaseIssueProjectionStore.list_projections()` через HTTP mock (`responses` / `httpretty`), без live Supabase.

### Почему это важно (риск)
Текущий Zone L contract parametrizes только InMemory + SQLite ([`test_issue_projection_store_contract.py`](../../../../../../../tests/test_issue_projection_store_contract.py)). Реализация в [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) ~L619–674 (PostgREST URL, status filter) не верифицируется offline.

### Факты из кода
1. REQ-39 §Zone L допускает live-only для Supabase story repo; projection store mock — рекомендованный audit path (Вариант A).
2. Аудит: сложность **HIGH** (mock setup); важность **MEDIUM**.

### Gap / Проблема
**AUDIT-GAP-39-L-SUPA:** `SupabaseIssueProjectionStore` excluded from parametrized contract file.

### AC/DoD
- [ ] (P0) Новый `tests/test_supabase_issue_projection_store_contract.py` с `@responses.activate` (или эквивалент).
- [ ] (P0) Assert корректный HTTP GET к `/rest/v1/doge_issues` и query params (e.g. `status=eq.PUBLISHED` when filtered).
- [ ] (P0) Mock response shape совместим с `filter_projection_rows` post-fetch path.
- [ ] (P1) Dev dependency для mock lib уже в project или добавить в `pyproject.toml` optional dev — только если отсутствует.
- [ ] (P0) Offline suite still green: `pytest tests/ --ignore=tests/integration -q`.

### Где менять код
- `tests/test_supabase_issue_projection_store_contract.py` (new)
- Опционально: [`pyproject.toml`](../../../../../../../pyproject.toml) dev deps

### Out of scope
- Live integration tests under `tests/integration/` (Вариант B аудита — отдельная ops-волна).
- Changing `pkg-000020`; parametrizing existing L file with live Supabase.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_supabase_issue_projection_store_contract.py
cd doge-complaints-gateway && python3 -m pytest tests/ --ignore=tests/integration -q --tb=no
```
