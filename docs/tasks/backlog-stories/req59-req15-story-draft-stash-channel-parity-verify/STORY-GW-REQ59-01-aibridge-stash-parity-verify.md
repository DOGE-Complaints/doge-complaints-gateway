# STORY-GW-REQ59-01 — Aibridge stash parity verify (REQ15)

## Meta
- **Key:** `STORY-GW-REQ59-01-aibridge-stash-parity-verify`
- **Status:** 🔵 **Done (Awaiting Commits)** · P3 gate PASS 2026-11-05T12:10:10Z · verify-first · no product · [`pkg-000117`](../../gateway-active-packages/pkg-000117-20261105-gw-req59-01-aibridge-stash-parity-verify.yaml) · [pipeline](../../epics/EPIC-req59-req15-story-draft-stash-channel-parity-verify/stories/STORY-GW-REQ59-01-aibridge-stash-parity-verify/STORY-GW-REQ59-01-aibridge-stash-parity-verify.md) · [evidence](../../analysis/evidence-gw-req59-01-aibridge-stash-parity-verify-2026-11-05.md)
- **Пакет:** [`req59-req15-story-draft-stash-channel-parity-verify/`](./INDEX.md)
- **Parent REQ:** [`59-req15-story-draft-stash-channel-parity-verify.md`](../../../requirements/59-req15-story-draft-stash-channel-parity-verify.md)
- **Parent product:** REQ15 AC-08
- **Gap closure:** G6 first ([execution-order](../../../../../docs/analysis/req15-gap-closure-execution-order-2026-11-03.md)) → then SPA [`STORY-SPA-REQ15-01`](../../../../../spa-app/docs/tasks/backlog-stories/req15-story-submit-handoff-continuity-verify/STORY-SPA-REQ15-01-story-submit-handoff-continuity-verify.md)
- **Siblings:** aibridge REQ-11 · [`STORY-AIBRIDGE-56`](../../../../../doge-ai-bridge/docs/tasks/backlog-stories/req-11-req15-dual-confirm-gateway-submit-spa-handoff/STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify.md) · spa 25 / STORY-SPA-REQ15-01 · Keep [`story-draft-handoff`](../story-draft-handoff/INDEX.md)
- **Peer arch:** [`req15-dual-confirm-handoff`](../../../../../doge-ai-bridge/docs/architecture/req15-dual-confirm-handoff/)
- **Skill declared:** `python-pro` · soft `code-documenter`
- **Tech subtasks:** Present · Status **Done** (t01–t06) · epic folders Created P1.3
- **Emitted:** 2026-11-03 · **L2 intake:** 2026-11-05T11:46:32Z
- **Scaffolded / P1.3 APPLY:** 2026-11-05T12:01:41Z
- **P3 Done:** 2026-11-05T12:10:10Z · gate PASS · live Unknown · no product code
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

## Scope
- Verify Present `POST /story-drafts` remains handoff SSOT for **aibridge** client (service Bearer).
- Evidence: 201 + `draft_id`; stash ≠ published Story; auth boundaries unchanged unless explicit REQ.
- Gap list only if hard break found — no silent contract invent.

## Out of scope
- Interview/roles/telegram; sense-brief; redesign intake for fun.
- Implementing new stash fields without T1/operator lock.
- SPA handoff UX (sibling SPA-REQ15-01); aibridge FSM rewrite (peer 56 Done).

## Verified current state (code probe 2026-11-05)

| Fact | Evidence |
|------|----------|
| Keep stash lineage Done | [`STORY-GW-DRAFT-01`](../story-draft-handoff/STORY-GW-DRAFT-01-story-draft-stash.md) · [`STORY-GW-DRAFT-02`](../story-draft-handoff/STORY-GW-DRAFT-02-browser-submit-verification-gate.md) · [`STORY-GW-DRAFT-05`](../story-draft-handoff/STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md) |
| POST stash + service auth | [`asgi_app.py:375`](../../../../src/core/api/asgi_app.py) `_STORY_DRAFT_WRITE_DEPS` · [`:368`](../../../../src/core/api/asgi_app.py) `require_public_content_service_auth` · [`:685`](../../../../src/core/api/asgi_app.py) `POST /story-drafts` |
| Create → 201 + `draft_id` | [`handlers.py:790–829`](../../../../src/core/api/handlers.py) `handle_story_draft_create` · `data={"draft_id": …}` · status `201` |
| GET draft = citizen | [`asgi_app.py:378–398`](../../../../src/core/api/asgi_app.py) `require_story_draft_read_user` · [`:717`](../../../../src/core/api/asgi_app.py) `GET /story-drafts/{draft_id}` · [`handlers.py:841`](../../../../src/core/api/handlers.py) |
| Submit = citizen + verify gate | [`asgi_app.py:401–430`](../../../../src/core/api/asgi_app.py) `require_story_draft_submit_user` · [`:735–738`](../../../../src/core/api/asgi_app.py) · [`handlers.py:965`](../../../../src/core/api/handlers.py) `handle_story_draft_submit` → intake |
| Aibridge client | [`gateway.py:13`](../../../../../doge-ai-bridge/src/aibridge/gateway.py) `STASH_PATH="/story-drafts"` · [`:206`](../../../../../doge-ai-bridge/src/aibridge/gateway.py) `GATEWAY_SERVICE_API_TOKEN` · [`:209`](../../../../../doge-ai-bridge/src/aibridge/gateway.py) `execute_stash` · [`:123`](../../../../../doge-ai-bridge/src/aibridge/gateway.py) `parse_success_body` (`draft_id` + `trace_id`) · [`:118`](../../../../../doge-ai-bridge/src/aibridge/gateway.py) `build_continuation_url` |

REQ-59 P1.3 APPLY Done 2026-11-05T12:01:41Z — verify package · pipeline T01–T06 Todo · tip pkg-000117 · Await P2.

## L1.5 Ownership

| Rule | Owner |
|------|--------|
| Stash HTTP + service auth | gateway `asgi_app` / `handlers` / Keep GW-DRAFT-01 |
| Stash ≠ published Story | create returns only `draft_id`; Story/issue only via submit→intake (`handle_story_draft_submit`) |
| Aibridge client contract | peer `GatewayExecutor` (REQ-11 / STORY-56) — **client**; **server** owns stash |
| Auth boundary | POST = service Bearer; GET/submit = citizen Bearer (+ submit verification gate) |
| Continuation URL shape | aibridge `build_continuation_url` — SPA consumes (sibling SPA-REQ15) |

## Target / AC
- [x] **AC-GW-59-01:** Documented verify: stash 201 + `draft_id` works for aibridge client
- [x] **AC-GW-59-02:** Stash success still ≠ published Story
- [x] **AC-GW-59-03:** If break found: written gap + decision — no silent contract drift
- [x] **AC-GW-59-04:** Service vs citizen auth boundaries unchanged unless explicit REQ
- [x] Default Pass = **no gateway code change** if parity holds

## Technical subtasks (arch-bound; P3 Done)

| ID | Slug | Essence | Arch / AC | Touch (as-is) | OOS | Status |
|----|------|---------|-----------|---------------|-----|--------|
| **t01** | `task-gw-req59-01-t01-stash-path-inventory` | Inventory Present: route deps, handler 201/`draft_id`, repo save, TTL config | support AC-01/02 · GW-DRAFT-01 | `asgi_app.py` · `handlers.py` · DRAFT-01 | redesign intake | **Done** |
| **t02** | `task-gw-req59-01-t02-aibridge-client-contract-parity` | Parity vs aibridge: path `/story-drafts`, Bearer from config, success body `draft_id`+`trace_id`, outcome map | AC-GW-59-01 · peer arch `01-keep-pipe` | peer `gateway.py` + GW envelope | change aibridge | **Done** |
| **t03** | `task-gw-req59-01-t03-auth-boundary-service-vs-citizen` | POST service-only; GET/submit citizen; wrong/missing service → 401; citizen Bearer must not stash | AC-GW-59-04 | `_STORY_DRAFT_*_DEPS` · `require_*` | new auth modes | **Done** |
| **t04** | `task-gw-req59-01-t04-stash-neq-story-assert` | Evidence: after 201 stash, no Story/issue until submit; cite create vs `handle_story_draft_submit` | AC-GW-59-02 | `handlers.py` create/submit | SPA UI | **Done** |
| **t05** | `task-gw-req59-01-t05-evidence-or-gap-note` | Write evidence note under `doge-complaints-gateway/docs/analysis/` **или** gap+decision if hard break; default **no GW code change**. Live soft-depends G4; if live blocked → harness Present + **Unknown** live (no invent PASS) | AC-GW-59-01…03 | analysis note | silent contract invent | **Done** |
| **t06** | `task-gw-req59-01-t06-story-gate` | Gate checklist AC-GW-59-01…04; INDEX/status sync | package gate | story + INDEX | SPA-REQ15 implement | **Done** |

**Order:** t01 → t02 → t03 → t04 → t05 → t06.  
**Skill:** `python-pro` (path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`).

## Dependencies
- Soft: aibridge live stash client path (MVP smoke / G4).
- Soft: peer STORY-AIBRIDGE-56 Done (client Keep).
- Blocks (soft): SPA-REQ15-01 live `draft_id` evidence.
