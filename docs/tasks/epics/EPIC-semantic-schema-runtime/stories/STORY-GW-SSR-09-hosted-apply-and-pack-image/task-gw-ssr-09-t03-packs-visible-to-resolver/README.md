# task-gw-ssr-09-t03-packs-visible-to-resolver

## Task: tests — schema-packs tree + resolver contract

## Meta
- **Story:** [STORY-GW-SSR-09](../STORY-GW-SSR-09-hosted-apply-and-pack-image.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000067
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-29T18:09:45Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-09-hosted-apply-and-pack-image.md` T03

## Purpose
`schema-packs/` present so resolver default finds an example pack (`legal_process/v1` and/or `tallinn_civic/v1`). If process CWD ≠ gateway root, use `SCHEMA_PACKS_ROOT` on volume/image — **do not** add `AppConfig` field (absent — fact). Dockerfile **Not found** — do not invent; record current build fact (Railway/Nixpacks root copies sources). Live image = operator, not overnight proof.

## Code Facts
- Resolver — [`resolver.py:19–30`](../../../../../../../src/core/schema/resolver.py) `SCHEMA_PACKS_ROOT` or `parents[3] / "schema-packs"`
- `SCHEMA_PACKS_ROOT` in `AppConfig` — **Not found** (`src/core/config/` Grep empty)
- Dockerfile in gateway — **Not found** (Glob 0)
- Packs on disk — `schema-packs/legal_process/v1`, `mobility_observation/v1`, `tallinn_civic/v1`
- Manual — [`schema-packs-node-data-model-ru.md`](../../../../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md)

## Acceptance / DoD
- [x] `test -d schema-packs`
- [x] Example pack resolves via `default_packs_root` (loader keys)
- [x] Document CWD ≠ root → `SCHEMA_PACKS_ROOT` (no `AppConfig` field)
- [x] No new Dockerfile
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/schema-packs/` (already on disk)
- Optional `tests/test_gw_ssr_09_*` for resolver + example pack load
- Manual deploy sentence if missing — **not** a new Dockerfile

## Out of scope
- Invent Dockerfile; invent HTTP; change `AppConfig`
- `unknown schema` fix via new engine
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py:108–111`).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:30–44`).
  - Не invent HTTP filter / IDX/QRY. `GET /tallinn/issues` stays (`asgi_app.py` :462).
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/10/12. Не reopen SSR-08.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0[1-5]*`.
  - `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Overlay UI spa-app — **not this story**.
  - Не invent Dockerfile.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
test -d doge-complaints-gateway/schema-packs
test -f doge-complaints-gateway/schema-packs/legal_process/v1/pack.json
rg -n "SCHEMA_PACKS_ROOT|default_packs_root" doge-complaints-gateway/src/core/schema/resolver.py
rg -n "SCHEMA_PACKS_ROOT" doge-complaints-gateway/src/core/config || true
```
