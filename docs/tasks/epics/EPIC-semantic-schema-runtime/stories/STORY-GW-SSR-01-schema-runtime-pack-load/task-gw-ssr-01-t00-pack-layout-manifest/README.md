# task-gw-ssr-01-t00-pack-layout-manifest

## Meta
- **Story:** [STORY-GW-SSR-01](../STORY-GW-SSR-01-schema-runtime-pack-load.md)
- **Type:** docs / contract
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000061
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-08-28T13:11:39Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-01-schema-runtime-pack-load.md` T00; INDEX **D-SSR-4**

## Purpose
Зафиксировать pack layout: `schema-packs/<schema_id>/<schema_version>/` + манифест, который loader умеет (JSON Schema file + representable field-policy states + ≥1 exact-lens block **shape** как CL-001 example). Example lens block **обязан** нести CL-003 conceptual tokens, которые SSR-05 мапит на существующий `PromotionGatePolicy` (только 3 knobs: `min_readiness_score`, `min_stories` ← `min_size`, `require_actionable_canonical_type=false` для pack). Числа — **в файле example pack**, не копировать civic `70`/`2` в Python default. Имена ключей манифеста — **только этот loader**, таблица в README.

## Code Facts
- Packs dir **not found** — Glob `doge-complaints-gateway/schema-packs/**` = 0 (P1 scaffold)
- Runtime dir **not found** — Glob `src/core/schema/` = 0
- D-SSR-4 layout — [`INDEX.md`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md) `src/core/schema/` vs `schema-packs/<schema_id>/<schema_version>/`
- Civic promotion knobs (map later SSR-05; numbers **not** copied into Python default here) — [`gates.py:11–14`](../../../../../../../src/core/promotion/gates.py)
- T00 is loader-only on-disk contract — story §«Стыковка с кодом»; SCHEMA-003 keys not frozen

## Acceptance / DoD
- [x] Traces story T00: layout `schema-packs/<schema_id>/<schema_version>/` documented
- [x] `schema-packs/README.md` names loader-only manifest keys (table); not a frozen universal YAML dialect
- [x] Example pack ids `legal_process.v1` / `mobility_observation.v1` (parent §29 Integration)
- [x] Example lens block shape carries CL-003 conceptual tokens for 3 knobs; numbers in example pack files
- [x] T03/T04 blocked until this Done (noted in Depends of those tasks)
- [x] BULLRUN phases complete

## Where to change
- New `doge-complaints-gateway/schema-packs/README.md`
- Example packs under `schema-packs/legal_process/<version>/` and `schema-packs/mobility_observation/<version>/` (ids from story T00)

## Out of scope
- Frozen «универсальный YAML диалект»; domain fields в parser; второй диалект readiness в SSR-05
- Implementing `SchemaRuntime` / resolver / validator (T02–T04); `jsonschema` dep (T01)
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

## Verification commands
```bash
ls -la doge-complaints-gateway/schema-packs/
rg -n 'legal_process|mobility_observation|min_readiness_score|min_stories|require_actionable_canonical_type' doge-complaints-gateway/schema-packs/
```
