# Story acceptance gate — STORY-GW-CAB-02

- **Story:** Current draft discovery (`GET /story-drafts/current`)
- **Package:** `pkg-000053-20260714-gw-cab-02-current-draft-discovery.yaml`
- **Result:** PASS
- **Date:** 2026-07-14T10:31:35Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| `GET /story-drafts/current` под browser-Bearer возвращает `{draft_id,last_edited_at}` последнего непросроченного черновика юзера (D-CAB02-3) или `{data: null}` | PASS | T04 route `asgi_app.py`; T05 `test_gw_cab_02_association_on_read_enables_current`, `test_gw_cab_02_current_null_when_no_pending_draft`; OpenAPI `SuccessEnvelope_StoryDraftCurrent` |
| Ассоциация `draft_id→sub` пишется на `GET /story-drafts/{id}` под сессией; **кросс-девайс** (другой браузер того же юзера находит черновик) | PASS | T03 `handle_story_draft_get` + `set_owner`; T05 `test_gw_cab_02_cross_device_current_without_second_read` |
| Изоляция: юзер не видит чужой pending-черновик (owner-scoped) — доказано тестом | PASS | T05 `test_gw_cab_02_isolation_user_b_does_not_see_user_a_draft` |
| Просроченный (`expires_at<=now`) и уже засабмиченный (`delete_draft`) черновик в `current` не попадают | PASS | T05 `test_gw_cab_02_expired_draft_excluded_from_current`, `test_gw_cab_02_submitted_draft_excluded_from_current`, `test_gw_cab_02_manual_expired_association_excluded` |
| `last_edited_at` = `updated_at` (сейчас `= created_at`); поле готово к будущему трекингу правок | PASS | T01 `StoryDraftRecord.updated_at`; T05 `test_gw_cab_02_last_edited_at_equals_updated_at` |
| Full offline suite (`-m "not live_integration"`) green | PASS | 588 passed 2026-07-14 |

## Commands (live verification 2026-07-14)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_cab_02_current_draft_discovery.py -m "not live_integration"
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
