# Story acceptance gate — STORY-GW-RC-04

- **Story:** Колоночная модель проекции (удаление `payload_json`)
- **Package:** `pkg-000033-20260619-gw-rc-04-columnar-model-migration.yaml`
- **Result:** PASS
- **Date:** 2026-06-19

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| ADR зафиксировал представление i18n/geo (jsonb vs explode) и судьбу вьюхи. | PASS | T01 `adr-column-schema-d-rc-5.md` |
| Внешняя форма ответа issue идентична до/после (контракт-тесты зелёные). | PASS | `test_gw_rc_03_contract_guarantee.py`, `test_supabase_issue_projection_store_contract.py`; T08 |
| `payload_json` удалён; данные перенесены без потерь. | PASS | T07 migrations + SQLite columnar migration; no `payload_json` in `src/` |
| Фильтры/сортировка работают по колонкам/jsonb; 3 бэкенда согласованы. | PASS | T04–T05 `columnar_storage.py` + store parity |
| Тест-суит без регрессий. | PASS | `509 passed in 15.07s` — live run 2026-06-19 |

## Commands (live verification 2026-06-19)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest --ignore=tests/integration --ignore=tests/smoke -q
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
