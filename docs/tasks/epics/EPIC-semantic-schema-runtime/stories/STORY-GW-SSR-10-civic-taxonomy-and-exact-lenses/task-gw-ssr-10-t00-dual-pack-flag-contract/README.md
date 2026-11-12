# task-gw-ssr-10-t00-dual-pack-flag-contract

## Task: implement — pack dual vs exact-only flag (R1)

## Meta
- **Story:** [STORY-GW-SSR-10](../STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000068
- **Skill declared:** python-pro
- **Depends on:** SSR-04 Done (loader / `exact_lenses`)
- **Scaffolded:** 2026-08-29T18:25:31Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md` R1

## Purpose
Имя+семантика pack-флага dual vs exact-only; default exact-only (`legal_process` без ключа). Ключ loader — refine, **не** invent frozen YAML-диалект. Document in `schema-packs/README.md` after name is chosen (SCHEMA-005: один loader). Loader/resolver reads flag; absent/false = current exact-only. G10: pack without dual key = T-wave exact-only.

## Code Facts
- Resolver `exact_lenses` required — [`resolver.py:91–93`](../../../../../../../src/core/schema/resolver.py); no dual key parsed
- Loader keys — [`schema-packs/README.md`](../../../../../../../schema-packs/README.md) — нет civic-lens / dual блока
- Pack algorithm exact-only — [`pack_engine.py:100–101`](../../../../../../../src/core/schema/pack_engine.py)
- G10 — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.3

## Acceptance / DoD
- [ ] Pack MAY объявить dual; absent/false = T-wave поведение
- [ ] Default exact-only for packs without the key (`legal_process` stays exact-only)
- [ ] Key name documented in `schema-packs/README.md` after refine (not frozen dialect)
- [ ] Existing packs not required to add civic-lens block
- [ ] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/schema/contracts.py`
- `doge-complaints-gateway/src/core/schema/resolver.py`
- `doge-complaints-gateway/schema-packs/README.md` (table row)

## Out of scope
- Frozen диалект до refine; require dual on `legal_process` / `tallinn_civic` by default
- Always civic for any binding; expand `ClusterLens`
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79) как default для всех packs.
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py:108–111`).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:30–44`).
  - Не invent HTTP filter / IDX/QRY. `GET /tallinn/issues` stays (`asgi_app.py` :462).
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/11/12/13. Не reopen 01–05/08/09.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0[1-5]*`.
  - `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Overlay UI spa-app — **not this story**.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n "exact_lenses|dual" doge-complaints-gateway/src/core/schema/resolver.py \
  doge-complaints-gateway/src/core/schema/contracts.py
rg -n "dual|civic-lens" doge-complaints-gateway/schema-packs/README.md || true
test -f doge-complaints-gateway/schema-packs/legal_process/v1/pack.json
```
