# task-gw-ssr-23-t00-contract-readme

## Task: add — document `geo_detail` + `geo_intake` (T00)

## Meta
- **Story:** [STORY-GW-SSR-23](../STORY-GW-SSR-23-geo-detail-intake-contract.md)
- **Type:** docs
- **Status:** 🔵 Done · P4 PASS 2026-08-30T20:44:21Z
- **Package:** pkg-000080
- **Skill declared:** python-pro
- **Depends on:** SSR-22 Done (G22)
- **Scaffolded:** 2026-08-30T20:29:24Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-23-geo-detail-intake-contract.md` T00

## Purpose
Зафиксировать shape `geo_detail` (root sidecar) и pack `geo_intake` в [`schema-packs/README.md`](../../../../../../../schema-packs/README.md). Не invent frozen YAML dialect.

## Code Facts
1. **As-of-Done:** README documents `geo_detail` + `geo_intake` — [`schema-packs/README.md:31`](../../../../../../../schema-packs/README.md), [`:81–102`](../../../../../../../schema-packs/README.md).
2. **As-of-Done:** sidecars `gpt_signals` + `schema_binding` + optional `geo_detail` — [`contracts.py:193`](../../../../../../../src/core/intake/contracts.py), [`:209`](../../../../../../../src/core/intake/contracts.py).
3. **As-of-Done:** Tallinn payload `geo.*` (district…houses) — [`payload.schema.json:23–38`](../../../../../../../schema-packs/tallinn_civic/v1/payload.schema.json).
4. **Historical (pre-SSR-23):** README без `geo_intake` / `geo_detail`; payload `geo.district` only.
5. D-SSR-10 — [`INDEX.md`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md).
6. G23 — [`orchestrator-geo-detail-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-geo-detail-runbook.md) §6.2.

## Acceptance / DoD
- [x] `schema-packs/README.md` документирует `geo_detail` fields и `geo_intake` modes из story In
- [x] Не invent frozen YAML dialect
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/schema-packs/README.md`

## Out of scope
- Loader / parse / merge (T01–T03). SQL (→24).
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
rg -n "geo_detail|geo_intake" doge-complaints-gateway/schema-packs/README.md
```
