# task-gw-ssr-31-t04-tests-uus-shaped-contour2-load

## Task: tests — uus-shaped Contour2 load SUCCESS (T04)

## Meta
- **Story:** [STORY-GW-SSR-31](../STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000088
- **Skill declared:** python-pro
- **Depends on:** T01 (preferably T02)
- **Scaffolded:** 2026-09-04T12:50:23Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md`

## Purpose
Preferred home `tests/test_gw_ssr_31_node_taxonomy_contour2.py`: prove uus-shaped / 24-axis (or other ≠`TAXONOMY_AXIS_VALUES`) tmp pack with `taxonomy_schema` **loads**; `ctx.taxonomy.axes` matches file. Also AC-05: legal/mobility without `taxonomy_schema` → `taxonomy is None`. ClusterLens stays 10.

## Code Facts
1. Story AC-01/05 — backlog Layer 2 Concrete AC.
2. tmp_path nested `schema-packs/<id>/<ver>/` — SSR-26 pattern.
3. Fixtures may use minimal N-axis stub with matching maps (no uus pack.json product edit).

## Gap
No dedicated SUCCESS proof that Contour2 accepts node-defined ≠13 axes after unlock.

## Acceptance / DoD
- [x] ≠13 structurally valid tmp pack → `resolve_pack` SUCCESS; axes match file
- [x] legal/mobility → `taxonomy is None`
- [x] `len(ClusterLens)==10`
- [x] No uus `pack.json` edit in product tree
- [x] Targeted pytest green
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_31_node_taxonomy_contour2.py` (new)

## Out of scope
Docs SSR-33. Contour1. uus readiness_policy repair. GPT-SSR-15.
- Overlay bans (every task):
  - Contour2 only: drop membership + set-equality lockstep; keep structural validation.
  - **No** Contour1 `normalize_axis` (SSR-32).
  - **No** docs/README/manual rewrite (SSR-33).
  - **No** ClusterLens expand; **no** uus pack.json product edit; **no** GPT-SSR-15.
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not reopen 01–30 product beyond test adaptations required by Contour2 unlock.

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_ssr_31_node_taxonomy_contour2.py --tb=short
```
