## Task: implement — RLS/policy layer for exposed DB paths

### Цель
Ввести явный policy слой (RLS + access patterns) для данных, доступных через Supabase exposed surface.

### Почему это важно (риск)
Без RLS риск несанкционированного чтения/записи при расширении API поверхности и интеграций.

### Scope
Входит: enable RLS, policy SQL, policy verification tests.
Не входит: frontend auth flows.

### Факты из кода (Code Facts / SSOT)
1. В анализе зафиксирован `GAP-DB-007` (нет RLS/policies в текущем core runtime репозитории).
2. План target-state требует RLS для exposed access patterns.
3. Сейчас runtime не имеет DB security policy слоя.

### Gap / Проблема
`GAP-DB-007`: отсутствует декларативный security policy уровень.

### Decision Points
- **PM decision:** какие data access сценарии обязательны для demo.
- **CTO decision:** least-privilege и policy-by-contract вместо широких grants.
- **Options A/B:** permissive baseline vs strict default deny + explicit allow.
- **Recommendation:** strict default deny + explicit allow policies.

### AC/DoD
- [ ] (P0) Включен RLS для целевых exposed таблиц.
- [ ] (P0) Реализованы явные policies по access patterns.
- [ ] (P1) Добавлены policy verification tests.
- [ ] (P1) Зафиксирован security runbook для проверки policies.

### Где менять код
- DB migrations/policy SQL
- tests (security/policy verification)
- docs/analysis and runtime security docs

### План выполнения (Execution Plan)
1) Сформировать access matrix. 2) Реализовать RLS/policies. 3) Написать verification tests. 4) Обновить runbook.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
# policy verification tests
```
