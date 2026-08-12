# Story acceptance gate — STORY-GW-L10N-02

- **Story:** `original_locale` в публичной проекции issue
- **Package:** `pkg-000028-20260603-gw-l10n-02-original-locale-in-public-projection.yaml`
- **Result:** PASS (re-verified)
- **Date:** 2026-06-15
- **Remediation:** Prior gate date `2026-05-29` was invalid (before `pkg-000028` `created_at` 2026-06-03 and dependency GW-L10N-01 gate 2026-06-15). Corrected per live verification run below.

## AC checklist (verbatim from backlog)

| AC | Status | Evidence |
|----|--------|----------|
| `GET /tallinn/issues` и `/{id}` возвращают `original_locale: string[]` | PASS | `tests/test_gw_l10n_02_original_locale.py::test_tallinn_list_and_get_return_original_locale` |
| Смешанный кластер: дедуп; стабильный порядок | PASS | `test_mixed_et_ru_cluster_produces_canonical_order`; `test_original_locale_from_languages_canonical_order_and_dedup` |
| Поле опускается когда язык неизвестен | PASS | `test_unknown_language_omits_original_locale_from_public_dict` |
| openapi/API_REFERENCE описывают поле | PASS | `openapi.yaml` L331–339 `IssueProjection.original_locale`; `API_REFERENCE.md` §7 |
| Тест-суит без регрессий | PASS | `457 passed in 15.07s` — live run 2026-06-15 UTC (`pytest tests/ -q --ignore=tests/smoke --ignore=tests/integration`) |
| `builder_resolve_queue.py --verify` ok 7 paths | PASS | pkg-000028 (live run 2026-06-15) |
| Audit G1 backfill assertion (T08) | PASS | `tests/test_reproject_issue_i18n.py::test_reproject_write_sets_original_locale_from_cluster_stories` (2026-06-15) |

## Commands (live verification 2026-06-15)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest tests/ -q --ignore=tests/smoke --ignore=tests/integration
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_l10n_02_original_locale.py tests/test_reproject_issue_i18n.py -q
```
