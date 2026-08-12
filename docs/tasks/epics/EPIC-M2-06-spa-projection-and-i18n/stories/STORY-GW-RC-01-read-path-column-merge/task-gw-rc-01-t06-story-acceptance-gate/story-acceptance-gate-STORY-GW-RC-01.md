# Story acceptance gate — STORY-GW-RC-01

- **Story:** Read-path column merge (id/status/created_at)
- **Package:** `pkg-000030-20260619-gw-rc-01-read-path-column-merge.yaml`
- **Result:** PASS
- **Date:** 2026-06-19

## AC checklist (verbatim from backlog)

| AC | Status | Evidence |
|----|--------|----------|
| `GET /tallinn/issues` и `/{id}`: каждый issue имеет `id`, `status`, `created_at` из колонок | PASS | `test_http_list_get_merge_incomplete_payload` |
| При неполном `payload_json` (без id/status) ответ всё равно содержит `id`/`status` из колонок | PASS | `test_store_get_list_merge_incomplete_payload`; `test_m14_incomplete_payload_merge_columns` |
| Фильтр `?status=` работает по колонке (а не по payload) | PASS | `test_m13_status_filter_uses_column_not_payload`; HTTP + store status filter tests |
| Поведение идентично на Supabase/SQLite/InMemory | PASS | T02 mock contract; sqlite/memory parametrize in T05 |
| Тест-суит без регрессий; добавлен тест «seed неполного payload → есть id/status» | PASS | `489 passed in 15.64s` — live run 2026-06-19 |
| `builder_resolve_queue.py --verify` ok 6 paths | PASS | live run 2026-06-19 |

## Commands (live verification 2026-06-19)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_01_read_path_column_merge.py -q
cd doge-complaints-gateway && python3 -m pytest tests/ -q --ignore=tests/smoke --ignore=tests/integration
```
