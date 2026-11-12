# task-gw-ssr-33-t01-schema-packs-readme-axes-contract

## Task: docs — schema-packs README Contour2 axes contract (T01)

## Meta
- **Story:** [STORY-GW-SSR-33](../STORY-GW-SSR-33-node-specific-taxonomy-docs-setup-tests-hygiene.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000090
- **Skill declared:** code-documenter
- **Depends on:** SSR-31 + SSR-32 Done
- **Scaffolded:** 2026-09-04T13:23:06Z
- **Closed:** 2026-09-04T13:28:42Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-33-node-specific-taxonomy-docs-setup-tests-hygiene.md`

## Purpose
Replace `schema-packs/README.md` axes row (L44 «must equal all 13» / ∈ frozen set) with pack-defined unique non-empty + structural notes; link D-SSR-11 / arch-doc; keep dispositions / internal / maps; tallinn = exemplar.

## Code Facts
1. **Historical (pre-P3):** `schema-packs/README.md` L44 `axes[]` ∈ `TAXONOMY_AXIS_VALUES` + set must equal all 13.
2. **As-of-Done:** README axes = node-defined (D-SSR-11 / SSR-31); lockstep only as negation; tallinn exemplar.
3. Runtime Contour2 — SSR-31 unlock shipped (no lockstep in resolver).
4. Arch — `docs/analysis/architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md` D-SSR-11.

## Gap
**As-of-Done:** Gap closed at P3 — README no longer requires Contour2 lockstep. G1 SSOT labels closed P6 2026-09-04T13:34:49Z.

## Acceptance / DoD
- [x] README axes = node-defined; no «must equal all 13»
- [x] Link D-SSR-11 / arch-doc; tallinn exemplar noted
- [x] dispositions / internal_axes / maps wording kept
- [x] No resolver / normalize_axis / GPT file edits
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/schema-packs/README.md`

## Out of scope
Product code; uus pack.json; GPT-SSR-15 file edit.
- Overlay bans (every task):
  - Docs/README/manual/setup/test inventory **only**.
  - **No** `resolver.py` Contour2 reopen; **no** `axes.py` / `normalize_axis` reopen.
  - **No** GPT UI file edit (GPT-SSR-15) unless operator expands scope — handoff note only.
  - **No** ClusterLens / vocabulary / uus pack.json product repair.
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Prefer README+manual+INDEX; avoid rewriting Done story bodies (SSR-26/29) unless necessary.

## Verification commands
```bash
rg -n "must equal all 13|TAXONOMY_AXIS_VALUES|D-SSR-11" doge-complaints-gateway/schema-packs/README.md
```
