# Story acceptance gate — STORY-GW-RC-02

- **Story:** Type canonical on read (legacy lowercase)
- **Package:** `pkg-000031-20260529-gw-rc-02-type-canonical-on-read.yaml`
- **Result:** PASS
- **Date:** 2026-06-19

## AC checklist (verbatim from backlog)

| AC | Status | Evidence |
|----|--------|----------|
| `GET /tallinn/issues` и `/{id}` отдают `type` в каноне даже для legacy строчного значения | PASS | `test_gw_rc_02_type_canonical_on_read.py` store + HTTP |
| Фильтр `?type=` и i18n типа на фронте работают на live-данных (бэк гарантирует канон) | PASS | `test_type_filter_matches_legacy_lowercase_payload`; HTTP `?type=IMPROVEMENT` tests |
| Поведение для неизвестного `type` определено и покрыто тестом | PASS | default `IMPROVEMENT` + `unknown_issue_types.jsonl` telemetry |
| Тест-суит без регрессий | PASS | `503 passed in 16.04s` — live run 2026-06-19 |
| `builder_resolve_queue.py --verify` ok 6 paths | PASS | live run 2026-06-19 |

## Commands (live verification 2026-06-19)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_02_type_canonical_on_read.py -q
cd doge-complaints-gateway && python3 -m pytest --ignore=tests/integration --ignore=tests/smoke -q
```
