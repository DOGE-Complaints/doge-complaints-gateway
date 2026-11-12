# task-gw-ssr-31-t05-story-acceptance-gate

## Task: analyze — story acceptance + G31 (T05)

## Meta
- **Story:** [STORY-GW-SSR-31](../STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md)
- **Type:** gate
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000088
- **Skill declared:** python-pro
- **Depends on:** T01–T04 Done
- **Scaffolded:** 2026-09-04T12:50:23Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md`

## Purpose
Story acceptance gate G31. PASS iff AC-GW-SSR31-01…05. Contour2 unlock proven; ClusterLens=10; no Contour1/docs/GPT-SSR-15; no §Актуальная точка rewrite.

## Code Facts
- Template — story-acceptance-gate-template.md
- Story AC — backlog SSR-31 Layer 1 + Layer 2 Concrete AC
- Arch — D-SSR-11

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-31.md` PASS/FAIL + evidence (P3)
- [x] `acceptance-verification-gw-ssr-31-t05.md` signed (Date post P3 live verify)
- [x] AC-GW-SSR31-01…05 covered
- [x] Live `--project gateway --verify` recorded
- [x] Resolver Contour2 grep-clean of accept/reject via `TAXONOMY_AXIS_VALUES`
- [x] Do **not** rewrite §«Актуальная точка»
- [x] BULLRUN phases complete

## Where to change
- This folder gate artifacts (P3)

## Out of scope
P3 invent Contour1/docs; uus pack.json; ClusterLens expand.
- Overlay bans (every task):
  - Contour2 only: drop membership + set-equality lockstep; keep structural validation.
  - **No** Contour1 `normalize_axis` (SSR-32).
  - **No** docs/README/manual rewrite (SSR-33).
  - **No** ClusterLens expand; **no** uus pack.json product edit; **no** GPT-SSR-15.
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not reopen 01–30 product beyond test adaptations required by Contour2 unlock.

## Verification commands
```bash
cd doge-complaints-gateway
rg -n "TAXONOMY_AXIS_VALUES" src/core/schema/resolver.py || true
.venv/bin/python -m pytest -q tests/test_gw_ssr_26_taxonomy_loader.py tests/test_gw_ssr_28_taxonomy_seed.py tests/test_gw_ssr_31_node_taxonomy_contour2.py --tb=short
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
