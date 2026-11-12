# STORY-GW-REQ57-03 — Sweep / retry sense-brief jobs

## Meta
- **Key:** `STORY-GW-REQ57-03-sweep-retry-sense-brief`
- **Пакет:** [`req57-issue-sense-brief-poster/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) · P3 gate PASS 2026-10-15T12:03:07Z · [`pkg-000115`](../../gateway-active-packages/pkg-000115-20261015-gw-req57-03-sweep-retry-sense-brief.yaml) · [pipeline](../../epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-03-sweep-retry-sense-brief/STORY-GW-REQ57-03-sweep-retry-sense-brief.md)
- **Тип:** scheduler / recovery
- **Parent REQ:** [`57-req13-issue-sense-brief-poster-projection.md`](../../../requirements/57-req13-issue-sense-brief-poster-projection.md) AC-57-06
- **Architecture:** [`02-job-lifecycle-bind-in-retry.md`](../../../architecture/issue-sense-brief-poster/02-job-lifecycle-bind-in-retry.md) §2.4
- **Env:** [`ENV-CHECKLIST.md`](./ENV-CHECKLIST.md) (reuses nudge vars from 02)
- **Skill declared:** `python-pro`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Зависит от:** STORY-GW-REQ57-01, STORY-GW-REQ57-02
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Scaffolded:** 2026-10-15T10:42:18Z
- **P1 APPLY:** 2026-10-15T11:57:04Z
- **P3 Done:** 2026-10-15T12:03:07Z · gate PASS · suite 5

---

## Scope

1. Cron-class scan Issues with `generation_status` in `pending` / `failed` lacking successful brief apply; re-nudge / recover (AC-57-06).
2. Reuse scheduler precedent `ClusterCronJob` (`asgi_app.py` ~194–220; `cluster_cron.py`).
3. Must not silently overwrite **ready** brief with alpha (brief-wins lock).
4. Same `generation_version` re-nudge may hit aibridge idempotency (safe no-spend); after fail, bump version only when ops/regenerate policy requires (prefer leave version for 04 / explicit bump).

## Out of scope

- Bind/nudge first implement (01/02); manual regenerate endpoint (04); multi-replica aibridge store.

## Verified current state (As-of-Done P3)

| Fact | Path |
|------|------|
| Eligible + sweep service | `src/core/application/sense_brief_sweep.py` |
| Cron job | `src/core/scheduler/sense_brief_sweep_cron.py` |
| ASGI wire | `asgi_app.py` lifespan |
| Stub suite | `tests/test_gw_req57_03_sweep_retry_sense_brief.py` **5 passed** |

### Historical (pre-P3)
| Fact | Path |
|------|------|
| ClusterCronJob | Present |
| Sense-brief sweep | **Absent** |

## Target / AC

- [x] **AC-GW-REQ5703-01:** previously failed/missing job can complete via sweep (AC-57-06).
- [x] **AC-GW-REQ5703-02:** ready brief not silently replaced by alpha on sweep.
- [x] **AC-GW-REQ5703-03:** unit/integration with stubs.

## Code touchpoints (As-of-Done P3)

- `src/core/application/sense_brief_sweep.py`
- `src/core/scheduler/sense_brief_sweep_cron.py`
- `src/core/api/asgi_app.py`
- Reuse nudge client from 02 (`sense_brief_nudge.py`)

## Dependencies

- STORY-GW-REQ57-01, STORY-GW-REQ57-02

## Nested tasks (pipeline Present under EPIC-req57 · pkg-000115)

| Task | Slug | Status | Essence | Arch / AC |
|------|------|--------|---------|-----------|
| **T01** | `task-gw-req57-03-t01-sweep-eligible-query` | Done | Select Issues `pending`/`failed` without successful brief apply | arch 02 §2.4 |
| **T02** | `task-gw-req57-03-t02-sense-brief-cron-job` | Done | Cron-class (precedent `ClusterCronJob`) — re-nudge via client from 02 | arch 02 §2.4; AC-5703-01 |
| **T03** | `task-gw-req57-03-t03-asgi-cron-wire` | Done | Start/stop sweep cron in `asgi_app.py` lifespan (nudge-enabled) | `asgi_app.py` ~229–265 |
| **T04** | `task-gw-req57-03-t04-ready-no-alpha-overwrite` | Done | Sweep must not replace ready brief with alpha | brief-wins; AC-5703-02 |
| **T05** | `task-gw-req57-03-t05-sweep-tests` | Done | Stub nudge + pending/failed fixtures → recover path | AC-5703-01…03 |
| **T06** | `task-gw-req57-03-t06-story-gate` | Done | Gate AC-GW-REQ5703-01…03 PASS | story gate |
| **T07** | `task-gw-req57-03-t07-audit-g1-asgi-lifespan-sweep-test` | Done | ASGI lifespan sweep cron test (G1) | audit follow-up |
| **T08** | `task-gw-req57-03-t08-audit-g4-t03-asgi-line-refs` | Done | T03 ASGI line-ref SSOT (G4) | audit follow-up |
