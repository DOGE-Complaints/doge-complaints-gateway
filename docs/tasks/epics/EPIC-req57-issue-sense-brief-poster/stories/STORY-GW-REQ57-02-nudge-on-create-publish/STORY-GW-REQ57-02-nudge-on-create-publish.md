# STORY-GW-REQ57-02 — Thin nudge on Issue create/publish

## Meta
- **Key:** `STORY-GW-REQ57-02-nudge-on-create-publish`
- **Parent Epic:** [`../../../EPIC-req57-issue-sense-brief-poster.md`](../../../EPIC-req57-issue-sense-brief-poster.md)
- **Пакет:** [`req57-issue-sense-brief-poster/`](../../../../backlog-stories/req57-issue-sense-brief-poster/INDEX.md)
- **Status:** 🔵 Implemented (Waiting Acceptance) · P3 Done 2026-10-15T11:41:13Z · gate PASS
- **Тип:** outbound S2S client / Issue lifecycle hook
- **source:** [`../../../../backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-02-nudge-on-create-publish.md`](../../../../backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-02-nudge-on-create-publish.md)
- **Parent REQ:** [`57-req13-issue-sense-brief-poster-projection.md`](../../../../requirements/57-req13-issue-sense-brief-poster-projection.md)
- **Architecture:** [`02-job-lifecycle-bind-in-retry.md`](../../../../architecture/issue-sense-brief-poster/02-job-lifecycle-bind-in-retry.md) · [`00-overview`](../../../../architecture/issue-sense-brief-poster/00-overview.md)
- **Peer:** `POST /v1/worker/sense-brief/accept` + worker S2S
- **Env:** [`ENV-CHECKLIST.md`](../../../../backlog-stories/req57-issue-sense-brief-poster/ENV-CHECKLIST.md) — `AIBRIDGE_BASE_URL`, `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN`, `AIBRIDGE_SENSE_BRIEF_NUDGE_ENABLED`
- **decision_ref:** backlog REQ57-02 · package INDEX · peer handoff · arch 02
- **Skill declared:** `python-pro`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Operative package:** [`../../../../gateway-active-packages/pkg-000114-20261015-gw-req57-02-nudge-on-create-publish.yaml`](../../../../gateway-active-packages/pkg-000114-20261015-gw-req57-02-nudge-on-create-publish.yaml)
- **Git:** `dev`
- **Зависит от:** STORY-GW-REQ57-01
- **Blocks:** STORY-GW-REQ57-03, 04
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../../.cursor/rules/analysis.mdc)
- **Scaffolded:** 2026-10-15T11:34:35Z
- **P3 Done:** 2026-10-15T11:41:13Z · gate PASS · [`run-summary`](../../../../run-reports/run-summary-20261015-1141-gw-req57-02-p3.md)
- **Backlog Scaffolded:** 2026-10-15T10:42:18Z

## Nested tasks (pkg-000114)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req57-02-t01-nudge-config-env`](./task-gw-req57-02-t01-nudge-config-env/README.md) | 🟢 Done |
| T02 | [`task-gw-req57-02-t02-nudge-http-client`](./task-gw-req57-02-t02-nudge-http-client/README.md) | 🟢 Done |
| T03 | [`task-gw-req57-02-t03-corpus-from-issue-stories`](./task-gw-req57-02-t03-corpus-from-issue-stories/README.md) | 🟢 Done |
| T04 | [`task-gw-req57-02-t04-create-publish-hook`](./task-gw-req57-02-t04-create-publish-hook/README.md) | 🟢 Done |
| T05 | [`task-gw-req57-02-t05-nudge-fail-closed`](./task-gw-req57-02-t05-nudge-fail-closed/README.md) | 🟢 Done |
| T06 | [`task-gw-req57-02-t06-nudge-tests-double`](./task-gw-req57-02-t06-nudge-tests-double/README.md) | 🟢 Done |
| T07 | [`task-gw-req57-02-t07-story-gate`](./task-gw-req57-02-t07-story-gate/README.md) | 🟢 Done |
| T08 | [`task-gw-req57-02-t08-audit-g3-g5-ssot-docs`](./task-gw-req57-02-t08-audit-g3-g5-ssot-docs/README.md) | 🟢 Done · audit G3+G5 |
| T09 | [`task-gw-req57-02-t09-audit-g4-manual-issue-nudge-test`](./task-gw-req57-02-t09-audit-g4-manual-issue-nudge-test/README.md) | 🟢 Done · audit G4 |

---

## Scope

1. After successful Issue create/publish → set `generation_status=pending` + initial `generation_version`.
2. Thin nudge: `POST {AIBRIDGE_BASE_URL}/v1/worker/sense-brief/accept` with body `issue_id`, `generation_version`, optional `corpus`.
3. Auth: `Authorization: Bearer {AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN}`.
4. Gate on `AIBRIDGE_SENSE_BRIEF_NUDGE_ENABLED=true`; if disabled/missing required env → fail-closed (no pretend success); pending may remain observable.
5. Observable in logs / test double (AC-57-03).
6. Do not run LLM/image in gateway.

## Out of scope

- Bind receiver (01); sweep (03); regenerate (04).

## Verified current state (As-of-Done P3 2026-10-15T11:41:13Z)

| Fact | Path |
|------|------|
| Nudge config env | `src/core/config/schema.py` + `example.env` |
| Nudge client | `src/core/application/sense_brief_nudge.py` |
| Create/publish hook | `issue_create.py` `_apply_pending_and_nudge` |
| Stub suite | `tests/test_gw_req57_02_nudge_on_create_publish.py` **8 passed** |

### Historical (scaffold / pre-P3)
| Fact | Path |
|------|------|
| Issue create route | `asgi_app.py` `@app.post("/node/issues")` ~602 Present |
| Nudge client / `AIBRIDGE_*` in `src/` | **Absent** |

## Target / AC

- [x] **AC-GW-REQ5702-01:** create/publish → pending + nudge observable (AC-57-03).
- [x] **AC-GW-REQ5702-02:** nudge URL/body/auth match as-built accept + locked env names.
- [x] **AC-GW-REQ5702-03:** tests with HTTP test double (no live aibridge required).
- [x] **AC-GW-REQ5702-04:** missing/disabled nudge config → fail-closed (no silent success).

## Code touchpoints

- Issue create/publish success path (`issue_create.py` / handlers)
- `src/core/application/sense_brief_nudge.py`
- Config schema for locked env names

## Dependencies

- STORY-GW-REQ57-01 (fields/status on Issue). Operator: fill ENV-CHECKLIST before live verify.
