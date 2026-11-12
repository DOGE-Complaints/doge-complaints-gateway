# task-gw-ssr-15-t05-negative-tallinn-404

## Task: tests — `GET /tallinn/issues` → 404 (T05)

## Meta
- **Story:** [STORY-GW-SSR-15](../STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000072
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-29T19:41:20Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md` T05 / scenario 5

## Purpose
`GET /tallinn/issues` → **404**. No 301/302/200 alias. This is the **only** allowed `client.get("/tallinn/issues")` leftover for T06 rg.

## Code Facts
- Hard cut — `/tallinn/` empty in `src/core/api` (G13). Routes are `/node/*` — [`asgi_app.py:65`](../../../../../../../src/core/api/asgi_app.py)
- SSR-11 already asserts `"/tallinn/issues" not in` asgi — [`test_gw_ssr_11_public_dict_no_dump.py:105`](../../../../../../../tests/test_gw_ssr_11_public_dict_no_dump.py)
- Negative HTTP 404 — [`test_gw_ssr_15_scenarios.py`](../../../../../../../tests/test_gw_ssr_15_scenarios.py) `test_ssr15_legacy_tallinn_issues_is_404`

## Acceptance / DoD
- [x] Сценарий 5 зелёный: `GET /tallinn/issues` → **404**
- [x] No alias 200 / 301 / 302
- [x] This is the only leftover `client.get("/tallinn/issues")` after T01
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_15_*.py` (negative 404)

## Out of scope
- Alias 200. `@app.get("/tallinn"`.
- INDEX/runbook §8 + fence hard bans:
  - **Hard cut `/tallinn/*` — NO alias.**
  - Не invent HTTP filter / IDX/QRY.
  - Не `live_integration` proof.
  - Не менять geo `tallinn`.
  - Не переписывать T-wave G3 / §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не реализовывать SSR-06/07/12.

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration" -k "tallinn and 404"
rg -n 'client\.(get|post)\("/tallinn' doge-complaints-gateway/tests --glob '*.py'
```
