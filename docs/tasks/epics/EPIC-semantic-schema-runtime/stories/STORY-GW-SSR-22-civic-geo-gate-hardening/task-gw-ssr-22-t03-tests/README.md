# task-gw-ssr-22-t03-tests

## Task: tests — req35 + `test_gw_ssr_22_*` (T03)

## Meta
- **Story:** [STORY-GW-SSR-22](../STORY-GW-SSR-22-civic-geo-gate-hardening.md)
- **Type:** tests
- **Status:** 🔵 Done · P4 PASS 11 passed 2026-08-30T20:13:31Z
- **Package:** pkg-000079
- **Skill declared:** python-pro
- **Depends on:** T00–T02
- **Scaffolded:** 2026-08-30T20:01:08Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-22-civic-geo-gate-hardening.md` T03

## Purpose
Покрыть fail path (scope + no service → не 202) и optional path (нет `geo_scope`). Адаптировать [`test_req35_geo_scope_and_filter.py`](../../../../../../../tests/test_req35_geo_scope_and_filter.py). `tests/test_gw_ssr_22_*` для G22. Не parse `geo_detail` (→23).

## Code Facts
- REQ-35 suite — [`test_req35_geo_scope_and_filter.py`](../../../../../../../tests/test_req35_geo_scope_and_filter.py)
- G22 scope — `tests/test_gw_ssr_22_*.py` (0 files at P1)
- `ClusterLens` baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)

## Acceptance / DoD
- [x] `test_gw_ssr_22_*` + req35 зелёные
- [x] scope+no service не accept; optional/no-scope path зелёный
- [x] Нет тестов parse `geo_detail` (→23)
- [x] `ClusterLens` = 10
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_22_*.py`
- `doge-complaints-gateway/tests/test_req35_geo_scope_and_filter.py` (adapt)

## Out of scope
- `geo_detail` parse (→23). `live_integration` proof. Start SSR-23.
- Overlay bans (every task):
  - Remove silent skip when `geo_scope` active + `geo_service is None`.
  - **No full `geo_detail` / `geo_intake` parse** (→23). No invent HTTP filter.
  - **No ClusterLens add/remove.** Enum stays 10 (`types.py:10–22`).
  - **Нет `GET /schema-active`.** Нет IDX. Нет GPT UI.
  - **No global require-geo.** Optional / no-`geo_scope` stays geo-agnostic (REQ-35).
  - **Нет SSR-06/07/12.** Не reopen 01–21. Не стартовать 23…25 в этом pkg.
  - Stay `semantic-schema-runtime`. Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.

## Verification commands
```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_22_*.py
python3 -m pytest -q -m "not live_integration" tests/test_req35_geo_scope_and_filter.py
```
