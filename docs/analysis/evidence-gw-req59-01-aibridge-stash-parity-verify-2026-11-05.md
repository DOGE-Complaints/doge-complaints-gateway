# Evidence — STORY-GW-REQ59-01 aibridge stash parity verify

- **Date:** 2026-11-05T12:10:10Z
- **Package:** pkg-000117
- **Story:** STORY-GW-REQ59-01
- **Nature:** verify-first · **Default Pass = no gateway product code change**
- **Product code changed this P3:** **no**
- **Result:** Parity **holds** (harness Present) · Live aibridge stash: **Unknown** (not executed this fence — no invent PASS)

## AC map

| AC | Verdict | Evidence |
|----|---------|----------|
| AC-GW-59-01 | PASS (code + harness) | Peer `STASH_PATH="/story-drafts"` · `execute_stash` · `parse_success_body` expects `data.draft_id` + `trace_id` · GW `handle_story_draft_create` → 201 + `draft_id` · suite `test_gw_draft_01_*` / openapi |
| AC-GW-59-02 | PASS | Create returns only `draft_id`; Story/issue only via `handle_story_draft_submit` → intake · `test_post_story_drafts_returns_draft_id_without_creating_story` |
| AC-GW-59-03 | PASS (no hard break) | No gap/decision needed — parity holds; no silent contract invent |
| AC-GW-59-04 | PASS | POST `_STORY_DRAFT_WRITE_DEPS` / service auth · GET/submit citizen deps · missing/wrong service → 401 (`test_post_story_drafts_requires_service_token` / `rejects_invalid_service_token`) |

## Code cites (gateway)

| Fact | Path |
|------|------|
| POST service-only | `asgi_app.py:368–375` `require_public_content_service_auth` · `_STORY_DRAFT_WRITE_DEPS` · `:685` `POST /story-drafts` |
| Create 201 + draft_id | `handlers.py:790–829` `handle_story_draft_create` · `data={"draft_id": …}` · status `201` · TTL `config.story_draft_ttl_seconds` / `STORY_DRAFT_TTL_SECONDS` |
| Repo save | `handlers.py:817` `repository.save_draft` · `StoryDraftRepository` |
| GET citizen | `asgi_app.py:378–398` / `:433` / `:717` |
| Submit citizen + verify gate | `asgi_app.py:401–430` / `:434` / `:734–751` · `handlers.py:965+` → `handle_story_intake` |

## Peer cites (aibridge · read-only)

| Fact | Path |
|------|------|
| Path | `doge-ai-bridge/src/aibridge/gateway.py:13` `STASH_PATH = "/story-drafts"` |
| Bearer | `:204–207` `GATEWAY_SERVICE_API_TOKEN` → `Authorization: Bearer …` |
| Success parse | `:123–143` `draft_id` + `trace_id` |
| Outcome 201 | `:154–158` → `GatewayOutcome.STASHED` |
| Stash ≠ published wording | `:20–22` `STASH_REPLY` |

## Harness (Present)

```text
.venv/bin/python -m pytest -q \
  tests/test_gw_draft_01_story_draft_stash_contract.py \
  tests/test_gw_draft_02_get_auth_contract.py \
  tests/test_gw_draft_02_story_draft_submit_contract.py \
  tests/test_openapi_runtime_compliance.py \
  -m "not live_integration"
→ 24 passed (14 + 10 across runs; draft_01+get=14; draft_02+openapi=10)
```

## Live

- Soft-depend G4 / live aibridge `execute_stash` against hosted gateway: **not run** this P3 → **Unknown** live (harness Present; no invent live PASS).

## Gap list

- **Empty** OPEN gaps for AC-01…04 under verify-first default Pass.
