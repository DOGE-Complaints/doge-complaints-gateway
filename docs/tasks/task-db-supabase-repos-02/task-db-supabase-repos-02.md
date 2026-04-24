## Task: implement — supabase-native repositories and stores

### Цель
Перевести runtime persistence на supabase-native репозитории для stories, idempotency, embeddings и SPA projections без опоры на sqlite backend.

### Почему это важно (риск)
Текущая SQL-ветка остается sqlite-centric и не доказывает production готовность на Supabase/Postgres.

### Scope
Входит: supabase/postgres adapters, repository wiring, protocol compatibility.  
Не входит: финальный live integration test batch.

### Факты из кода (Code Facts / SSOT)
1. `providers.py` включает SQL-режим только для `DB_BACKEND=sqlite`.
2. `db_sqlite.py` реализует текущие SQL stores в sqlite формате.
3. DB e2e тест (`test_db_backed_pipeline_e2e.py`) запускается только на sqlite.

### Gap / Проблема
Нет runtime supabase-native repository слоя при `DB_BACKEND=supabase`.

### AC/DoD
- [ ] (P0) Реализованы supabase-native repositories для stories/idempotency.
- [ ] (P0) Реализованы supabase-native stores для story/projection embeddings и projections.
- [ ] (P0) `DB_BACKEND=supabase` использует новые adapters, а не sqlite/in-memory.
- [ ] (P1) Протоколы приложения сохраняют совместимость.

### Где менять код
- `src/core/infrastructure/`
- `src/core/application/services.py`
- `src/core/application/issue_create.py`

### План выполнения (Execution Plan)
1) Добавить supabase adapters. 2) Подключить провайдеры backend-switching. 3) Пройти contract/regression tests.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/test_config_loading.py tests/test_di_service_factory.py -q
```
