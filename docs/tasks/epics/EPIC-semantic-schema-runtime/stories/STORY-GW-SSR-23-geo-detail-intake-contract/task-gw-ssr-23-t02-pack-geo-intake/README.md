# task-gw-ssr-23-t02-pack-geo-intake

## Task: implement — loader `geo_intake` + three packs (T02)

## Meta
- **Story:** [STORY-GW-SSR-23](../STORY-GW-SSR-23-geo-detail-intake-contract.md)
- **Type:** implement
- **Status:** 🔵 Done · P4 PASS 2026-08-30T20:44:21Z
- **Package:** pkg-000080
- **Skill declared:** python-pro
- **Depends on:** T00
- **Scaffolded:** 2026-08-30T20:29:24Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-23-geo-detail-intake-contract.md` T02

## Purpose
Загрузить pack блок `geo_intake` (`mode` / `merge` / `mirror_to_payload`). Три packs хотя бы `optional`. Не env override поверх pack.

## Code Facts
1. **As-of-Done:** `geo_intake` on three packs (`mode=optional`) — `schema-packs/tallinn_civic/v1/pack.json`, `legal_process/v1/pack.json`, `mobility_observation/v1/pack.json`.
2. **As-of-Done:** loader `_parse_geo_intake` required — [`resolver.py:254`](../../../../../../../src/core/schema/resolver.py), [`:343`](../../../../../../../src/core/schema/resolver.py).
3. **As-of-Done:** Tallinn payload `geo.*` (district…houses) — [`payload.schema.json:23–38`](../../../../../../../schema-packs/tallinn_civic/v1/payload.schema.json).
4. **Historical (pre-SSR-23):** `geo_intake` absent; payload `geo.district` only.

## Acceptance / DoD
- [x] Loader parse+validate `geo_intake.mode` = `optional` \| `require_location_or_detail` \| `require_detail`
- [x] Три packs содержат `geo_intake` (хотя бы optional)
- [x] Нет env override
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/schema/` (loader / context)
- `doge-complaints-gateway/schema-packs/*/v1/pack.json`
- payload.schema `geo.*` paths as story In

## Out of scope
- Env override. SQL (→24). Merge wire (T03).
- Overlay bans (every task):
  - Parse `geo_detail`; pack `geo_intake`; three packs; tests `test_gw_ssr_23_*`.
  - **No SQL migration** (→24). Do not add street/houses columns this pkg.
  - **No ClusterLens add/remove.** Enum stays 10 (`types.py:10–22`).
  - **Нет `GET /schema-active`.** Нет IDX / QRY. Нет GPT UI.
  - **No global require-geo** without pack `geo_intake`.
  - Не dump raw `geo_detail` в public Issue card.
  - Не класть новые geo cols в `required_columns_ready`.
  - **Нет SSR-06/07/12.** Не reopen 01–22 product. Не стартовать 24…25 в этом pkg.
  - Stay `semantic-schema-runtime`. Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.
  - Не invent второй binding; sidecar class = `gpt_signals` (root, рядом с `schema_binding`).
  - Не drop `location_query`. Scope gate SSR-22 остаётся.

## Verification commands
```bash
rg -n "geo_intake" doge-complaints-gateway/schema-packs/tallinn_civic/v1/pack.json \
  doge-complaints-gateway/schema-packs/legal_process/v1/pack.json \
  doge-complaints-gateway/schema-packs/mobility_observation/v1/pack.json
```
