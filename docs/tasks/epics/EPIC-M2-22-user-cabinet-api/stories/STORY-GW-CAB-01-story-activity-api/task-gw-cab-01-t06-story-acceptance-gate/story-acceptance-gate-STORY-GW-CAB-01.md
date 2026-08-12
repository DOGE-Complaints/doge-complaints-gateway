# Story acceptance gate — STORY-GW-CAB-01

- **Story:** Story Activity API (`GET /story-activity`)
- **Package:** `pkg-000052-20260713-gw-cab-01-story-activity-api.yaml`
- **Result:** PASS
- **Date:** 2026-07-13T09:59:00Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-1: GET /story-activity (browser Bearer) → 200 SuccessEnvelope с data.metrics + data.stories по MVP-контракту | PASS | T04 route `asgi_app.py`; T03 `StoryActivityService`; T05 `test_gw_cab_01_*` contract asserts; OpenAPI `SuccessEnvelope_StoryActivity` |
| AC-2: Author scoping: gateway форвардит Bearer в identity /me → sub → фильтр историй по автору | PASS | `_STORY_DRAFT_READ_DEPS` + `user_introspection.sub`; T02 `list_stories_by_submitter`; T05 `test_gw_cab_01_scoping_isolates_users` |
| AC-3: In scope: user-scoped read «мои истории + метрики»; author из /me | PASS | Handler read-only; metrics + stories list; no write path |
| AC-4: Вне scope: запись; пагинация; issue-детали | PASS | T05 `test_gw_cab_01_response_has_no_issue_details`; response rows = story_id/status/created_at only |

## Commands (live verification 2026-07-13)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_cab_01_story_activity_api.py -m "not live_integration"
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
