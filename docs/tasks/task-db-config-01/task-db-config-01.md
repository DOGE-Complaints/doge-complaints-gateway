## Task: implement — DB/Supabase config contract + readiness

### Цель
Расширить `AppConfig` DB/Supabase параметрами и добавить readiness-проверки соединения/совместимости.

### Почему это важно (риск)
Без явного config-контракта DB интеграция будет неуправляемой и хрупкой в deploy.

### Scope
Входит: DB env contract, валидация, readiness hooks.
Не входит: бизнес-логика репозиториев.

### Факты из кода (Code Facts / SSOT)
1. В `src/core/config/schema.py` сейчас нет DB/Supabase полей.
2. `example.env` содержит Supabase переменные, но runtime их не использует.
3. `providers.py` поднимает только in-memory реализации.

### Gap / Проблема
`GAP-DB-003`: нет runtime DB/Supabase config контракта.

### Decision Points
- **PM decision:** минимальный набор переменных для demo-перехода.
- **CTO decision:** fail-fast валидация + прозрачные ошибки конфигурации.
- **Options A/B:** мягкая optional конфигурация vs strict profile-based.
- **Recommendation:** strict профильный контракт для DB режима.

### AC/DoD
- [ ] (P0) Добавлены DB/Supabase параметры в `AppConfig`.
- [ ] (P0) Добавлена валидация env-контракта.
- [ ] (P1) Readiness сигнал отражает DB connectivity/migration compatibility.
- [ ] (P1) Обновлен `example.env` и runtime docs.

### Где менять код
- `src/core/config/schema.py`
- `src/core/infrastructure/providers.py`
- `docs/runtime-docs/server-env-quickstart.md`
- `example.env`

### План выполнения (Execution Plan)
1) Расширить config schema. 2) Подключить providers/readiness. 3) Обновить docs/env contract. 4) Добавить тесты.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/test_config_loading.py -q
```
