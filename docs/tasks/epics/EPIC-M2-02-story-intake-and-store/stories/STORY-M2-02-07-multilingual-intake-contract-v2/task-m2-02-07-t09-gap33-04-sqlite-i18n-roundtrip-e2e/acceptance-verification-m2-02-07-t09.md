# Acceptance verification — T09 (GAP-33-04)

| AC | Код / тест | Статус |
|----|------------|--------|
| SQLite round-trip title/description dict | `test_sqlite_intake_v2_narrative_i18n_roundtrip` | pass |
| `narrative_session_language` persisted | same test | pass |

Команда:
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_db_backed_pipeline_e2e.py::test_sqlite_intake_v2_narrative_i18n_roundtrip -q
```
