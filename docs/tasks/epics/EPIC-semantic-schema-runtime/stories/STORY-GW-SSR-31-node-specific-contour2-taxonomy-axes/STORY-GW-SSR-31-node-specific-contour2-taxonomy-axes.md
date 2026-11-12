# STORY-GW-SSR-31 — Node-specific Contour2 taxonomy axes

## Meta
- **Key:** `STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** P1 — node-taxonomy Contour2 (sequence **31**)
- **Тип:** implement (Contour2 loader + tests)
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md)
- **Architecture:** D-SSR-11 · arch-doc 2026-09-04
- **Parent REQ:** 51
- **decision_ref:** backlog SSR-31
- **Skill declared:** python-pro
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000088-20260904-gw-ssr-31-node-specific-contour2-taxonomy-axes.yaml`](../../../../gateway-active-packages/pkg-000088-20260904-gw-ssr-31-node-specific-contour2-taxonomy-axes.yaml)
- **Git:** только `semantic-schema-runtime`
- **Зависит от:** SSR-26 Done
- **Parallel out:** SSR-32 Contour1; SSR-33 docs
- **Scaffolded:** 2026-09-04T12:50:23Z
- **G31 PASS:** 2026-09-04T12:55:28Z · [`run-summary`](../../../../run-reports/run-summary-20260904-1255-gw-ssr-31-p3.md)

## Nested tasks (pkg-000088)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-ssr-31-t01-resolver-contour2-unlock`](./task-gw-ssr-31-t01-resolver-contour2-unlock/README.md) | Done |
| T02 | [`task-gw-ssr-31-t02-adapt-ssr26-taxonomy-tests`](./task-gw-ssr-31-t02-adapt-ssr26-taxonomy-tests/README.md) | Done |
| T03 | [`task-gw-ssr-31-t03-adapt-ssr28-seed-helper`](./task-gw-ssr-31-t03-adapt-ssr28-seed-helper/README.md) | Done |
| T04 | [`task-gw-ssr-31-t04-tests-uus-shaped-contour2-load`](./task-gw-ssr-31-t04-tests-uus-shaped-contour2-load/README.md) | Done |
| T05 | [`task-gw-ssr-31-t05-story-acceptance-gate`](./task-gw-ssr-31-t05-story-acceptance-gate/README.md) | Done · G31 |
| T06 | [`task-gw-ssr-31-t06-audit-g1-as-of-done-ssot`](./task-gw-ssr-31-t06-audit-g1-as-of-done-ssot/README.md) | Done · G1 CLOSED |

## As-of-Done (P3 2026-09-04T12:55:28Z)

| Fact | Ref |
|------|-----|
| Contour2 lockstep removed | `resolver.py` `_parse_taxonomy_pack` — no `TAXONOMY_AXIS_VALUES` accept/reject |
| Structural validation kept | dupe axes; internal ⊆ axes; map keys ∈ axes; dispositions |
| SSR-26/28 adapted | content 13 = tallinn seed; ≠13 loads OK |
| uus-shaped 24-axis SUCCESS | `tests/test_gw_ssr_31_node_taxonomy_contour2.py` |
| ClusterLens | still 10 |

## Scope / Out of scope

**In:** Contour2 unlock + tests. **Out:** Contour1; docs SSR-33; ClusterLens; uus pack.json; GPT-SSR-15; §Актуальная точка.

## Target / AC

- [x] **AC-GW-SSR31-01…05** — see backlog · G31 PASS
