# task-gw-ssr-33-t02-manual-operator-setup-usage

## Task: docs — operator manual dual contour + setup/usage (T02)

## Meta
- **Story:** [STORY-GW-SSR-33](../STORY-GW-SSR-33-node-specific-taxonomy-docs-setup-tests-hygiene.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000090
- **Skill declared:** code-documenter
- **Depends on:** T01
- **Scaffolded:** 2026-09-04T13:23:06Z
- **Closed:** 2026-09-04T13:28:42Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-33-node-specific-taxonomy-docs-setup-tests-hygiene.md`

## Purpose
Update `docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md` taxonomy dual-contour: node axes; Contour1 open; Contour2 pack-owned; civic skip; tallinn exemplar; authoring steps (backlog Layer 2 list 1–6). Optional short «Authoring node taxonomy» subsection.

## Code Facts
1. **Historical (pre-P3):** Manual SSR-29 dual contour — likely lockstep / no D-SSR-11 authoring steps.
2. **As-of-Done:** Manual §Taxonomy dual contour (D-SSR-11) + §Authoring node taxonomy steps 1–6 + GPT-SSR-15 invert note.
3. Runtime — Contour1 open (SSR-32); Contour2 pack-owned (SSR-31); civic skip unmapped.

## Gap
**As-of-Done:** Gap closed at P3 — manual describes D-SSR-11. G1 SSOT labels closed P6 2026-09-04T13:34:49Z.

## Acceptance / DoD
- [x] Manual §taxonomy: Contour1 open + Contour2 pack-owned + civic skip + tallinn exemplar
- [x] Operator setup steps 1–6 landed (or equivalent subsection)
- [x] Arch-doc / D-SSR-11 linked
- [x] No product code / GPT file edit
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md`

## Out of scope
Product code; uus pack.json; GPT file edit.
- Overlay bans (every task):
  - Docs/README/manual/setup/test inventory **only**.
  - **No** `resolver.py` Contour2 reopen; **no** `axes.py` / `normalize_axis` reopen.
  - **No** GPT UI file edit (GPT-SSR-15) unless operator expands scope — handoff note only.
  - **No** ClusterLens / vocabulary / uus pack.json product repair.
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Prefer README+manual+INDEX; avoid rewriting Done story bodies (SSR-26/29) unless necessary.

## Verification commands
```bash
rg -n "D-SSR-11|Authoring node taxonomy|GPT-SSR-15|Contour1|Contour2" doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
```
