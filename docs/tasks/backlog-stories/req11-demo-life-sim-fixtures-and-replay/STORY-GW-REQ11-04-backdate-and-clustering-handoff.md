# STORY-GW-REQ11-04 — Backdate contract + clustering wait handoff

## Meta
- **Key:** `STORY-GW-REQ11-04-backdate-and-clustering-handoff`
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](./INDEX.md)
- **Status:** Done
- **Тип:** backdate path / runbook handoff
- **Parent REQ:** [`55-…`](../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md) §4.6, §4.8; **GW-11-05**, **GW-11-07**; D5; K3
- **Skill declared (future P3):** `python-pro` · soft `code-documenter`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Operator lock (backdate):** **B** — service-auth controlled backdate after stash→submit (not public intake field invent; not SQL dump as Pass)
- **Зависит от:** STORY-GW-REQ11-03
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Done at:** 2026-09-29T14:39:37Z · P3 · pkg-000103

---

## Scope

1. Documented + implemented **B** path: after API create, service-auth controlled backdate so fixture timestamps survive (exact route/field names at PA.2/P3 — do not invent in this backlog text beyond lock B).
2. Runbook/script documents wait for clustering (`CLUSTER_MIN_SIZE` / cron) before sibling threads social seed handoff (GW-11-07); card count follows clustering (K3).

## Out of scope

- Threads seed itself (sibling `04-…`).
- Spa verify (sibling `20-…`).
- Public intake timestamp invent (rejected vs lock B).
- SQL dump as primary Pass (K4).

## Verified current state

| Fact | Path |
|------|------|
| Submit path stamps `created_at=now` (representative) | `src/core/application/services.py:313`, `:579` |
| `CLUSTER_MIN_SIZE` default in example | `example.env:69` |
| Lock-B ops backdate (P3) | `PATCH /ops/stories/{story_id}/created-at` |
| Clustering wait handoff for life-sim | note + `tests/sandbox/life_sim_wait_clustering.sh` |

## Target / AC

- [x] **AC-GW-REQ1104-01:** Fixture times survive intake via lock-B service-auth backdate (GW-11-05 / D5).
- [x] **AC-GW-REQ1104-02:** Runbook/script documents clustering wait before threads seed handoff (GW-11-07).
- [x] **AC-GW-REQ1104-03:** Explicit note: board card count follows clustering (K3); no invent of new cluster product APIs.

## Code touchpoints

- `PATCH /ops/stories/{story_id}/created-at` + `patch_story_created_at_http` after `post_stash_and_submit_http`
- `services.py` created_at write sites (evidence)
- `example.env` `CLUSTER_MIN_SIZE` / cron

## Dependencies

- REQ11-03 Done enough to exercise submit→backdate.
- Exact endpoint: lock-B `PATCH /ops/stories/{story_id}/created-at`.
