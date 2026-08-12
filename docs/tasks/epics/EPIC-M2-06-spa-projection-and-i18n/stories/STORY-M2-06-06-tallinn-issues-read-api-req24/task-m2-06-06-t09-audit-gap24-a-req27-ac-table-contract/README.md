## Task workspace — `task-m2-06-06-t09-audit-gap24-a-req27-ac-table-contract`

- Story: [`../STORY-M2-06-06-tallinn-issues-read-api-req24.md`](../STORY-M2-06-06-tallinn-issues-read-api-req24.md)
- Decision Ref: [`../../../../../../requirements/27-doge-issue-domain-rename.md`](../../../../../../requirements/27-doge-issue-domain-rename.md) (decision 2026-05-05); [`../../../../../../analysis/audit-req24-tallinn-issues-api-2026-05-17.md`](../../../../../../analysis/audit-req24-tallinn-issues-api-2026-05-17.md) §6 GAP-A, GAP-C
- Supersedes: audit proposal to rename `doge_issues` → `tallinn_issues_projections`

---
**Приоритет:** P0  
**Сложность:** S  
**Оценка времени:** ~1–2 ч  
**Статус:** done  
**Wave:** audit override (`run_mode=story06_06_audit_req24_followup`)  
---

## Task: tests + docs — REQ-27 AC-1/AC-2 table contract (no DDL rename)

### Цель
Формально закрыть REQ-24 AC-1 и AC-2 в терминах REQ-27: persistence table **`doge_issues`** — финальное архитектурное имя; DDL rename **не** выполняется.

### Почему это важно (риск)
Внешний аудит пометил AC-1/AC-2 как OPEN из-за устаревшего текста REQ-24 §2.1 и отсутствия dedicated write-path теста. Без явного закрытия остаётся ложная уверенность, что нужен rename в `tallinn_issues_projections`.

### Факты из кода
1. [`db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py) — `CREATE TABLE IF NOT EXISTS doge_issues`; read SQL `FROM doge_issues`.
2. [`test_req24_tallinn_issues_read_api.py`](../../../../../../../tests/test_req24_tallinn_issues_read_api.py) — `test_req24_ac1_sqlite_doge_issues_table_exists` уже asserts `doge_issues` (корректен).
3. Write-path: `POST /intake/stories` → cluster → `IssueCreateService._create_issue` → `issue_projection_store.save_projection` (тот же store/backend).
4. STORY-M2-06-06 Product decisions: REQ-27 supersedes REQ-24 §2.1.

### Gap / Проблема
- **AUDIT-GAP-24-A:** аудит предлагал rename; **отклонено** — REQ-27 decision 2026-05-05.
- **AUDIT-GAP-24-C:** AC-1 тест уже верен; merge в этот таск.
- **AC-2:** нет `test_req24_ac2_write_path_uses_doge_issues`.

### AC/DoD
- [ ] (P0) **AC-1:** без изменений DDL/runtime; `test_req24_ac1_sqlite_doge_issues_table_exists` green.
- [ ] (P0) **AC-2:** новый `test_req24_ac2_write_path_uses_doge_issues`: `POST /intake/stories` с `CLUSTER_MIN_SIZE=1` и `CLUSTER_READINESS_THRESHOLD=1` (как client fixture в req24 tests); `process_all_pending()`; assert запись в projection store — без ошибки `no such table: tallinn_issues_projections`.
- [ ] (P0) [`24-tallinn-issues-read-api.md`](../../../../../../requirements/24-tallinn-issues-read-api.md) §2.1 и cascade step 1: явная **superseded**-заметка (REQ-27, 2026-05-05); устаревшие фрагменты с `tallinn_issues_projections` в §3.2–3.4 / §6 step 1 → `doge_issues` или deprecated inline.
- [ ] (P1) [`audit-req24-tallinn-issues-api-2026-05-17.md`](../../../../../../analysis/audit-req24-tallinn-issues-api-2026-05-17.md) §6: абзац Resolution — GAP-A/C closed per REQ-27.
- [ ] (P1) `acceptance-verification-m2-06-06-t09.md` + `BULLRUN-PHASE-LOG.md`.

### Где менять код
- [`tests/test_req24_tallinn_issues_read_api.py`](../../../../../../../tests/test_req24_tallinn_issues_read_api.py)
- [`docs/requirements/24-tallinn-issues-read-api.md`](../../../../../../requirements/24-tallinn-issues-read-api.md) (docs only)

### Out of scope
- DDL rename / Supabase migration `doge_issues` → `tallinn_issues_projections`
- `db_sqlite.py`, `db_supabase.py`, `repositories.py` runtime changes (unless test-only helpers)
- `pkg-000019` YAML changes

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_req24_tallinn_issues_read_api.py::test_req24_ac1_sqlite_doge_issues_table_exists tests/test_req24_tallinn_issues_read_api.py::test_req24_ac2_write_path_uses_doge_issues -q
```
