# task-gw-ssr-02-t10-audit-g2-sqlite-save-return-hash

## Meta
- **Story:** [STORY-GW-SSR-02](../STORY-GW-SSR-02-structured-payload-persist.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000062 (parent product Done); wave `run_mode=gw_ssr_02_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-02
- **Depends on:** T00–T08 Done
- **Audit ref:** [`audit-gw-ssr-02-structured-payload-persist-2026-08-28.md`](../../../../../../analysis/audit-gw-ssr-02-structured-payload-persist-2026-08-28.md) **G2**
- **Scaffolded:** 2026-08-28T13:53:59Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-02_gap_20260828T135245Z.plan.md` G2 TASKED follow_up=none

## Purpose
Adapter parity: `SqliteStoryRepository.save_story` returns a record whose `payload_hash` is `authoritative_payload_hash` (same as in-memory `replace`), not the client-supplied digest on the input object. Persist write path already hashes. Do not invent a new hash algorithm.

## Code Facts
- sqlite write uses `_binding_bind` → `authoritative_payload_hash` — [`db_sqlite.py:80–88`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- sqlite **return** is input `record` — [`db_sqlite.py:689`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- In-memory `replace`s hash before store+return — [`repositories.py:59–73`](../../../../../../../src/core/infrastructure/repositories.py)
- Hash helper — [`payload.py`](../../../../../../../src/core/schema/payload.py) `authoritative_payload_hash` / `payload_hash_for`
- Tests today assert via `get_story`, not sqlite `save_story` return — [`tests/test_gw_ssr_02_structured_payload_persist.py`](../../../../../../../tests/test_gw_ssr_02_structured_payload_persist.py)
- DATA-004 persist = OK (audit G2)

## Acceptance / DoD
- [x] `SqliteStoryRepository.save_story` return `payload_hash` equals `authoritative_payload_hash(structured_payload)` (prefer `dataclasses.replace`, same as memory)
- [x] Client-supplied hash on the input record is not the returned digest
- [x] Hash algorithm unchanged (`payload_hash_for` / canonical JSON)
- [x] Test in `tests/test_gw_ssr_02_*.py` asserts sqlite **return** (not only `get_story`)
- [x] `test_clustering_engine.py` untouched
- [x] P5 this file only; implementation + pytest in **P6**
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-02-t10.md` signed (Date post P6 verify only)

## Where to change
- `doge-complaints-gateway/src/core/infrastructure/db_sqlite.py` (`save_story` return; P6)
- `doge-complaints-gateway/tests/test_gw_ssr_02_structured_payload_persist.py` (assert return digest; P6)

## Out of scope
- G1 docs SSOT (T09); G3 bullrun §Актуальная точка
- New hash algorithm; `schema_binding` intake (SSR-03); CREATE TABLE rewrite
- INDEX/runbook §4 bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py` :106–109).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:29–43`).
  - Не invent HTTP filter / новый intake path.
  - Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3).
  - Не реализовывать SSR-06/07 (`story_dimensions`, processor pipeline).
  - `build_index` / `project` — stub/no-op, не «working IDX/PROC».
  - Semantic persist field = `bound_schema_version`, не вторая колонка `schema_version`.
  - Pack cluster_id namespace `schema:…`; не `stable_cluster_id(ClusterLens, …)`.
  - Civic `_persist_memberships` / `_create_issue_for_cluster` as-is не использовать для pack.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`.

## Verification commands
```bash
# P6 only:
rg -n 'return record|authoritative_payload_hash|replace\(' doge-complaints-gateway/src/core/infrastructure/db_sqlite.py
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" tests/test_gw_ssr_02_*.py
```
