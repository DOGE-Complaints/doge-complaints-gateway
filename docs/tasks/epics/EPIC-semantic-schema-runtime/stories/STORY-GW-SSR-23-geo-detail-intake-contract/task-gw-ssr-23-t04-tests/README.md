# task-gw-ssr-23-t04-tests

## Task: tests — `test_gw_ssr_23_*` (T04)

## Meta
- **Story:** [STORY-GW-SSR-23](../STORY-GW-SSR-23-geo-detail-intake-contract.md)
- **Type:** tests
- **Status:** 🔵 Done · P4 PASS 2026-08-30T20:44:21Z
- **Package:** pkg-000080
- **Skill declared:** python-pro
- **Depends on:** T01 T02 T03
- **Scaffolded:** 2026-08-30T20:29:24Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-23-geo-detail-intake-contract.md` T04

## Purpose
Покрыть AC: accept detail; invalid → 4xx; optional omit → 202; `require_detail` miss → 4xx; merge + `location_query`. Не SQL migration tests (→24).

## Code Facts
1. G23 pytest glob — [`orchestrator-geo-detail-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-geo-detail-runbook.md) §6.2.
2. ClusterLens baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py).
3. SSR-22 tests stay — [`test_gw_ssr_22_civic_geo_gate.py`](../../../../../../../tests/test_gw_ssr_22_civic_geo_gate.py).

## Acceptance / DoD
- [x] `tests/test_gw_ssr_23_*.py` покрывает AC
- [x] Нет SQL migration (→24)
- [x] ClusterLens=10 asserted
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_23_*.py` (new)

## Out of scope
- SQL / omit-probe (→24). `live_integration`.
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
cd doge-complaints-gateway
.venv/bin/python -m pytest -q -m "not live_integration" tests/test_gw_ssr_23_*.py
```
