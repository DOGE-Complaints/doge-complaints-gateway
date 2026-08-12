# Story acceptance gate — STORY-GW-L10N-01

- **Story:** Сохранение реального мультиязычного контента в проекции
- **Package:** `pkg-000027-20260603-gw-l10n-01-projection-content-i18n-preservation.yaml`
- **Result:** PASS
- **Date:** 2026-06-15

## AC checklist (verbatim from backlog)

| AC | Status | Evidence |
|----|--------|----------|
| Различающиеся title/description/summary по локалям | PASS | `tests/test_gw_l10n_01_projection_i18n.py::test_dominant_story_distinct_title_locales_produce_distinct_projection_title` |
| Источник dominant + fallback | PASS | `extraction_policy.py` `i18n_text_from_optional_dict`; `test_dominant_story_missing_narrative_title_falls_back_to_promoted_title` |
| Manual POST сохраняет i18n-title | PASS | `issue_create.py` `_manual_title_i18n`; `test_manual_create_preserves_request_i18n_title` |
| Бэкфилл (re-project) | PASS | `scripts/reproject_issue_i18n.py --dry-run` / `--help` |
| Тест-суит без регрессий | PASS | `446 passed` unit suite 2026-06-15 |
| `builder_resolve_queue.py --verify` ok 6 paths | PASS | pkg-000027 |

## Commands

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest tests/ -q --ignore=tests/smoke --ignore=tests/integration
```
