# STORY-GW-REQ57-01 — Bind-in receiver + sense-brief projection apply

## Meta
- **Key:** `STORY-GW-REQ57-01-bind-in-projection-apply`
- **Parent Epic:** [`../../../EPIC-req57-issue-sense-brief-poster.md`](../../../EPIC-req57-issue-sense-brief-poster.md)
- **Пакет:** [`req57-issue-sense-brief-poster/`](../../../../backlog-stories/req57-issue-sense-brief-poster/INDEX.md)
- **Status:** 🔵 Implemented (Waiting Acceptance) · P3 Done 2026-10-15T11:13:59Z · gate PASS
- **Тип:** API / service-auth bind-in / Issue projection
- **source:** [`../../../../backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-01-bind-in-projection-apply.md`](../../../../backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-01-bind-in-projection-apply.md)
- **Parent REQ:** [`57-req13-issue-sense-brief-poster-projection.md`](../../../../requirements/57-req13-issue-sense-brief-poster-projection.md)
- **Architecture:** [`00-overview`](../../../../architecture/issue-sense-brief-poster/00-overview.md) · [`01-projection`](../../../../architecture/issue-sense-brief-poster/01-projection-and-brief-apply.md) · [`02-lifecycle`](../../../../architecture/issue-sense-brief-poster/02-job-lifecycle-bind-in-retry.md) · [`03-public-wire`](../../../../architecture/issue-sense-brief-poster/03-public-wire-and-media.md)
- **Peer handoff:** [`handoff-gateway-req13-sense-brief-worker-2026-10-15.md`](../../../../../../doge-ai-bridge/docs/analysis/handoff-gateway-req13-sense-brief-worker-2026-10-15.md)
- **Env:** [`ENV-CHECKLIST.md`](../../../../backlog-stories/req57-issue-sense-brief-poster/ENV-CHECKLIST.md) — bind uses `SERVICE_API_TOKEN`
- **decision_ref:** backlog REQ57-01 · package INDEX operator locks 2026-10-15 · peer handoff · arch 00–03
- **Siblings:** aibridge REQ-09 (bind client Present); spa 23 (consumer of locked public keys); soft REQ57-02/03/04
- **Skill declared:** `python-pro` · soft `fastapi-expert`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`  
  Soft: `.cursor/skills/sources/jeffallan-claude-skills/skills/fastapi-expert/SKILL.md`
- **Operative package:** [`../../../../gateway-active-packages/pkg-000113-20261015-gw-req57-01-bind-in-projection-apply.yaml`](../../../../gateway-active-packages/pkg-000113-20261015-gw-req57-01-bind-in-projection-apply.yaml)
- **Git:** `dev`
- **Operator locks:** bind `POST /v1/issue-sense-brief/bind` + `SERVICE_API_TOKEN`; public keys locked; brief wins until regenerate; DP5 no job table
- **Зависит от:** —
- **Blocks:** STORY-GW-REQ57-02, 03, 04
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../../.cursor/rules/analysis.mdc)
- **Scaffolded:** 2026-10-15T11:04:04Z
- **Backlog Scaffolded:** 2026-10-15T10:42:18Z
- **P3 Done:** 2026-10-15T11:13:59Z · [`run-summary`](../../../../run-reports/run-summary-20261015-1113-gw-req57-01-p3.md) · [`gate`](./task-gw-req57-01-t08-story-gate/story-acceptance-gate-STORY-GW-REQ57-01.md) PASS

## Nested tasks (pkg-000113)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req57-01-t01-generation-fields-persist`](./task-gw-req57-01-t01-generation-fields-persist/README.md) | 🟢 Done |
| T02 | [`task-gw-req57-01-t02-public-payload-keys`](./task-gw-req57-01-t02-public-payload-keys/README.md) | 🟢 Done |
| T03 | [`task-gw-req57-01-t03-bind-success-apply`](./task-gw-req57-01-t03-bind-success-apply/README.md) | 🟢 Done |
| T04 | [`task-gw-req57-01-t04-bind-fail-apply`](./task-gw-req57-01-t04-bind-fail-apply/README.md) | 🟢 Done |
| T05 | [`task-gw-req57-01-t05-bind-route-service-auth`](./task-gw-req57-01-t05-bind-route-service-auth/README.md) | 🟢 Done |
| T06 | [`task-gw-req57-01-t06-brief-wins-guard`](./task-gw-req57-01-t06-brief-wins-guard/README.md) | 🟢 Done |
| T07 | [`task-gw-req57-01-t07-unit-asgi-bind-tests`](./task-gw-req57-01-t07-unit-asgi-bind-tests/README.md) | 🟢 Done |
| T08 | [`task-gw-req57-01-t08-story-gate`](./task-gw-req57-01-t08-story-gate/README.md) | 🟢 Done |
| T09 | [`task-gw-req57-01-t09-audit-g1-g4-ssot-docs`](./task-gw-req57-01-t09-audit-g1-g4-ssot-docs/README.md) | ⚪ Todo · audit G1+G4 |
| T10 | [`task-gw-req57-01-t10-audit-g3-extend-issue-test`](./task-gw-req57-01-t10-audit-g3-extend-issue-test/README.md) | ⚪ Todo · audit G3 |
| T11 | [`task-gw-req57-01-t11-audit-g5-wrong-bearer-test`](./task-gw-req57-01-t11-audit-g5-wrong-bearer-test/README.md) | ⚪ Todo · audit G5 |

---

## Scope

1. Serve as-built bind path **`POST /v1/issue-sense-brief/bind`** with gateway service-auth (`SERVICE_API_TOKEN`; peer posts `GATEWAY_SERVICE_API_TOKEN` — same value).
2. On `outcome=success`: apply `apply.title` (≤80 plain) + `apply.summary` i18n; persist `poster_url` + `generation_version`; set **`generation_status=ready`**.
3. On `outcome=failure`: **`generation_status=failed`**; fail-closed/placeholder text; log `reason_class`; no silent alpha-as-AI-sense (AC-57-07).
4. Public Issue read exposes locked keys (operator 2026-10-15):
   - `generation_status`: `pending` | `ready` | `failed`
   - `generation_version`: string
   - `poster_url`: HTTPS when ready; omit or null when not
5. Reject channel Bearer / worker S2S as bind auth.
6. No separate job table (DP5).
7. **Conflict lock:** after ready, brief-derived title/summary **win until regenerate** — dominant Story extraction must not silently overwrite (operator 2026-10-15).

## Out of scope

- Thin nudge (→ 02); sweep (→ 03); manual regenerate (→ 04).
- LLM/image; SPA UI; Arweave as MVP poster.
- aibridge worker internals.

## Verified current state (As-of-Done P3 2026-10-15T11:13:59Z)

| Fact | Path |
|------|------|
| Bind route + service-auth | `src/core/api/asgi_app.py` `POST /v1/issue-sense-brief/bind` + `require_public_content_service_auth` |
| Bind apply service | `src/core/application/sense_brief_bind.py` `IssueSenseBriefBindService` |
| Generation fields columnar | `src/core/projection/columnar_storage.py` + SQLite migrate + InMemory |
| Brief-wins on extend | `issue_create.py` `_extend_issue` + `preserve_brief_wins_fields` |
| Stub suite | `tests/test_gw_req57_01_bind_in_projection_apply.py` **8 passed** |
| Dominant Story extraction (still Present) | `src/core/projection/extraction_policy.py` |

### Historical (scaffold / pre-P3)
| Fact | Path |
|------|------|
| Bind receiver `/v1/issue-sense-brief/bind` | **Absent** |
| `generation_status` / `poster_url` in `src/` | **Absent** |

## Target / AC

- [x] **AC-GW-REQ5701-01:** success bind → public title/summary ≠ sole dominant-story baseline (AC-57-01).
- [x] **AC-GW-REQ5701-02:** brief-sourced title ≤80 / plainness per REQ13 (AC-57-02).
- [x] **AC-GW-REQ5701-03:** public read includes `poster_url` when ready (AC-57-04).
- [x] **AC-GW-REQ5701-04:** `generation_status` pending/ready/failed distinguishable (AC-57-05).
- [x] **AC-GW-REQ5701-05:** fail bind → failed + no pretend AI sense (AC-57-07).
- [x] **AC-GW-REQ5701-06:** ready brief not overwritten by dominant Story without regenerate.
- [x] **AC-GW-REQ5701-07:** unit/ASGI tests with stub bind payloads (no live LLM).

## Code touchpoints (As-of-Done P3 — Present)

- `src/core/api/asgi_app.py` / `handlers.py` — bind route
- `src/core/application/sense_brief_bind.py` — apply + brief-wins helper
- `src/core/projection/columnar_storage.py` / stores — generation fields
- `src/core/application/issue_create.py` — brief-wins on extend save

## Dependencies

- Peer bind schema frozen (handoff). Public keys + brief-wins locked (package INDEX).

## Related

- Backlog: [`../../../../backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-01-bind-in-projection-apply.md`](../../../../backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-01-bind-in-projection-apply.md)
- Epic / INDEX: [`../../../EPIC-req57-issue-sense-brief-poster.md`](../../../EPIC-req57-issue-sense-brief-poster.md) · [`../../../../backlog-stories/req57-issue-sense-brief-poster/INDEX.md`](../../../../backlog-stories/req57-issue-sense-brief-poster/INDEX.md)
- Gate: [`./task-gw-req57-01-t08-story-gate/story-acceptance-gate-STORY-GW-REQ57-01.md`](./task-gw-req57-01-t08-story-gate/story-acceptance-gate-STORY-GW-REQ57-01.md)
