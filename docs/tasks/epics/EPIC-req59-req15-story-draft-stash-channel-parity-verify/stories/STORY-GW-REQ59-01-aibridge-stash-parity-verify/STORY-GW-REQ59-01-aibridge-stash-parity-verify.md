# STORY-GW-REQ59-01 — Aibridge stash parity verify (REQ15)

## Meta
- **Key:** `STORY-GW-REQ59-01-aibridge-stash-parity-verify`
- **Parent Epic:** [`../../../EPIC-req59-req15-story-draft-stash-channel-parity-verify.md`](../../../EPIC-req59-req15-story-draft-stash-channel-parity-verify.md)
- **Пакет:** [`req59-req15-story-draft-stash-channel-parity-verify/`](../../../../backlog-stories/req59-req15-story-draft-stash-channel-parity-verify/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) · P3 gate PASS 2026-11-05T12:10:10Z · **verify-first** · no product code
- **Тип:** verify / parity (REQ15 AC-08 · G6)
- **source:** [`../../../../backlog-stories/req59-req15-story-draft-stash-channel-parity-verify/STORY-GW-REQ59-01-aibridge-stash-parity-verify.md`](../../../../backlog-stories/req59-req15-story-draft-stash-channel-parity-verify/STORY-GW-REQ59-01-aibridge-stash-parity-verify.md)
- **Parent REQ:** [`59-req15-story-draft-stash-channel-parity-verify.md`](../../../../requirements/59-req15-story-draft-stash-channel-parity-verify.md)
- **Parent product:** REQ15 AC-08
- **decision_ref:** backlog REQ59-01 · package INDEX · Keep GW-DRAFT-01/02/05 · peer arch req15-dual-confirm-handoff
- **Skill declared:** `python-pro` · soft `code-documenter`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Operative package:** [`../../../../gateway-active-packages/pkg-000117-20261105-gw-req59-01-aibridge-stash-parity-verify.yaml`](../../../../gateway-active-packages/pkg-000117-20261105-gw-req59-01-aibridge-stash-parity-verify.yaml)
- **Git:** `dev`
- **Зависит от:** Soft — aibridge STORY-56 Done; soft live G4
- **Blocks:** Soft — SPA-REQ15-01 live `draft_id` evidence
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../../.cursor/rules/analysis.mdc)
- **Scaffolded:** 2026-11-05T12:01:41Z
- **P3 Done:** 2026-11-05T12:10:10Z · [`run-summary`](../../../../run-reports/run-summary-20261105-1210-gw-req59-01-p3.md) · [`evidence`](../../../../../analysis/evidence-gw-req59-01-aibridge-stash-parity-verify-2026-11-05.md)
- **Backlog Emitted:** 2026-11-03 · **L2 intake:** 2026-11-05T11:46:32Z

## Nested tasks (pkg-000117)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req59-01-t01-stash-path-inventory`](./task-gw-req59-01-t01-stash-path-inventory/README.md) | 🔵 Done |
| T02 | [`task-gw-req59-01-t02-aibridge-client-contract-parity`](./task-gw-req59-01-t02-aibridge-client-contract-parity/README.md) | 🔵 Done |
| T03 | [`task-gw-req59-01-t03-auth-boundary-service-vs-citizen`](./task-gw-req59-01-t03-auth-boundary-service-vs-citizen/README.md) | 🔵 Done |
| T04 | [`task-gw-req59-01-t04-stash-neq-story-assert`](./task-gw-req59-01-t04-stash-neq-story-assert/README.md) | 🔵 Done |
| T05 | [`task-gw-req59-01-t05-evidence-or-gap-note`](./task-gw-req59-01-t05-evidence-or-gap-note/README.md) | 🔵 Done |
| T06 | [`task-gw-req59-01-t06-story-gate`](./task-gw-req59-01-t06-story-gate/README.md) | 🔵 Done · gate PASS |
| T07 | [`task-gw-req59-01-t07-audit-g3-g4-ssot-docs`](./task-gw-req59-01-t07-audit-g3-g4-ssot-docs/README.md) | 🔵 Done · G3+G4 CLOSED |

---

## Scope

- Verify Present `POST /story-drafts` remains handoff SSOT for **aibridge** client (service Bearer).
- Evidence: 201 + `draft_id`; stash ≠ published Story; auth boundaries unchanged unless explicit REQ.
- Gap list only if hard break found — no silent contract invent.

## Out of scope

- Interview/roles/telegram; sense-brief; redesign intake for fun.
- Implementing new stash fields without T1/operator lock.
- SPA handoff UX (sibling SPA-REQ15-01); aibridge FSM rewrite (peer 56 Done).

## Verified current state (As-of-Done P3 2026-11-05T12:10:10Z · audit SSOT P6 2026-11-05T12:20:04Z)

| Fact | Evidence |
|------|----------|
| Keep stash lineage Done | STORY-GW-DRAFT-01 / 02 / 05 |
| POST stash + service auth | `asgi_app.py` `_STORY_DRAFT_WRITE_DEPS` · `require_public_content_service_auth` · `POST /story-drafts` — Present |
| Create → 201 + `draft_id` | `handlers.py` `handle_story_draft_create` — Present |
| GET draft = citizen | `require_story_draft_read_user` — Present |
| Submit = citizen + verify gate | `require_story_draft_submit_user` · `handle_story_draft_submit` — Present |
| Aibridge client | peer `gateway.py` `STASH_PATH="/story-drafts"` · `execute_stash` — Present (peer) |
| Evidence note | [`evidence-gw-req59-01-aibridge-stash-parity-verify-2026-11-05.md`](../../../../../analysis/evidence-gw-req59-01-aibridge-stash-parity-verify-2026-11-05.md) — Present · live Unknown · no GW product code |

## Target / AC

- [x] **AC-GW-59-01:** Documented verify: stash 201 + `draft_id` works for aibridge client
- [x] **AC-GW-59-02:** Stash success still ≠ published Story
- [x] **AC-GW-59-03:** If break found: written gap + decision — no silent contract drift
- [x] **AC-GW-59-04:** Service vs citizen auth boundaries unchanged unless explicit REQ
- [x] Default Pass = **no gateway code change** if parity holds

## Code touchpoints

- `asgi_app.py` / `handlers.py` — stash create/read/submit
- Keep GW-DRAFT-01 lineage
- Peer `doge-ai-bridge` `gateway.py` (read-only for parity)
- Evidence: `docs/analysis/` (T05)

## Dependencies

- Soft: aibridge live stash client path (MVP smoke / G4).
- Soft: peer STORY-AIBRIDGE-56 Done (client Keep).
- Blocks (soft): SPA-REQ15-01 live `draft_id` evidence.
