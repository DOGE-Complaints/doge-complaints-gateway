# STORY-GW-REQ57-02 — Thin nudge on Issue create/publish

## Meta
- **Key:** `STORY-GW-REQ57-02-nudge-on-create-publish`
- **Пакет:** [`req57-issue-sense-brief-poster/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) · P3 gate PASS 2026-10-15T11:41:13Z · [`pipeline`](../../epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-02-nudge-on-create-publish/STORY-GW-REQ57-02-nudge-on-create-publish.md) · [`pkg-000114`](../../gateway-active-packages/pkg-000114-20261015-gw-req57-02-nudge-on-create-publish.yaml)
- **Тип:** outbound S2S client / Issue lifecycle hook
- **Parent REQ:** [`57-req13-issue-sense-brief-poster-projection.md`](../../../requirements/57-req13-issue-sense-brief-poster-projection.md)
- **Architecture:** [`02-job-lifecycle-bind-in-retry.md`](../../../architecture/issue-sense-brief-poster/02-job-lifecycle-bind-in-retry.md)
- **Peer:** `POST /v1/worker/sense-brief/accept` + worker S2S
- **Env:** [`ENV-CHECKLIST.md`](./ENV-CHECKLIST.md) — `AIBRIDGE_BASE_URL`, `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN`, `AIBRIDGE_SENSE_BRIEF_NUDGE_ENABLED`
- **Skill declared:** `python-pro`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Зависит от:** STORY-GW-REQ57-01
- **Blocks:** STORY-GW-REQ57-03, 04
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Scaffolded:** 2026-10-15T10:42:18Z
- **P1.3 APPLY:** 2026-10-15T11:34:35Z
- **P3 Done:** 2026-10-15T11:41:13Z

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
| Nudge config | `src/core/config/schema.py` + `example.env` |
| Nudge client | `src/core/application/sense_brief_nudge.py` |
| Create/publish hook | `issue_create.py` `_apply_pending_and_nudge` |
| Stub suite | `tests/test_gw_req57_02_nudge_on_create_publish.py` **8 passed** |

### Historical (scaffold)
| Fact | Path |
|------|------|
| Issue create route | `asgi_app.py` `@app.post("/node/issues")` ~602 |
| Nudge client | **Absent** |
| Peer accept | Present on aibridge (handoff) |

## Target / AC

- [x] **AC-GW-REQ5702-01:** create/publish → pending + nudge observable (AC-57-03).
- [x] **AC-GW-REQ5702-02:** nudge URL/body/auth match as-built accept + locked env names.
- [x] **AC-GW-REQ5702-03:** tests with HTTP test double (no live aibridge required).
- [x] **AC-GW-REQ5702-04:** missing/disabled nudge config → fail-closed (no silent success).

## Code touchpoints (As-of-Done P3 — Present)

- `src/core/application/issue_create.py` — `_apply_pending_and_nudge` on `_create_issue` + `create_manual_issue`
- `src/core/application/sense_brief_nudge.py` — accept client + fail-closed + corpus helper
- `src/core/config/schema.py` + `example.env` — locked `AIBRIDGE_*` names
- `src/core/infrastructure/service_factory.py` — DI `build_nudge_service_from_config`

## Dependencies

- STORY-GW-REQ57-01 (fields/status on Issue). Operator: fill [`ENV-CHECKLIST.md`](./ENV-CHECKLIST.md) before live verify.

## Nested tasks (pipeline Present under EPIC-req57)

| Task | Slug | Status | Essence | Arch / AC |
|------|------|--------|---------|-----------|
| **T01** | `task-gw-req57-02-t01-nudge-config-env` | Done | Config: `AIBRIDGE_BASE_URL`, `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN`, `AIBRIDGE_SENSE_BRIEF_NUDGE_ENABLED` | ENV-CHECKLIST; arch 00 §5 |
| **T02** | `task-gw-req57-02-t02-nudge-http-client` | Done | Client `POST {base}/v1/worker/sense-brief/accept` + Bearer S2S; body `issue_id`+`generation_version`(+optional `corpus`) | arch 02 §2.1; peer accept |
| **T03** | `task-gw-req57-02-t03-corpus-from-issue-stories` | Done | Optional `corpus` from Issue Stories membership; no clustering change | REQ §2; arch 02 |
| **T04** | `task-gw-req57-02-t04-create-publish-hook` | Done | After create/publish: pending + initial version + nudge | arch 02 §2.1; AC-5702-01 |
| **T05** | `task-gw-req57-02-t05-nudge-fail-closed` | Done | Disabled/missing env → no silent success; pending may remain | AC-5702-04 |
| **T06** | `task-gw-req57-02-t06-nudge-tests-double` | Done | HTTP test double; no live aibridge | AC-5702-01…04 |
| **T07** | `task-gw-req57-02-t07-story-gate` | Done | Gate AC-GW-REQ5702-01…04 PASS | story gate |
| **T08** | `task-gw-req57-02-t08-audit-g3-g5-ssot-docs` | Done | Backlog touchpoints + ENV-CHECKLIST SSOT (G3+G5) | audit follow-up |
| **T09** | `task-gw-req57-02-t09-audit-g4-manual-issue-nudge-test` | Done | `create_manual_issue` pending+nudge test (G4) | audit follow-up |
