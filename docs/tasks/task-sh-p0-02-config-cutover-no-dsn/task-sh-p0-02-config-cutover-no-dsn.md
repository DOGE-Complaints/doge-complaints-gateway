## Task: implement — Supabase config cutover without DATABASE_URL

Key: TASK-SH-P0-02  
Priority: P0  
Status: Todo  
Closes: SH-CONFIG-HTTP-01  
Supersedes: TASK-DB-CONFIG-SUPABASE-02  
Decision Ref: `docs/analysis/story-first-supabase-verification-report.md`

### Goal
Сделать `DB_BACKEND='supabase'` полностью HTTP-native: обязательны только `SUPABASE_URL` и `SUPABASE_SERVICE_ROLE`.

### Code facts
1. `src/core/config/schema.py` требует `DATABASE_URL` для `DB_BACKEND='supabase'`.
2. `SUPABASE_URL/SUPABASE_SERVICE_ROLE` уже валидируются, но не являются самодостаточным контрактом.
3. `providers.py` полагается на `database_url` для supabase backend ветки.

### AC/DoD
- [ ] Для `DB_BACKEND='supabase'` `DATABASE_URL` больше не обязателен.
- [ ] Конфликтные env-сценарии валидируются fail-fast.
- [ ] Обновлены tests на загрузку и backend-switching.

### Verification commands
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/test_config_loading.py tests/test_db_backend_switching.py -q
rg -n "DATABASE_URL.*supabase|SUPABASE_URL|SUPABASE_SERVICE_ROLE" src/core/config/schema.py
```
