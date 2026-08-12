# Acceptance Verification — TASK-DB-CONFIG-01

- [ ] `AppConfig` содержит DB/Supabase runtime поля.
- [ ] env-контракт валидируется fail-fast.
- [ ] Readiness учитывает DB режим.
- [ ] PM gate: DB режим включается предсказуемо для demo.
- [ ] CTO gate: нет скрытых fallback/неявных default для критичных DB переменных.
