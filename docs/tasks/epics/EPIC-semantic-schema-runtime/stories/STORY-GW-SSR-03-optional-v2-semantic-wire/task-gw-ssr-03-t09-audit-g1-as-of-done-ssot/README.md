# task-gw-ssr-03-t09-audit-g1-as-of-done-ssot

## Meta
- **Story:** [STORY-GW-SSR-03](../STORY-GW-SSR-03-optional-v2-semantic-wire.md)
- **Type:** docs
- **Status:** 🔵 Done
- **Package:** pkg-000063 (parent product Done); wave `run_mode=gw_ssr_03_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-03
- **Depends on:** T01–T08 Done
- **Audit ref:** [`audit-gw-ssr-03-optional-v2-semantic-wire-2026-08-28.md`](../../../../../../analysis/audit-gw-ssr-03-optional-v2-semantic-wire-2026-08-28.md) **G1**
- **Scaffolded:** 2026-08-28T14:21:18Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-03_gap_20260828T142007Z.plan.md` G1 TASKED follow_up=none

## Purpose
As-of-Done vs Historical split для persistent SSOT: backlog + pipeline SSR-03 §Verified still present-tense pre-P3 (`schema_binding` parsed **Not found**; envelope 6-tuple; persist envelope only; DI SchemaRuntime ещё нет). Без runtime parser/persist. INDEX persist/stash seams already As-of-Done — do not regress.

## Code Facts
- Parser — [`contracts.py:227`](../../../../../../../src/core/intake/contracts.py) `_parse_schema_binding_block`; `SCHEMA_BINDING_ALLOWED_KEYS` [`:92–100`](../../../../../../../src/core/intake/contracts.py)
- Fields — `StoryDraftStashRequest` [`:122`](../../../../../../../src/core/intake/contracts.py); `StoryIntakeRequest` [`:137`](../../../../../../../src/core/intake/contracts.py)
- Envelope body 7-tuple — `_parse_story_envelope_body` return [`:480–491`](../../../../../../../src/core/intake/contracts.py) includes `schema_binding`
- Factory — [`service_factory.py:85`](../../../../../../../src/core/infrastructure/service_factory.py) `schema_runtime=LocalSchemaRuntime()`
- Validate before save — [`services.py:246–262`](../../../../../../../src/core/application/services.py)
- Stale backlog §Verified — split applied (As-of-Done vs Historical) in [`STORY-GW-SSR-03`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-03-optional-v2-semantic-wire.md)
- Stale pipeline §Verified — split applied (same) in [`pipeline`](../STORY-GW-SSR-03-optional-v2-semantic-wire.md)
- INDEX persist/stash already As-of-Done — [`INDEX.md`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md) (P3 recount); do not rewrite as Historical-only
- Product Status 🔵 Done; gate PASS 2026-08-28T14:13:05Z

## Acceptance / DoD
- [x] Backlog SSR-03 §Verified current state: Current (`schema_binding` parsed; 7-tuple; factory wires `LocalSchemaRuntime`; persist map when present) vs Historical (pre-P3 Not found / 6-tuple / envelope-only / DI ещё нет)
- [x] Pipeline SSR-03 §Verified: same As-of-Done vs Historical split (keep in sync with backlog)
- [x] INDEX persist/stash As-of-Done rows not reverted
- [x] No `src/` / OpenAPI / intake runtime edits
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-03-t09.md` signed (Date post P6 verify only)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-03-optional-v2-semantic-wire.md` (§Verified current state)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-03-optional-v2-semantic-wire/STORY-GW-SSR-03-optional-v2-semantic-wire.md` (§Verified current state)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Runtime parser / persist / hash / factory algorithm
- INDEX/runbook §4 + §8 bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py` :102–109).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:29–43`).
  - Не invent HTTP filter / новый intake path. OpenAPI only existing paths. `GET /tallinn/issues` must stay (`asgi_app.py` :462).
  - Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3). Не менять identity handlers (`handlers.py` :221).
  - Не реализовывать SSR-06/07 (`story_dimensions`, processor pipeline).
  - `build_index` / `project` — stub/no-op, не «working IDX/PROC».
  - Semantic persist field = `bound_schema_version`, не вторая колонка `schema_version`.
  - Pack cluster_id namespace `schema:…`; не `stable_cluster_id(ClusterLens, …)`.
  - Civic `_persist_memberships` / `_create_issue_for_cluster` as-is не использовать для pack.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`.
- SSR-03 extras: sidecar only; `payload_hash` not on the wire; no new envelope enum.

## Verification commands
```bash
rg -n 'Not found|6-tuple|SchemaRuntime ещё нет|schema_version=request.schema_version only' \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-03-optional-v2-semantic-wire.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-03-optional-v2-semantic-wire/STORY-GW-SSR-03-optional-v2-semantic-wire.md
rg -n '_parse_schema_binding_block|LocalSchemaRuntime' \
  doge-complaints-gateway/src/core/intake/contracts.py \
  doge-complaints-gateway/src/core/infrastructure/service_factory.py
```
