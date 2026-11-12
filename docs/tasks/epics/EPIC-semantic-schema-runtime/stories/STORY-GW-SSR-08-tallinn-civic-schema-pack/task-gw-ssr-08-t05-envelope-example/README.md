# task-gw-ssr-08-t05-envelope-example

## Meta
- **Story:** [STORY-GW-SSR-08](../STORY-GW-SSR-08-tallinn-civic-schema-pack.md)
- **Type:** docs
- **Status:** 🔵 Done
- **Package:** pkg-000066
- **Skill declared:** python-pro
- **Depends on:** T00
- **Scaffolded:** 2026-08-29T17:47:38Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-08-tallinn-civic-schema-pack.md` T05

## Purpose
Пример envelope (verbatim JSON из `$storyFile`) в этой стори / мануал; optional contract test fixture. Не менять GPT UI.

## Code Facts
- Example JSON — [`STORY-GW-SSR-08-….md`](../STORY-GW-SSR-08-tallinn-civic-schema-pack.md) §Пример envelope (gateway; не GPT UI)
- Backlog keep — [`STORY-GW-SSR-08-tallinn-civic-schema-pack.md`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-08-tallinn-civic-schema-pack.md)
- Manual — [`schema-packs-node-data-model-ru.md`](../../../../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md)
- Wire already parses `schema_binding` — SSR-03 Done; this task is gateway example only

## Acceptance / DoD
- [x] Traces story T05: `schema_binding` envelope example in gateway repo (not GPT UI)
- [x] Narrative title/description still required; payload does not replace civic envelope
- [x] No `GPT UI/` instruction pack; no spa-16 overlay
- [x] BULLRUN phases complete

## Where to change
- `$storyFile` keep; pipeline story copy; `docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md` and/or `tests/` fixture. **Not** `GPT UI/`.

## Out of scope
- `GPT UI/` instruction pack; overlay spa-16
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22). 10 members stay.
  - Не править `lens_dimension` под pack (`engine.py` :66–79). Pack **не** via civic `lens_dimension`.
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py:108–111`).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:30–44`).
  - Не invent HTTP filter / новый intake path / IDX/QRY. `GET /tallinn/issues` stays (`asgi_app.py` :462).
  - Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3). Не менять identity handlers (`handlers.py` :221).
  - Не реализовывать / не ставить в очередь SSR-06/07/12.
  - `build_index` / `project` — stub/no-op (`runtime.py` :62–72).
  - Не переименовывать `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0*`.
  - Civic path без binding **must stay**.
  - Overlay UI spa-app — **not this story**.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не новый Python engine; не прогонять bound story через civic engine (dual → SSR-10).
  - Pack cluster_id namespace `schema:…`; civic `_persist_memberships` / `_create_issue_for_cluster` as-is не для pack.

## Verification commands
```bash
rg -n "tallinn_civic" doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-08-tallinn-civic-schema-pack.md
rg -n "schema_binding" doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md || true
test ! -d "GPT UI" || rg -L "instruction pack" --glob '*tallinn_civic*' "GPT UI" || true
```
