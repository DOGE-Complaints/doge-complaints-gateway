# task-gw-ssr-01-t10-audit-g3-nesting-depth-test

## Meta
- **Story:** [STORY-GW-SSR-01](../STORY-GW-SSR-01-schema-runtime-pack-load.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000061 (parent product Done); wave `run_mode=gw_ssr_01_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-01
- **Depends on:** T00–T07 Done
- **Audit ref:** [`audit-gw-ssr-01-schema-runtime-pack-load-2026-08-28.md`](../../../../../../analysis/audit-gw-ssr-01-schema-runtime-pack-load-2026-08-28.md) **G3**
- **Scaffolded:** 2026-08-28T13:26:25Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-01_gap_20260828T132458Z.plan.md` G3 TASKED follow_up=none

## Purpose
Один unit-тест: payload глубже `MAX_NESTING_DEPTH` (32) → `PolicyViolationError`. Лимит уже в коде. Не invent новый product threshold. Не менять константу.

## Code Facts
- Limit — [`validator.py:21`](../../../../../../../src/core/schema/validator.py) `MAX_NESTING_DEPTH = 32`; enforce [`:108–109`](../../../../../../../src/core/schema/validator.py)
- Helper `nesting_depth` — [`validator.py:28–37`](../../../../../../../src/core/schema/validator.py)
- Oversized covered — `test_oversized_payload_rejected` in [`tests/test_gw_ssr_01_schema_runtime.py`](../../../../../../../tests/test_gw_ssr_01_schema_runtime.py)
- Nesting covered — `test_payload_deeper_than_max_nesting_depth_rejected` (P6). **Historical (pre-P6):** tests Grep `MAX_NESTING_DEPTH` under `tests/` = empty (audit G3)
- Story T04 / SEC-002 names nesting

## Acceptance / DoD
- [x] Test in `tests/test_gw_ssr_01_*.py`: nested mapping/list depth > 32 raises `PolicyViolationError` (`code == policy_violation`)
- [x] `MAX_NESTING_DEPTH` unchanged (still 32)
- [x] `test_clustering_engine.py` untouched
- [x] P5 this file only; implementation + pytest in **P6**
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-01-t10.md` signed (Date post P6 verify only)

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_01_schema_runtime.py` (add test in P6)
- Do **not** change `src/core/schema/validator.py` constants unless a bug is proven (not this gap)

## Out of scope
- G1/G2 docs; changing SEC-002 numbers; homemade validator; `test_clustering_engine.py`
- INDEX/runbook §4 bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py` :106–109).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :336).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:29–43`).
  - Не invent HTTP filter / новый intake path.
  - Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3).
  - Не реализовывать SSR-06/07 (`story_dimensions`, processor pipeline).
  - `build_index` / `project` — stub/no-op, не «working IDX/PROC».
  - Semantic persist field = `bound_schema_version`, не вторая колонка `schema_version`.
  - Pack cluster_id namespace `schema:…`; не `stable_cluster_id(ClusterLens, …)`.
  - Civic `_persist_memberships` / `_create_issue_for_cluster` as-is не использовать для pack.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».

## Verification commands
```bash
# P6 only:
rg -n 'MAX_NESTING_DEPTH|nesting_depth' doge-complaints-gateway/tests/test_gw_ssr_01_*.py
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" tests/test_gw_ssr_01_*.py
```
