## Task: test — Unit and mock coverage for Supabase HTTP adapters

Key: TASK-SH-P2-01  
Priority: P2  
Status: Todo  
Closes: SH-TEST-HTTP-UNIT-01  
Decision Ref: `docs/tasks/task-test-unit-infra-config-01/task-test-unit-infra-config-01.md`

### Goal
Добавить полный unit/mock coverage для транспортного и репозиторного HTTP слоя.

### AC/DoD
- [ ] Покрыты timeout/auth/4xx/5xx/retry path.
- [ ] Покрыта семантика upsert/list/get для HTTP repositories.
- [ ] Покрыты ветки fallback/error mapping в приложение.

### Verification commands
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests -k "supabase and http and unit" -q
```
