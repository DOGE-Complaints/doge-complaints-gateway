# task-gw-ssr-15-t04-pulse-emerging

## Task: tests — Pulse/Emerging on separate `/node/` paths (T04)

## Meta
- **Story:** [STORY-GW-SSR-15](../STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000072
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-29T19:41:20Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md` T04 / scenario 3

## Purpose
Pulse → `/node/network-pulse`; Emerging → `/node/emerging-signals`; не issues. After T01, `test_gw_es_02_*` / `test_gw_es_03_*` should already separate paths — verify + keep Topic≠Issue / Emerging≠Issues.

## Code Facts
- Pulse GET — [`asgi_app.py:436`](../../../../../../../src/core/api/asgi_app.py) `@app.get("/node/network-pulse")`
- Emerging GET — [`asgi_app.py:450`](../../../../../../../src/core/api/asgi_app.py) `@app.get("/node/emerging-signals")`
- Tests after T01 — [`test_gw_es_02_network_pulse.py`](../../../../../../../tests/test_gw_es_02_network_pulse.py); [`test_gw_es_03_emerging_signals.py`](../../../../../../../tests/test_gw_es_03_emerging_signals.py); [`test_gw_ssr_15_scenarios.py`](../../../../../../../tests/test_gw_ssr_15_scenarios.py)

## Acceptance / DoD
- [x] Сценарий 3 зелёный: Pulse / Emerging on `/node/…`; not issues
- [x] Topic≠Issue / Emerging≠Issues meaning unchanged
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_es_02_network_pulse.py`
- `doge-complaints-gateway/tests/test_gw_es_03_emerging_signals.py`

## Out of scope
- Кормить Emerging из issues. Change L1/L2 semantics.
- INDEX/runbook §8 + fence hard bans:
  - Не invent HTTP filter / IDX/QRY.
  - Не alias 200. Не `live_integration` proof.
  - Не менять geo `tallinn`.
  - Не переписывать T-wave G3 / §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не реализовывать SSR-06/07/12.

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration" tests/test_gw_es_02_network_pulse.py tests/test_gw_es_03_emerging_signals.py
```
