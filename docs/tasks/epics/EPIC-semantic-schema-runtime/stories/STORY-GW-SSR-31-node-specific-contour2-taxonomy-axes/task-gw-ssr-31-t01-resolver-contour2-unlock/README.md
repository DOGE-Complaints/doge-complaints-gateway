# task-gw-ssr-31-t01-resolver-contour2-unlock

## Task: implement — Contour2 unlock in `_parse_taxonomy_pack` (T01)

## Meta
- **Story:** [STORY-GW-SSR-31](../STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000088
- **Skill declared:** python-pro
- **Depends on:** SSR-26 Done
- **Scaffolded:** 2026-09-04T12:50:23Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md`

## Purpose
Remove Contour2 axis membership + set-equality lockstep against `TAXONOMY_AXIS_VALUES` in `_parse_taxonomy_pack`. Keep non-empty/dupe loop and structural validation. Do **not** change Contour1 `normalize_axis`.

## Code Facts
1. **As-of-Done (SSR-31 pkg-000088):** Contour2 unlock — `_parse_taxonomy_pack` keeps non-empty + dupe only; no `TAXONOMY_AXIS_VALUES` in `resolver.py` (`rg` empty).
2. **As-of-Done:** structural checks remain — `internal_axes ⊆ axes`; keys ∈ axes; dispositions enum.
3. Optional Contour2 — absent `taxonomy_schema` → `taxonomy is None`.
4. **Historical (pre-P3):** Lockstep reject L293–303 (`unknown axis` + `must equal all 13`); import `TAXONOMY_AXIS_VALUES`.

## Gap
**Closed (P3):** node packs with ≠13 axes load when structurally valid (e.g. uus-shaped 24). **Historical gap:** «Node packs ≠13 cannot load Contour2 despite valid structure».

## Acceptance / DoD
- [x] Membership + set-equality block removed; non-empty + duplicate axis checks remain
- [x] Structural rejects unchanged
- [x] Contour2 path does not accept/reject via `TAXONOMY_AXIS_VALUES` (import unused → remove if clean)
- [x] No Contour1 / ClusterLens / docs edits
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/src/core/schema/resolver.py` (`_parse_taxonomy_pack`)

## Out of scope
Contour1 (→SSR-32). Docs (→SSR-33). uus pack.json. GPT-SSR-15.
- Overlay bans (every task):
  - Contour2 only: drop membership + set-equality lockstep; keep structural validation.
  - **No** Contour1 `normalize_axis` (SSR-32).
  - **No** docs/README/manual rewrite (SSR-33).
  - **No** ClusterLens expand; **no** uus pack.json product edit; **no** GPT-SSR-15.
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not reopen 01–30 product beyond test adaptations required by Contour2 unlock.

## Verification commands
```bash
rg -n "TAXONOMY_AXIS_VALUES|unknown axis|must equal all 13" doge-complaints-gateway/src/core/schema/resolver.py
```
