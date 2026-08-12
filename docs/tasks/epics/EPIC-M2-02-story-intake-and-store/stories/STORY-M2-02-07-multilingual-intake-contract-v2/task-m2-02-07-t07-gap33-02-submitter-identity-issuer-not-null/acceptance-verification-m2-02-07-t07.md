# Acceptance verification — T07 (GAP-33-02)

| AC | Код / тест | Статус |
|----|------------|--------|
| Bootstrap NOT NULL | `000_full_init.sql` L12 | pass |
| Migration backfill + NOT NULL | `20260515_1200_submitter_identity_issuer_not_null.sql` | pass |
| SQLite fresh schema NOT NULL | `db_sqlite.py` CREATE TABLE | pass |

Команды:
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_story_intake_contract.py tests/test_db_backed_pipeline_e2e.py::test_sqlite_intake_v2_narrative_i18n_roundtrip -q
```
