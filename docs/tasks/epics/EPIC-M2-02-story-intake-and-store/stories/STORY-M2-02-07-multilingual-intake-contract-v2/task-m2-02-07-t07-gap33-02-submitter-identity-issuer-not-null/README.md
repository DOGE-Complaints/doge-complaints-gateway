## Task workspace — `task-m2-02-07-t07-gap33-02-submitter-identity-issuer-not-null`

- Story: [`../STORY-M2-02-07-multilingual-intake-contract-v2.md`](../STORY-M2-02-07-multilingual-intake-contract-v2.md)
- Decision Ref: [`../../../../../../analysis/audit-req33-multilingual-intake-v2-2026-05-15.md`](../../../../../../analysis/audit-req33-multilingual-intake-v2-2026-05-15.md) GAP-33-02; REQ-33 §2.3 (eID gate)

## Task: implement — `submitter_identity_issuer` NOT NULL in Supabase schema

### Цель
Закрыть обход eID gate на уровне БД: `submitter_identity_issuer` обязателен в bootstrap и hosted migration (backfill NULL → `legacy-unknown`).

### Факты из кода
1. [`supabase/bootstrap/000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql) L12: `submitter_identity_issuer text` (nullable).
2. Intake enforce'ит issuer; прямой INSERT/upsert может оставить NULL → `StoryRecord` с `""` при чтении.

### Gap / Проблема
**GAP-33-02 (P1):** DB не отражает обязательность поля из REQ-33 §2.3.

### AC/DoD
- [x] (P1) Bootstrap: `submitter_identity_issuer text not null`.
- [x] (P1) Migration `20260515_*`: `UPDATE … WHERE submitter_identity_issuer IS NULL` + `ALTER COLUMN … SET NOT NULL`.
- [x] (P2) Fresh SQLite `CREATE TABLE` в `db_sqlite.py` — `submitter_identity_issuer TEXT NOT NULL` для новых БД.

### Где менять код
- [`supabase/bootstrap/000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql)
- `supabase/migrations/20260515_*_submitter_identity_issuer_not_null.sql` (новый)
- [`src/core/infrastructure/db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py) (CREATE TABLE)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_supabase_bootstrap_schema.py tests/test_story_intake_contract.py -q --tb=short
```
