## Task workspace — `task-m2-02-06-t10-gap-11-railway-db-backend-supabase-env`

- Story: [`../STORY-M2-02-06-data-model-registry-section-16-followup.md`](../STORY-M2-02-06-data-model-registry-section-16-followup.md)
- Decision Ref: [`../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md`](../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md) — **«Незакрытые хвосты — финальный прогон»**; §16 **GAP-11**
- Cross: [`task-m2-09-05-t02-gap-trace-00b-db-backend-supabase`](../../../../EPIC-M2-09-security-config-observability/stories/STORY-M2-09-05/task-m2-09-05-t02-gap-trace-00b-db-backend-supabase/README.md) — полный Railway runbook не дублировать.

## Task: data — Railway: явный `DB_BACKEND=supabase` в production

### Цель
Исключить сценарий «HTTP 200, база пуста»: в prod окружении переменная **`DB_BACKEND=supabase`** должна быть задана явно; дефолт `in_memory` в коде намеренно сохранён (`tests/test_config_loading.py`).

### Факты из кода
1. Предупреждение при старте: [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) — `startup.db_backend_in_memory` при `db_backend == "in_memory"`.
2. Регресс дефолта: [`tests/test_config_loading.py`](../../../../../../../tests/test_config_loading.py).

### Gap / Проблема
Конфигурация Railway живёт вне репозитория; закрытие — ops-действие + фиксация в таске.

### AC/DoD
- [ ] (P0) Чеклист: Railway dashboard → service → Variables → `DB_BACKEND=supabase` (и наличие `SUPABASE_URL` + service role, если используется HTTP backend).
- [ ] (P1) После деплоя: в логах старта **нет** `startup.db_backend_in_memory` (или ожидаемое поведение задокументировано для staging).
- [ ] (P2) Follow-up: жёсткий FAIL в dotenv-тесте при `in_memory` + live — отдельное согласование (см. Decision Ref, системные причины).

### Где менять
- Railway Variables; опционально одна строка в существующем runtime runbook со ссылкой на этот README.

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_config_loading.py::test_db_backend_env_default_matches_schema
```
