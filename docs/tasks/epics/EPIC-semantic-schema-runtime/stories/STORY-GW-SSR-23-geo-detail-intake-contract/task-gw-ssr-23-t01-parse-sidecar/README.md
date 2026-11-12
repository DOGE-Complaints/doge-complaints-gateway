# task-gw-ssr-23-t01-parse-sidecar

## Task: implement — parse `geo_detail` sidecar; stash+submit share (T01)

## Meta
- **Story:** [STORY-GW-SSR-23](../STORY-GW-SSR-23-geo-detail-intake-contract.md)
- **Type:** implement
- **Status:** 🔵 Done · P4 PASS 2026-08-30T20:44:21Z
- **Package:** pkg-000080
- **Skill declared:** python-pro
- **Depends on:** T00
- **Scaffolded:** 2026-08-30T20:29:24Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-23-geo-detail-intake-contract.md` T01

## Purpose
Парсить root `geo_detail` (класс как `gpt_signals`) в [`contracts.py`](../../../../../../../src/core/intake/contracts.py). Stash+submit share. Invalid → `IntakeValidationError`. Не новый intake HTTP path.

## Code Facts
1. **As-of-Done:** root `geo_detail` parse stash+submit — [`contracts.py:650–654`](../../../../../../../src/core/intake/contracts.py), [`:700`](../../../../../../../src/core/intake/contracts.py), [`:728`](../../../../../../../src/core/intake/contracts.py).
2. **As-of-Done:** `geo_detail` on stash/intake — [`contracts.py:193`](../../../../../../../src/core/intake/contracts.py), [`:209`](../../../../../../../src/core/intake/contracts.py); stash copy [`:763`](../../../../../../../src/core/intake/contracts.py).
3. **Historical (pre-SSR-23):** Wire geo = `narrative.location_query` only; no `geo_detail` on stash/intake.
4. `location_query` остаётся для fuzzy resolve — [`contracts.py:43`](../../../../../../../src/core/intake/contracts.py).

## Acceptance / DoD
- [x] `geo_detail` парсится на stash+submit
- [x] invalid → `IntakeValidationError`
- [x] Нет нового intake path; нет второго binding
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/intake/contracts.py`

## Out of scope
- Новый intake path. Pack loader (T02). SQL (→24).
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
rg -n "geo_detail" doge-complaints-gateway/src/core/intake/contracts.py
```
