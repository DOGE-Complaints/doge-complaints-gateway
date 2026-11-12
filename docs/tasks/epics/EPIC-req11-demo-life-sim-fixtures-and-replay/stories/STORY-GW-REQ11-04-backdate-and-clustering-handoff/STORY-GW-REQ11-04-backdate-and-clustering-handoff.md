# STORY-GW-REQ11-04 — Backdate contract + clustering wait handoff

## Meta
- **Key:** `STORY-GW-REQ11-04-backdate-and-clustering-handoff`
- **Parent Epic:** [`../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md`](../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md)
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/INDEX.md)
- **Status:** ✅ Done
- **Done at:** 2026-09-29T14:39:37Z
- **Тип:** backdate path / runbook handoff
- **source:** [`../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-04-backdate-and-clustering-handoff.md`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-04-backdate-and-clustering-handoff.md)
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md) §4.6, §4.8; **GW-11-05**, **GW-11-07**; D5; K3
- **decision_ref:** backlog REQ11-04 · REQ55 §4.6/§4.8 · GW-11-05/07 · D5 · K3 · lock B
- **Skill declared:** python-pro · soft code-documenter
- **Operative package:** [`../../../../gateway-active-packages/pkg-000103-20260929-gw-req11-04-backdate-and-clustering-handoff.yaml`](../../../../gateway-active-packages/pkg-000103-20260929-gw-req11-04-backdate-and-clustering-handoff.yaml)
- **Git:** `dev`
- **Operator lock (backdate):** **B** — service-auth controlled backdate after stash→submit (not public intake field invent; not SQL dump as Pass)
- **Зависит от:** STORY-GW-REQ11-03
- **Scaffolded:** 2026-09-29T14:33:30Z

## Nested tasks (pkg-000103)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req11-04-t01-created-at-stamp-evidence`](./task-gw-req11-04-t01-created-at-stamp-evidence/README.md) | Done |
| T02 | [`task-gw-req11-04-t02-lock-b-service-auth-backdate`](./task-gw-req11-04-t02-lock-b-service-auth-backdate/README.md) | Done |
| T03 | [`task-gw-req11-04-t03-replay-apply-fixture-timestamps`](./task-gw-req11-04-t03-replay-apply-fixture-timestamps/README.md) | Done |
| T04 | [`task-gw-req11-04-t04-clustering-wait-runbook`](./task-gw-req11-04-t04-clustering-wait-runbook/README.md) | Done |
| T05 | [`task-gw-req11-04-t05-k3-card-count-follows-clustering`](./task-gw-req11-04-t05-k3-card-count-follows-clustering/README.md) | Done |
| T06 | [`task-gw-req11-04-t06-story-gate`](./task-gw-req11-04-t06-story-gate/README.md) | Done |
| T07 | [`task-gw-req11-04-t07-audit-g2-as-of-done-ssot`](./task-gw-req11-04-t07-audit-g2-as-of-done-ssot/README.md) | Done · G2 CLOSED P6 |
| T08 | [`task-gw-req11-04-t08-audit-g4-note-wait-script-pointer`](./task-gw-req11-04-t08-audit-g4-note-wait-script-pointer/README.md) | Done · G4 CLOSED P6 |

## Scope

1. Documented + implemented **B** path: after API create, service-auth controlled backdate so fixture timestamps survive (exact route/field names at PA.2/P3 — do not invent in this backlog text beyond lock B).
2. Runbook/script documents wait for clustering (`CLUSTER_MIN_SIZE` / cron) before sibling threads social seed handoff (GW-11-07); card count follows clustering (K3).

## Out of scope

- Threads seed itself (sibling `04-…`).
- Spa verify (sibling `20-…`).
- Public intake timestamp invent (rejected vs lock B).
- SQL dump as primary Pass (K4).

## Verified current state (As-of-Done 2026-09-29T14:39:37Z)

| Fact | Path |
|------|------|
| Submit path stamps `created_at=now` (representative) | `src/core/application/services.py:313`, `:579` |
| `CLUSTER_MIN_SIZE` default in example | `example.env:69` |
| Lock-B ops backdate | `PATCH /ops/stories/{story_id}/created-at` · `StoryRepository.update_created_at` |
| Runner applies fixture times via B | `tests/simulation_runner.py` `--life-sim` + `patch_story_created_at_http` |
| Clustering wait handoff | note + `tests/sandbox/life_sim_wait_clustering.sh` |

## Target / AC

- [x] **AC-GW-REQ1104-01:** Fixture times survive intake via lock-B service-auth backdate (GW-11-05 / D5).
- [x] **AC-GW-REQ1104-02:** Runbook/script documents clustering wait before threads seed handoff (GW-11-07).
- [x] **AC-GW-REQ1104-03:** Explicit note: board card count follows clustering (K3); no invent of new cluster product APIs.

## Code touchpoints

- `PATCH /ops/stories/{story_id}/created-at` (`asgi_app` / `handlers`)
- `patch_story_created_at_http` + `--life-sim` backdate after submit
- `example.env` `CLUSTER_MIN_SIZE` / `CLUSTER_CRON_*`
- Note: `docs/analysis/note-gw-req11-04-backdate-and-clustering-handoff-2026-09-29.md`

## Dependencies

- REQ11-03 Done enough to exercise submit→backdate.
- Exact endpoint: `PATCH /ops/stories/{story_id}/created-at` (lock B; service-auth).
