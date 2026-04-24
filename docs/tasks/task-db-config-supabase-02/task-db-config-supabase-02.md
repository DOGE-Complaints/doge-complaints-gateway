## Task: implement — strict supabase config contract

### Цель
Сделать fail-fast контракт конфигурации для режимов `in_memory/sqlite/supabase` с приоритетом production-safe для Supabase.

### Почему это важно (риск)
Неоднозначный backend selection приводит к ложной готовности и нестабильным runtime-сценариям.

### Факты из кода (Code Facts / SSOT)
1. `schema.py` уже содержит db/supabase поля, но режимы требуют более строгого fail-fast.
2. `example.env` описывает параметры, но не фиксирует жесткие runtime/test профили.
3. В DB-волне основной runtime шел через sqlite.

### Gap / Проблема
Контракт env и правила выбора backend не закрывают все конфликтные комбинации.

### AC/DoD
- [ ] (P0) Валидация env явно запрещает конфликтные backend комбинации.
- [ ] (P0) Для `DB_BACKEND=supabase` обязательны валидные supabase credentials.
- [ ] (P1) `example.env` синхронизирован с новым контрактом.
- [ ] (P1) Добавлены тесты на fail-fast сценарии.

### Где менять код
- `src/core/config/schema.py`
- `example.env`
- `tests/test_config_loading.py`

### План выполнения (Execution Plan)
1) Уточнить контракт. 2) Обновить env примеры. 3) Добавить негативные/позитивные config tests.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/test_config_loading.py -q
```
