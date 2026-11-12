# STORY-GW-REQ57-04 — Manual regenerate (service-auth)

## Meta
- **Key:** `STORY-GW-REQ57-04-manual-regenerate-service`
- **Пакет:** [`req57-issue-sense-brief-poster/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) · P3 gate PASS 2026-10-15T12:23:00Z · [`pkg-000116`](../../gateway-active-packages/pkg-000116-20261015-gw-req57-04-manual-regenerate-service.yaml) · [pipeline](../../epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-04-manual-regenerate-service/STORY-GW-REQ57-04-manual-regenerate-service.md)
- **Тип:** API / service-auth ops
- **Parent REQ:** [`57-req13-issue-sense-brief-poster-projection.md`](../../../requirements/57-req13-issue-sense-brief-poster-projection.md) §4.6 DP6
- **Architecture:** [`02-job-lifecycle-bind-in-retry.md`](../../../architecture/issue-sense-brief-poster/02-job-lifecycle-bind-in-retry.md) §2.5
- **Env:** [`ENV-CHECKLIST.md`](./ENV-CHECKLIST.md) — `SERVICE_API_TOKEN` + nudge vars
- **Skill declared:** `python-pro` · soft `fastapi-expert`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`  
  Soft: `.cursor/skills/sources/jeffallan-claude-skills/skills/fastapi-expert/SKILL.md`
- **Зависит от:** STORY-GW-REQ57-01, STORY-GW-REQ57-02
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Scaffolded:** 2026-10-15T10:42:18Z
- **P1.3 APPLY:** 2026-10-15T12:17:03Z
- **P3 Done:** 2026-10-15T12:23:00Z · gate PASS · suite **6**

---

## Scope

1. Service-token / S2S only regenerate (not citizen Bearer) — DP6.
2. HTTP path (locked for implement): **`POST /v1/issue-sense-brief/regenerate`** with service-auth (`SERVICE_API_TOKEN`).
3. Effect: bump `generation_version` → `generation_status=pending` → thin nudge (02 client) → await bind.
4. Public consumers see new `generation_version` when ready.

## Out of scope

- Citizen regenerate; SPA UI; auto-regen on Story merge (REQ13 L9).

## Verified current state (As-of-Done P3 2026-10-15T12:23:00Z)

| Fact | Path |
|------|------|
| Regenerate apply | `src/core/application/sense_brief_regenerate.py` |
| Route + service-auth | `asgi_app.py` `POST /v1/issue-sense-brief/regenerate` |
| Stub suite | `tests/test_gw_req57_04_manual_regenerate_service.py` **6 passed** |

## Target / AC

- [x] **AC-GW-REQ5704-01:** service token → version bump + pending + nudge.
- [x] **AC-GW-REQ5704-02:** without service auth → rejected.
- [x] **AC-GW-REQ5704-03:** citizen Bearer cannot regenerate.
- [x] **AC-GW-REQ5704-04:** new version is distinct idempotency key for peer accept.

## Code touchpoints

- `src/core/application/sense_brief_regenerate.py`
- `asgi_app.py` / `handlers.py` — regenerate route
- Nudge client from 02; projection fields from 01

## Dependencies

- STORY-GW-REQ57-01, STORY-GW-REQ57-02

## Nested tasks (pipeline Present under EPIC-req57 · pkg-000116)

| Task | Slug | Status | Essence | Arch / AC |
|------|------|--------|---------|-----------|
| **T01** | `task-gw-req57-04-t01-regenerate-apply` | Done | Bump version → pending; keep brief title/summary; omit public poster while not ready | arch 02 §2.5; AC-5704-01 |
| **T02** | `task-gw-req57-04-t02-regenerate-route-service-auth` | Done | `POST /v1/issue-sense-brief/regenerate` + service-auth | DP6; locked path |
| **T03** | `task-gw-req57-04-t03-regenerate-nudge` | Done | Call nudge client 02 with new version (new peer idempotency key) | arch 02 §2.5; AC-5704-04 |
| **T04** | `task-gw-req57-04-t04-authz-reject-citizen` | Done | Citizen Bearer / missing token → rejected | AC-5704-02/03 |
| **T05** | `task-gw-req57-04-t05-regenerate-tests` | Done | ASGI/unit for regenerate + authz | AC-5704-01…04 |
| **T06** | `task-gw-req57-04-t06-story-gate` | Done | Gate AC-GW-REQ5704-01…04 PASS | story gate |
| **T07** | `task-gw-req57-04-t07-audit-g1-g3-ssot-docs` | Done | Pipeline Status + T01 Purpose SSOT (G1+G3) | audit follow-up |
| **T08** | `task-gw-req57-04-t08-audit-g4-unknown-issue-id-test` | Done | empty/unknown issue_id → 400 (G4) | audit follow-up |
