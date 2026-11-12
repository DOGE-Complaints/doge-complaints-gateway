# STORY-GW-SSR-29 — taxonomy docs + operator copy-paste seam

## Meta
- **Key:** `STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** P2 — taxonomy-pack wave capstone (sequence **29**)
- **Тип:** documentation + operator seam
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md)
- **Parent REQ:** 51
- **decision_ref:** backlog SSR-29
- **Skill declared:** python-pro
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000086-20260901-gw-ssr-29-taxonomy-docs-operator-copy-paste-seam.yaml`](../../../../gateway-active-packages/pkg-000086-20260901-gw-ssr-29-taxonomy-docs-operator-copy-paste-seam.yaml)
- **Git:** только `semantic-schema-runtime`
- **Зависит от:** SSR-26 Done; SSR-28 Done
- **Feeds:** GPT-SSR-05 / GPT-SSR-06 / GPT-SSR-09
- **Scaffolded:** 2026-09-01T13:43:47Z
- **G29 PASS:** 2026-09-01T13:49:03Z · [`run-summary`](../../../../run-reports/run-summary-20260901-1349-gw-ssr-29-p3.md)

## Nested tasks (pkg-000086)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-ssr-29-t01-manual-taxonomy-copy-paste`](./task-gw-ssr-29-t01-manual-taxonomy-copy-paste/README.md) | Done |
| T02 | [`task-gw-ssr-29-t02-schema-packs-readme-crosslink`](./task-gw-ssr-29-t02-schema-packs-readme-crosslink/README.md) | Done |
| T03 | [`task-gw-ssr-29-t03-gateway-index-hygiene`](./task-gw-ssr-29-t03-gateway-index-hygiene/README.md) | Done |
| T04 | [`task-gw-ssr-29-t04-story-checklist-canonical`](./task-gw-ssr-29-t04-story-checklist-canonical/README.md) | Done |
| T05 | [`task-gw-ssr-29-t05-cross-repo-handoff`](./task-gw-ssr-29-t05-cross-repo-handoff/README.md) | Done |
| T06 | [`task-gw-ssr-29-t06-story-acceptance-gate`](./task-gw-ssr-29-t06-story-acceptance-gate/README.md) | Done · G29 |

## Зачем простыми словами

Docs + checklist so gateway `schema-packs/` is SSOT and GPT gets byte-identical three-JSON copy. No implement code; no GPT UI materialize in this pkg.

## Scope / Out of scope

**In:** manual taxonomy/copy-paste; README cross-link; INDEX hygiene; story checklist lockstep; handoff paths; gate.

**Out:** GPT operator manual rewrite; code; GPT JSON commit from gateway P3; §Актуальная точка rewrite.

## As-of-Done (P3 2026-09-01T13:49:03Z)

| Fact | Ref |
|------|-----|
| Manual 3-file + dual contour + copy-paste 1–6 + deprecation | `docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md` |
| Geo § (SSR-27) + taxonomy § coexist | same manual |
| README → manual | `schema-packs/README.md` |
| INDEX wave 26/28/29 Done + GPT siblings | `backlog-stories/semantic-schema-runtime/INDEX.md` |
| Handoff path table | manual §Operator copy-paste |
| Explicit | gateway P3 does **not** edit GPT UI / commit GPT JSON |

## Target / AC

- [x] **AC-GW-SSR29-01…06** — see backlog · G29 PASS
