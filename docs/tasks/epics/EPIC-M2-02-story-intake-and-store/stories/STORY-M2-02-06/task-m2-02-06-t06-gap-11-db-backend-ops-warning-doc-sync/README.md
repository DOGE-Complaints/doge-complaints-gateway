## Task workspace — `task-m2-02-06-t06-gap-11-db-backend-ops-warning-doc-sync`

- Story: [`../STORY-M2-02-06-data-model-registry-section-16-followup.md`](../STORY-M2-02-06-data-model-registry-section-16-followup.md)
- Decision Ref: [`../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md`](../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md) — §16 слой 4, **GAP-11** (закрыт: §16 + `startup.db_backend_in_memory` WARNING + тест дефолта)
- Cross-epic: [`task-m2-09-05-t02-gap-trace-00b-db-backend-supabase`](../../../../EPIC-M2-09-security-config-observability/stories/STORY-M2-09-05/task-m2-09-05-t02-gap-trace-00b-db-backend-supabase/README.md) — Railway `DB_BACKEND=supabase`, не дублировать полный объём.

## Task: implement / data — GAP-11: дефолт `in_memory`, предупреждение при старте, синхронизация §16

### Цель
Свести к единому SSOT: (1) ops — явный `DB_BACKEND=supabase` в деплое; (2) runtime — заметное предупреждение при старте API с `in_memory` в профиле, близком к pilot/production; (3) анализ §16 — строка верификации отражает фактические тесты и дефолт `EnvSpec`.

### Факты из кода
1) `DB_BACKEND` default `in_memory` — [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py).
2) Регресс дефолта — [`tests/test_config_loading.py`](../../../../../../../tests/test_config_loading.py) (`test_db_backend_env_default_matches_schema`).

### Gap / Проблема
Риск «HTTP 200, база пуста»; §16 всё ещё утверждает отсутствие unit-теста — **дрейф документации** относительно кода.

### AC/DoD
- [x] (P0) §16 GAP-11: статус и ссылка на `test_db_backend_env_default_matches_schema` + startup warning.
- [x] (P1) `asgi_app.py`: `logging.warning("startup.db_backend_in_memory", ...)` при `db_backend == in_memory`; узкий автотест на лог startup не добавлялся (достаточно регрессии дефолта + §16).
- [x] (P1) Runbook: без дублирования M2-09-05 T02 — в §16 зафиксирована отсылка к факту кода.

### Где менять код
- [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py)
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) или точка сборки DI, где известен `AppConfig`
- [`docs/runtime-docs/server-env-quickstart.md`](../../../../../../../docs/runtime-docs/server-env-quickstart.md) при необходимости
- [`docs/analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md`](../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md)

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_config_loading.py
```

### Артефакты процесса (`task-execution-process.md`)
- [`BULLRUN-PHASE-LOG.md`](./BULLRUN-PHASE-LOG.md)
- [`implementation-plan-m2-02-06-t06.md`](./implementation-plan-m2-02-06-t06.md)
- [`acceptance-verification-m2-02-06-t06.md`](./acceptance-verification-m2-02-06-t06.md)
- [`retrospective-m2-02-06-t06-full.md`](./retrospective-m2-02-06-t06-full.md)
