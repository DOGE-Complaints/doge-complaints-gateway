## Task workspace — `task-m2-02-07-t09-gap33-04-sqlite-i18n-roundtrip-e2e`

- Story: [`../STORY-M2-02-07-multilingual-intake-contract-v2.md`](../STORY-M2-02-07-multilingual-intake-contract-v2.md)
- Decision Ref: [`../../../../../../analysis/audit-req33-multilingual-intake-v2-2026-05-15.md`](../../../../../../analysis/audit-req33-multilingual-intake-v2-2026-05-15.md) GAP-33-04

## Task: tests — SQLite round-trip for v2 i18n title/description

### Цель
E2E через SQLite: после `POST /intake/stories` в БД/репозитории сохранены `narrative_title` и `narrative_description` как dict `{et, ru, en}`.

### Факты из кода
1. Unit-тесты маппинга есть; сквозной SQLite round-trip для i18n dict — нет (GAP-33-04).
2. [`tests/test_db_backed_pipeline_e2e.py`](../../../../../../../tests/test_db_backed_pipeline_e2e.py) — fixture `client` + `intake_payload_simple`.

### Gap / Проблема
**GAP-33-04 (P2):** нет проверки persist/read i18n JSON колонок end-to-end.

### AC/DoD
- [x] (P2) Тест: intake v2 → `get_story` / SQL read → title/description dict совпадают с payload.
- [x] (P2) `narrative_session_language` сохранён.

### Где менять код
- [`tests/test_db_backed_pipeline_e2e.py`](../../../../../../../tests/test_db_backed_pipeline_e2e.py)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_db_backed_pipeline_e2e.py::test_sqlite_intake_v2_narrative_i18n_roundtrip -q
```
