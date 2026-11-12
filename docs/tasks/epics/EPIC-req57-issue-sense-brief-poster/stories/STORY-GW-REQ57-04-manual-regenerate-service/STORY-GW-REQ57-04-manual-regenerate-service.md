# STORY-GW-REQ57-04 — Manual regenerate (service-auth)

## Meta
- **Key:** `STORY-GW-REQ57-04-manual-regenerate-service`
- **Parent Epic:** [`../../../EPIC-req57-issue-sense-brief-poster.md`](../../../EPIC-req57-issue-sense-brief-poster.md)
- **Пакет:** [`req57-issue-sense-brief-poster/`](../../../../backlog-stories/req57-issue-sense-brief-poster/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) · P3 Done 2026-10-15T12:23:00Z · gate PASS · audit P6 T07–T08
- **Тип:** API / service-auth ops
- **source:** [`../../../../backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-04-manual-regenerate-service.md`](../../../../backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-04-manual-regenerate-service.md)
- **Parent REQ:** [`57-req13-issue-sense-brief-poster-projection.md`](../../../../requirements/57-req13-issue-sense-brief-poster-projection.md) §4.6 DP6
- **Architecture:** [`02-job-lifecycle-bind-in-retry.md`](../../../../architecture/issue-sense-brief-poster/02-job-lifecycle-bind-in-retry.md) §2.5 · [`00-overview`](../../../../architecture/issue-sense-brief-poster/00-overview.md)
- **Env:** [`ENV-CHECKLIST.md`](../../../../backlog-stories/req57-issue-sense-brief-poster/ENV-CHECKLIST.md) — `SERVICE_API_TOKEN` + nudge vars
- **decision_ref:** backlog REQ57-04 · package INDEX · arch 02 §2.5 · DP6
- **Skill declared:** `python-pro` · soft `fastapi-expert`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`  
  Soft: `.cursor/skills/sources/jeffallan-claude-skills/skills/fastapi-expert/SKILL.md`
- **Operative package:** [`../../../../gateway-active-packages/pkg-000116-20261015-gw-req57-04-manual-regenerate-service.yaml`](../../../../gateway-active-packages/pkg-000116-20261015-gw-req57-04-manual-regenerate-service.yaml)
- **Git:** `dev`
- **Зависит от:** STORY-GW-REQ57-01, STORY-GW-REQ57-02
- **Blocks:** —
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../../.cursor/rules/analysis.mdc)
- **Scaffolded:** 2026-10-15T12:17:03Z
- **P3 Done:** 2026-10-15T12:23:00Z · gate PASS · [`run-summary`](../../../../run-reports/run-summary-20261015-1223-gw-req57-04-p3.md)
- **Backlog Scaffolded:** 2026-10-15T10:42:18Z

## Nested tasks (pkg-000116)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req57-04-t01-regenerate-apply`](./task-gw-req57-04-t01-regenerate-apply/README.md) | 🟢 Done |
| T02 | [`task-gw-req57-04-t02-regenerate-route-service-auth`](./task-gw-req57-04-t02-regenerate-route-service-auth/README.md) | 🟢 Done |
| T03 | [`task-gw-req57-04-t03-regenerate-nudge`](./task-gw-req57-04-t03-regenerate-nudge/README.md) | 🟢 Done |
| T04 | [`task-gw-req57-04-t04-authz-reject-citizen`](./task-gw-req57-04-t04-authz-reject-citizen/README.md) | 🟢 Done |
| T05 | [`task-gw-req57-04-t05-regenerate-tests`](./task-gw-req57-04-t05-regenerate-tests/README.md) | 🟢 Done |
| T06 | [`task-gw-req57-04-t06-story-gate`](./task-gw-req57-04-t06-story-gate/README.md) | 🟢 Done |
| T07 | [`task-gw-req57-04-t07-audit-g1-g3-ssot-docs`](./task-gw-req57-04-t07-audit-g1-g3-ssot-docs/README.md) | 🟢 Done · audit G1+G3 |
| T08 | [`task-gw-req57-04-t08-audit-g4-unknown-issue-id-test`](./task-gw-req57-04-t08-audit-g4-unknown-issue-id-test/README.md) | 🟢 Done · audit G4 |

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
| Nudge reuse | `sense_brief_nudge.py` via regenerate service |
| Stub suite | `tests/test_gw_req57_04_manual_regenerate_service.py` **6 passed** |

### Historical (scaffold / pre-P3)
| Fact | Path |
|------|------|
| Service-auth helpers | Present |
| Regenerate endpoint | **Absent** |

## Target / AC

- [x] **AC-GW-REQ5704-01:** service token → version bump + pending + nudge.
- [x] **AC-GW-REQ5704-02:** without service auth → rejected.
- [x] **AC-GW-REQ5704-03:** citizen Bearer cannot regenerate.
- [x] **AC-GW-REQ5704-04:** new version is distinct idempotency key for peer accept.

## Code touchpoints

- `src/core/application/sense_brief_regenerate.py`
- `src/core/api/asgi_app.py` / `handlers.py`
- Nudge client from 02; projection fields from 01

## Dependencies

- STORY-GW-REQ57-01, STORY-GW-REQ57-02
