# STORY-GW-REQ57-03 — Sweep / retry sense-brief jobs

## Meta
- **Key:** `STORY-GW-REQ57-03-sweep-retry-sense-brief`
- **Parent Epic:** [`../../../EPIC-req57-issue-sense-brief-poster.md`](../../../EPIC-req57-issue-sense-brief-poster.md)
- **Пакет:** [`req57-issue-sense-brief-poster/`](../../../../backlog-stories/req57-issue-sense-brief-poster/INDEX.md)
- **Status:** 🔵 Implemented (Waiting Acceptance) · P3 Done 2026-10-15T12:03:07Z · gate PASS
- **Тип:** scheduler / recovery
- **source:** [`../../../../backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-03-sweep-retry-sense-brief.md`](../../../../backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-03-sweep-retry-sense-brief.md)
- **Parent REQ:** [`57-req13-issue-sense-brief-poster-projection.md`](../../../../requirements/57-req13-issue-sense-brief-poster-projection.md) AC-57-06
- **Architecture:** [`02-job-lifecycle-bind-in-retry.md`](../../../../architecture/issue-sense-brief-poster/02-job-lifecycle-bind-in-retry.md) §2.4 · [`00-overview`](../../../../architecture/issue-sense-brief-poster/00-overview.md)
- **Env:** [`ENV-CHECKLIST.md`](../../../../backlog-stories/req57-issue-sense-brief-poster/ENV-CHECKLIST.md) (reuses nudge vars from 02)
- **decision_ref:** backlog REQ57-03 · package INDEX · arch 02 §2.4
- **Skill declared:** `python-pro`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Operative package:** [`../../../../gateway-active-packages/pkg-000115-20261015-gw-req57-03-sweep-retry-sense-brief.yaml`](../../../../gateway-active-packages/pkg-000115-20261015-gw-req57-03-sweep-retry-sense-brief.yaml)
- **Git:** `dev`
- **Зависит от:** STORY-GW-REQ57-01, STORY-GW-REQ57-02
- **Blocks:** —
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../../.cursor/rules/analysis.mdc)
- **Scaffolded:** 2026-10-15T11:57:04Z
- **P3 Done:** 2026-10-15T12:03:07Z · gate PASS · [`run-summary`](../../../../run-reports/run-summary-20261015-1203-gw-req57-03-p3.md)
- **Backlog Scaffolded:** 2026-10-15T10:42:18Z

## Nested tasks (pkg-000115)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req57-03-t01-sweep-eligible-query`](./task-gw-req57-03-t01-sweep-eligible-query/README.md) | 🟢 Done |
| T02 | [`task-gw-req57-03-t02-sense-brief-cron-job`](./task-gw-req57-03-t02-sense-brief-cron-job/README.md) | 🟢 Done |
| T03 | [`task-gw-req57-03-t03-asgi-cron-wire`](./task-gw-req57-03-t03-asgi-cron-wire/README.md) | 🟢 Done |
| T04 | [`task-gw-req57-03-t04-ready-no-alpha-overwrite`](./task-gw-req57-03-t04-ready-no-alpha-overwrite/README.md) | 🟢 Done |
| T05 | [`task-gw-req57-03-t05-sweep-tests`](./task-gw-req57-03-t05-sweep-tests/README.md) | 🟢 Done |
| T06 | [`task-gw-req57-03-t06-story-gate`](./task-gw-req57-03-t06-story-gate/README.md) | 🟢 Done |
| T07 | [`task-gw-req57-03-t07-audit-g1-asgi-lifespan-sweep-test`](./task-gw-req57-03-t07-audit-g1-asgi-lifespan-sweep-test/README.md) | 🟢 Done · audit G1 |
| T08 | [`task-gw-req57-03-t08-audit-g4-t03-asgi-line-refs`](./task-gw-req57-03-t08-audit-g4-t03-asgi-line-refs/README.md) | 🟢 Done · audit G4 |

---

## Scope

1. Cron-class scan Issues with `generation_status` in `pending` / `failed` lacking successful brief apply; re-nudge / recover (AC-57-06).
2. Reuse scheduler precedent `ClusterCronJob` (`asgi_app.py` ~194–220; `cluster_cron.py`).
3. Must not silently overwrite **ready** brief with alpha (brief-wins lock).
4. Same `generation_version` re-nudge may hit aibridge idempotency (safe no-spend); after fail, bump version only when ops/regenerate policy requires (prefer leave version for 04 / explicit bump).

## Out of scope

- Bind/nudge first implement (01/02); manual regenerate endpoint (04); multi-replica aibridge store.

## Verified current state (As-of-Done P3 2026-10-15T12:03:07Z)

| Fact | Path |
|------|------|
| Eligible query | `src/core/application/sense_brief_sweep.py` |
| Sweep service + cron | `sense_brief_sweep.py` + `scheduler/sense_brief_sweep_cron.py` |
| ASGI wire | `asgi_app.py` lifespan (nudge-enabled) |
| Stub suite | `tests/test_gw_req57_03_sweep_retry_sense_brief.py` **5 passed** |

### Historical (scaffold / pre-P3)
| Fact | Path |
|------|------|
| ClusterCronJob | Present |
| Sense-brief sweep | **Absent** |

## Target / AC

- [x] **AC-GW-REQ5703-01:** previously failed/missing job can complete via sweep (AC-57-06).
- [x] **AC-GW-REQ5703-02:** ready brief not silently replaced by alpha on sweep.
- [x] **AC-GW-REQ5703-03:** unit/integration with stubs.

## Code touchpoints

- `src/core/application/sense_brief_sweep.py`
- `src/core/scheduler/sense_brief_sweep_cron.py`
- `src/core/api/asgi_app.py`
- Reuse nudge client from 02 (`sense_brief_nudge.py`)

## Dependencies

- STORY-GW-REQ57-01, STORY-GW-REQ57-02
