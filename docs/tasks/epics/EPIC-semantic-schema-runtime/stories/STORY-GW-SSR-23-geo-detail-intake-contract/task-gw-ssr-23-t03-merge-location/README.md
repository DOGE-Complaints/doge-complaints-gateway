# task-gw-ssr-23-t03-merge-location

## Task: implement — merge `geo_detail` + `location_query` (T03)

## Meta
- **Story:** [STORY-GW-SSR-23](../STORY-GW-SSR-23-geo-detail-intake-contract.md)
- **Type:** implement
- **Status:** 🔵 Done · P4 PASS 2026-08-30T20:44:21Z
- **Package:** pkg-000080
- **Skill declared:** python-pro
- **Depends on:** T01 T02
- **Scaffolded:** 2026-08-30T20:29:24Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-23-geo-detail-intake-contract.md` T03

## Purpose
Свести client `geo_detail` и `location_query` → snapshot draft / resolve. `merge`: client detail wins over provider miss. Не drop `location_query`. Enforce `geo_intake.mode`. Scope gate SSR-22 остаётся.

## Code Facts
1. **As-of-Done:** fuzzy resolve still `location_query`, then `enforce_geo_intake_mode` + `merge_client_geo_detail` — [`services.py:220–227`](../../../../../../../src/core/application/services.py), [`:281–286`](../../../../../../../src/core/application/services.py).
2. Snapshot без street/houses (persist →24) — [`domain/contracts.py:28–40`](../../../../../../../src/core/domain/contracts.py).
3. SSR-22 scope + no service → `IntakeValidationError("geo unavailable")` — [`handlers.py:258–260`](../../../../../../../src/core/api/handlers.py).
4. **Historical (pre-SSR-23):** resolve только `location_query`; no merge overlay.

## Acceptance / DoD
- [x] Merge задокументирован и применяется на intake
- [x] `location_query` остаётся для fuzzy resolve
- [x] `geo_intake.mode` управляет обязательностью
- [x] Не map-to-SQL depth (→24)
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/application/services.py`
- `doge-complaints-gateway/src/core/api/handlers.py` (policy vs SSR-22 gate; no new HTTP path)

## Out of scope
- Drop `location_query`. SQL columns (→24).
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
rg -n "geo_detail|geo_intake|location_query" doge-complaints-gateway/src/core/application/services.py
```
