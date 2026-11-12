# STORY-GW-REQ57-01 — Bind-in receiver + sense-brief projection apply

## Meta
- **Key:** `STORY-GW-REQ57-01-bind-in-projection-apply`
- **Пакет:** [`req57-issue-sense-brief-poster/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) · P3 gate PASS 2026-10-15T11:13:59Z · [pipeline](../../epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-01-bind-in-projection-apply/STORY-GW-REQ57-01-bind-in-projection-apply.md) · [pkg-000113](../../gateway-active-packages/pkg-000113-20261015-gw-req57-01-bind-in-projection-apply.yaml)
- **Тип:** API / service-auth bind-in / Issue projection
- **Parent REQ:** [`57-req13-issue-sense-brief-poster-projection.md`](../../../requirements/57-req13-issue-sense-brief-poster-projection.md)
- **Architecture:** [`00-overview`](../../../architecture/issue-sense-brief-poster/00-overview.md) · [`01-projection`](../../../architecture/issue-sense-brief-poster/01-projection-and-brief-apply.md) · [`02-lifecycle`](../../../architecture/issue-sense-brief-poster/02-job-lifecycle-bind-in-retry.md) · [`03-public-wire`](../../../architecture/issue-sense-brief-poster/03-public-wire-and-media.md)
- **Peer handoff:** [`handoff-gateway-req13-sense-brief-worker-2026-10-15.md`](../../../../doge-ai-bridge/docs/analysis/handoff-gateway-req13-sense-brief-worker-2026-10-15.md)
- **Env:** [`ENV-CHECKLIST.md`](./ENV-CHECKLIST.md) — bind uses `SERVICE_API_TOKEN`
- **Siblings:** aibridge REQ-09 (bind client Present); spa 23 (consumer of locked public keys)
- **Skill declared:** `python-pro` · soft `fastapi-expert`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`  
  Soft: `.cursor/skills/sources/jeffallan-claude-skills/skills/fastapi-expert/SKILL.md`
- **Зависит от:** —
- **Blocks:** STORY-GW-REQ57-02, 03, 04
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Scaffolded:** 2026-10-15T10:42:18Z
- **P1.3 APPLY:** 2026-10-15T11:04:04Z · Epic [`EPIC-req57-issue-sense-brief-poster`](../../epics/EPIC-req57-issue-sense-brief-poster.md)

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

## Verified current state (As-of-Done P3 2026-10-15T11:13:59Z · P6 SSOT sync)

| Fact | Path |
|------|------|
| Bind route + service-auth | `src/core/api/asgi_app.py` `POST /v1/issue-sense-brief/bind` + `require_public_content_service_auth` |
| Bind apply service | `src/core/application/sense_brief_bind.py` `IssueSenseBriefBindService` |
| Generation fields columnar | `src/core/projection/columnar_storage.py` + SQLite migrate + InMemory |
| Brief-wins on extend | `issue_create.py` `_extend_issue` + `preserve_brief_wins_fields` |
| Stub suite | `tests/test_gw_req57_01_bind_in_projection_apply.py` |
| Dominant Story extraction (still Present) | `src/core/projection/extraction_policy.py:29–35`, `:167–178` |
| aibridge bind client | Present (peer handoff) |

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

## Nested tasks (pipeline Present under EPIC-req57)

| Task | Slug | Status | Essence | Arch / AC |
|------|------|--------|---------|-----------|
| **T01** | `task-gw-req57-01-t01-generation-fields-persist` | 🟢 Done | Issue fields: `generation_status`, `generation_version`, `poster_url`, optional `generation_reason_class`; SQLite migrate + store R/W | arch 00 §3 DP5 |
| **T02** | `task-gw-req57-01-t02-public-payload-keys` | 🟢 Done | Serialize locked keys on public Issue list/get | AC-5701-03/04; arch 03 |
| **T03** | `task-gw-req57-01-t03-bind-success-apply` | 🟢 Done | Apply `apply.title` ≤80 + `apply.summary`; set ready + `poster_url` + version | arch 01 success; AC-5701-01/02 |
| **T04** | `task-gw-req57-01-t04-bind-fail-apply` | 🟢 Done | Fail path: failed + fail-closed text + `reason_class` log | arch 01 fail; AC-5701-05 |
| **T05** | `task-gw-req57-01-t05-bind-route-service-auth` | 🟢 Done | `POST /v1/issue-sense-brief/bind` + service-auth (`SERVICE_API_TOKEN`) | peer handoff §4 |
| **T06** | `task-gw-req57-01-t06-brief-wins-guard` | 🟢 Done | After ready — dominant Story must not overwrite title/summary without regenerate | operator lock; AC-5701-06 |
| **T07** | `task-gw-req57-01-t07-unit-asgi-bind-tests` | 🟢 Done | Stub success/fail bind payloads; no live LLM | AC-5701-01…06 |
| **T08** | `task-gw-req57-01-t08-story-gate` | 🟢 Done | Gate AC-GW-REQ5701-01…07 PASS | story gate |
| **T09** | `task-gw-req57-01-t09-audit-g1-g4-ssot-docs` | audit follow-up | backlog SSOT + T06 Where | G1+G4 |
| **T10** | `task-gw-req57-01-t10-audit-g3-extend-issue-test` | audit follow-up | live `_extend_issue` AC-06 | G3 |
| **T11** | `task-gw-req57-01-t11-audit-g5-wrong-bearer-test` | audit follow-up | wrong Bearer → 401 | G5 |
