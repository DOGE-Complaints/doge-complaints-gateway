## Task workspace — `task-gw-l10n-03-t08-decouple-label-miss-from-readiness`

- Story: [`../STORY-GW-L10N-03-label-miss-telemetry-sink.md`](../STORY-GW-L10N-03-label-miss-telemetry-sink.md)
- Depends on: T01 (table exists), T02–T03 (handler resilience Done)
- Decision Ref: [`../../../../../../analysis/audit-gw-l10n-03-label-miss-telemetry-2026-06-15.md`](../../../../../../analysis/audit-gw-l10n-03-label-miss-telemetry-2026-06-15.md) §3 G1, §2 R1; story AC «ошибки приёма не должны влиять на остальную систему»

---
**Priority:** P0  
**Complexity:** S  
**Estimate:** ~30 min  
**Status:** 🟢 Done  
**Wave:** audit override (`run_mode=gw_l10n_03_audit_followup`)  
**Skill declared:** python-pro  
---

## Task: fix — decouple `label_translation_misses` from global gateway readiness

### Цель
Исключить некритичную телеметрическую таблицу из `required_tables_ready()`, чтобы отсутствие миграции `label_translation_misses` на hosted Supabase **не** делало весь gateway not-ready (intake → 503) и не ломало integration-тест connectivity.

### Почему это важно (риск)
Story D-L10N-3 требует: телеметрия — некритичный путь; handler уже деградирует при сбое store ([`handlers.py:432-446`](../../../../../../../src/core/api/handlers.py#L432-L446)). Но `label_translation_misses` включена в обязательный readiness-набор ([`db_supabase.py:279`](../../../../../../../src/core/infrastructure/db_supabase.py#L279)) → `db_ready=False` ([`dependencies.py:73,79`](../../../../../../../src/core/api/dependencies.py#L73-L79)) → intake отклоняется 503 и падает [`test_supabase_dotenv_connectivity.py:92`](../../../../../../../tests/integration/supabase/test_supabase_dotenv_connectivity.py#L92) (audit G1/R1).

### Факты из кода
1. [`db_supabase.py:267-280`](../../../../../../../src/core/infrastructure/db_supabase.py#L267-L280) — `required_tables_ready()` включает `"label_translation_misses"` в `required` set.
2. [`dependencies.py:71-79`](../../../../../../../src/core/api/dependencies.py#L71-L79) — supabase branch: `db_checks["schema"] = health_db.required_tables_ready()`; `db_ready = all(db_checks.values())`.
3. [`test_supabase_dotenv_connectivity.py:92`](../../../../../../../tests/integration/supabase/test_supabase_dotenv_connectivity.py#L92) — `assert db.required_tables_ready() is True` (red до фикса, если миграция не применена на hosted).
4. [`test_gw_l10n_03_label_miss_telemetry.py:90`](../../../../../../../tests/test_gw_l10n_03_label_miss_telemetry.py#L90) — store failure → `202` + `accepted: false` (endpoint resilience уже есть; не ломать).

### Gap / Проблема
**G1 (audit):** некритичная телеметрия завязана на глобальную готовность gateway — инверсия story AC.  
**R1 (audit):** integration-тест Supabase падает из-за отсутствия таблицы в hosted project + её включения в required set.

### AC/DoD
- [x] (P0) Убрать `"label_translation_misses"` из `required_tables_ready()` required-set в [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py).
- [x] (P0) `required_tables_ready()` green на hosted Supabase **без** обязательной миграции телеметрии (закрывает R1).
- [x] (P0) Unit/regression: явная проверка, что telemetry table **не** входит в required set (mock или assertion на `required` frozenset/list).
- [x] (P1) `POST /telemetry/label-misses` по-прежнему деградирует при store fail — существующий тест `test_post_label_miss_store_failure_returns_202_degraded` green.
- [x] (P1) `python3 -m pytest -q tests/integration/supabase/test_supabase_dotenv_connectivity.py` green (при наличии `.env` creds) — 1 passed live 2026-06-15.

### Где менять код
- [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) — `required_tables_ready()` required set
- Опционально: [`tests/test_gw_l10n_03_label_miss_telemetry.py`](../../../../../../../tests/test_gw_l10n_03_label_miss_telemetry.py) или новый `tests/test_supabase_required_tables.py` — guard на состав required set

### Out of scope
- Новый pkg / смена [`gateway-active-package.current.yaml`](../../../../../../gateway-active-package.current.yaml)
- Применение миграции `20260615_1200_*` на hosted Supabase (ops)
- Rate-limit / anti-abuse
- Изменение handler resilience (T03 Done)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_l10n_03_label_miss_telemetry.py
cd doge-complaints-gateway && python3 -m pytest -q tests/integration/supabase/test_supabase_dotenv_connectivity.py
cd doge-complaints-gateway && python3 -m pytest -q --ignore=tests/integration --ignore=tests/smoke
```
