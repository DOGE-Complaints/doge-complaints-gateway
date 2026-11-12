# STORY-GW-SSR-32 — Node-specific Contour1 wire taxonomy axes

## Meta
- **Key:** `STORY-GW-SSR-32-node-specific-contour1-wire-axes`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** P1 — node-taxonomy Contour1 (sequence **32**)
- **Тип:** implement (Contour1 normalize + intake tests)
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-32-node-specific-contour1-wire-axes.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-32-node-specific-contour1-wire-axes.md)
- **Architecture:** D-SSR-11 · arch-doc 2026-09-04
- **Parent REQ:** 51
- **decision_ref:** backlog SSR-32
- **Skill declared:** python-pro
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000089-20260904-gw-ssr-32-node-specific-contour1-wire-axes.yaml`](../../../../gateway-active-packages/pkg-000089-20260904-gw-ssr-32-node-specific-contour1-wire-axes.yaml)
- **Git:** только `semantic-schema-runtime`
- **Зависит от:** soft SSR-31 Done (pkg-000088)
- **Parallel out:** SSR-33 docs
- **Scaffolded:** 2026-09-04T13:07:36Z
- **G32 PASS:** 2026-09-04T13:13:31Z · [`run-summary`](../../../../run-reports/run-summary-20260904-1313-gw-ssr-32-p3.md)

## Nested tasks (pkg-000089)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-ssr-32-t01-open-normalize-axis`](./task-gw-ssr-32-t01-open-normalize-axis/README.md) | Done |
| T02 | [`task-gw-ssr-32-t02-tests-custom-and-empty-wire`](./task-gw-ssr-32-t02-tests-custom-and-empty-wire/README.md) | Done |
| T03 | [`task-gw-ssr-32-t03-civic-skip-classic-regression`](./task-gw-ssr-32-t03-civic-skip-classic-regression/README.md) | Done |
| T04 | [`task-gw-ssr-32-t04-story-acceptance-gate`](./task-gw-ssr-32-t04-story-acceptance-gate/README.md) | Done · G32 |
| T05 | [`task-gw-ssr-32-t05-audit-g1-as-of-done-ssot`](./task-gw-ssr-32-t05-audit-g1-as-of-done-ssot/README.md) | Done · G1 CLOSED |

## As-of-Done (P3 2026-09-04T13:13:31Z)

| Fact | Ref |
|------|-----|
| Contour1 membership removed | `axes.py` `normalize_axis` — strip/lower only |
| Empty/non-str still rejected | ValueError / IntakeValidationError |
| Civic skip unmapped | `signals_from_story_labels` unchanged |
| Classic 13 wire | still parses |
| ClusterLens | still 10 |

## Scope / Out of scope

**In:** Open `normalize_axis`; wire tests; civic skip + classic 13.  
**Out:** Contour2; docs SSR-33; ClusterLens / vocabulary expand; §Актуальная точка.

## Target / AC

- [x] **AC-GW-SSR32-01…04** — see backlog · G32 PASS
