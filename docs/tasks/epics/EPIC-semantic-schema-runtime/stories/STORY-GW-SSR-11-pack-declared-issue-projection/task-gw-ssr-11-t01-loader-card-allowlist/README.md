# task-gw-ssr-11-t01-loader-card-allowlist

## Task: implement — loader reads card allowlist (T01)

## Meta
- **Story:** [STORY-GW-SSR-11](../STORY-GW-SSR-11-pack-declared-issue-projection.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000070
- **Skill declared:** python-pro
- **Depends on:** T00 (key name refined)
- **Scaffolded:** 2026-08-29T19:08:43Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-11-pack-declared-issue-projection.md` T01

## Purpose
Read allowlist from `pack.json` via `load_pack`; default (absent/empty) = nothing beyond civic card. Existing packs `legal_process` / `tallinn_civic` без ключа stay civic-form.

## Code Facts
- Loader `load_pack` — [`resolver.py:73–117`](../../../../../../../src/core/schema/resolver.py) no card-fields key
- `SchemaContext` — [`contracts.py:52–59`](../../../../../../../src/core/schema/contracts.py)
- Loader table — [`schema-packs/README.md:20–28`](../../../../../../../schema-packs/README.md)
- Dual key precedent — [`resolver.py:38–47`](../../../../../../../src/core/schema/resolver.py) `_parse_dual_civic_lenses`

## Acceptance / DoD
- [x] Loader reads allowlist dotted paths from `pack.json` (key from T00)
- [x] Absent/empty = ничего сверх civic card
- [x] `legal_process` / `tallinn_civic` without the key stay civic-form
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/schema/resolver.py` (`:73–117`)
- `doge-complaints-gateway/src/core/schema/contracts.py` (`:52–59`)
- `doge-complaints-gateway/schema-packs/README.md`

## Out of scope
- Проецировать весь payload; change civic `field_policy` enforcement semantics for all packs
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py:108–111`).
  - Не invent HTTP filter / IDX/QRY / `story_dimensions`. `GET /node/issues` stays (`asgi_app.py:462`).
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/12/14/15. Не reopen 01–05/08–10/13.
  - Не вызывать / не реализовывать `SchemaRuntime.project` (stub `runtime.py:68–72` stays `NotImplementedError`).
  - Не dump `structured_payload` на карточку; не проецировать `forbidden` / `node_private`.
  - Overlay UI spa-app — **not this story**.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0[1-5]*`.
  - `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n "load_pack|field_policy" doge-complaints-gateway/src/core/schema/resolver.py
test -f doge-complaints-gateway/schema-packs/legal_process/v1/pack.json
test -f doge-complaints-gateway/schema-packs/tallinn_civic/v1/pack.json
```
