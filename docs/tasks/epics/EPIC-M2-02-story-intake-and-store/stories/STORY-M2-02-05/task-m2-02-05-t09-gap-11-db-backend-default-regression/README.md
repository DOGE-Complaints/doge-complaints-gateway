## Task workspace — `task-m2-02-05-t09-gap-11-db-backend-default-regression`

- Story: [`../STORY-M2-02-05-supabase-bootstrap-schema-parity.md`](../STORY-M2-02-05-supabase-bootstrap-schema-parity.md)
- Decision Ref: [`../../../../../../analysis/implementation-report-STORY-M2-02-05-bootstrap-parity-2026-05-10.md`](../../../../../../analysis/implementation-report-STORY-M2-02-05-bootstrap-parity-2026-05-10.md) (§5.5)
- **cross_epic_ref (ops / env):** [`../../../../EPIC-M2-09-security-config-observability/stories/STORY-M2-09-05/task-m2-09-05-t02-gap-trace-00b-db-backend-supabase/README.md`](../../../../EPIC-M2-09-security-config-observability/stories/STORY-M2-09-05/task-m2-09-05-t02-gap-trace-00b-db-backend-supabase/README.md) — операционное закрытие `DB_BACKEND=supabase` и доказательства окружения; **не дублировать** полный объём T02.

## Task: tests — регрессия дефолта `DB_BACKEND` (документированный риск §5.5)

### Цель
Зафиксировать §5.5: `EnvSpec` для `DB_BACKEND` в [`src/core/config/schema.py`](../../../../../../src/core/config/schema.py) имеет `default="in_memory"` (строки ~124–128); смена дефолта не должна проходить незамеченной.

### Факты из кода
1) [`tests/test_config_loading.py`](../../../../../../tests/test_config_loading.py) — `test_load_config_demo_defaults` уже assert-ит `config.db_backend == "in_memory"` (строка ~24) при демо-профиле.
2) Схема env: [`src/core/config/schema.py`](../../../../../../src/core/config/schema.py) — `DB_BACKEND` `default="in_memory"`.

### Gap / Проблема
§5.5: нет **выделенного** теста именно на дефолт env-спеки при отсутствии переменной `DB_BACKEND` (частично перекрыто demo-тестом — в README зафиксировать и при необходимости добавить узкий тест).

### AC/DoD
- [ ] (P1) Либо добавить `test_db_backend_env_default_matches_schema` (минимальный env + отсутствие `DB_BACKEND` → `in_memory`), либо явно задокументировать в этом README и в §5.5 отчёта, что `test_load_config_demo_defaults` является каноническим регрессом, с цитатой строк.
- [ ] (P1) В README оставить `cross_epic_ref` на M2-09-05 T02 для ops-подтверждения Supabase.

### Где менять код
- [`doge-complaints-gateway/tests/test_config_loading.py`](../../../../../../tests/test_config_loading.py)
- Только ссылка: [`src/core/config/schema.py`](../../../../../../src/core/config/schema.py)

### План выполнения
1. Сравнить с §5.5 — избежать дублирования assert-ов.
2. Добавить узкий тест при пробеле покрытия.

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_config_loading.py
```
