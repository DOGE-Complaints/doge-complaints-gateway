## Task workspace — `task-m2-18-05-t23-audit-gap41-02-supabase-secret-naming-docs`

- Story: [`../STORY-M2-18-05-live-integration-ci-req41.md`](../STORY-M2-18-05-live-integration-ci-req41.md)
- Decision Ref: [`../../../../../../analysis/audit-req41-production-coverage-target-state-2026-05-18.md`](../../../../../../analysis/audit-req41-production-coverage-target-state-2026-05-18.md) §7, §9 GAP-AUDIT-REQ41-02; [`../../../../../../requirements/41-testing-production-coverage-target-state.md`](../../../../../../requirements/41-testing-production-coverage-target-state.md) §7

---
**Приоритет:** P2  
**Сложность:** XS  
**Оценка времени:** ~15 мин  
**Статус:** Done  
**Wave:** audit override (`run_mode=story18_audit_req41_followup`)  
---

## Task: docs — align REQ-41 §7 GitHub Secret name with integration-live workflow

### Цель
Устранить расхождение имён: workflow ожидает GitHub Secret `SUPABASE_TEST_SERVICE_ROLE_KEY` → env `SUPABASE_TEST_SERVICE_ROLE`; REQ-41 §7 документирует secret как `SUPABASE_TEST_SERVICE_ROLE`.

### Почему это важно (риск)
Оператор может создать secret с неверным именем в GitHub → live CI stage не получит credentials (аудит §7, §9).

### Факты из кода
1. [`.github/workflows/integration-live.yml`](../../../../../../../.github/workflows/integration-live.yml) L5, L31 — `secrets.SUPABASE_TEST_SERVICE_ROLE_KEY` → env `SUPABASE_TEST_SERVICE_ROLE`.
2. [`41-testing-production-coverage-target-state.md`](../../../../../../requirements/41-testing-production-coverage-target-state.md) L260 — secret как `SUPABASE_TEST_SERVICE_ROLE` (расхождение).
3. [`13-testing-and-quality-architecture.md`](../../../../../../solution%20architecture/13-testing-and-quality-architecture.md) L249 — уже согласован с workflow (`SUPABASE_TEST_SERVICE_ROLE_KEY`).

### Gap / Проблема
**GAP-AUDIT-REQ41-02:** minor naming mismatch REQ-41 §7 vs workflow; functionally workflow корректен.

### AC/DoD
- [x] (P0) REQ-41 §7 / таблица secrets: GitHub Secret = `SUPABASE_TEST_SERVICE_ROLE_KEY`, runner env var = `SUPABASE_TEST_SERVICE_ROLE`.
- [x] (P1) Cross-link в header [`.github/workflows/integration-live.yml`](../../../../../../../.github/workflows/integration-live.yml) → REQ-41 §7.

### Acceptance
- [`acceptance-verification-m2-18-05-t23.md`](./acceptance-verification-m2-18-05-t23.md) — PASS (2026-05-19)

### Где менять (P5)
- Primary: [`docs/requirements/41-testing-production-coverage-target-state.md`](../../../../../../requirements/41-testing-production-coverage-target-state.md) §7.
- Опционально: comment-only в [`integration-live.yml`](../../../../../../../.github/workflows/integration-live.yml).

### Out of scope
- Переименование существующего secret в GitHub org.
- Смена env var в тестах (`SUPABASE_TEST_SERVICE_ROLE` остаётся).
- Переименование workflow secret reference (workflow уже корректен).

### Команды проверки
```bash
# Docs-only — grep consistency after edit:
rg 'SUPABASE_TEST_SERVICE_ROLE' doge-complaints-gateway/docs/requirements/41-testing-production-coverage-target-state.md
rg 'SUPABASE_TEST_SERVICE_ROLE_KEY' doge-complaints-gateway/.github/workflows/integration-live.yml
```
