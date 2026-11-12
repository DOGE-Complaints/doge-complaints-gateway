# task-gw-ssr-15-t01-path-rename

## Task: tests — HTTP asserts `/node/…` + rename req24 (T01)

## Meta
- **Story:** [STORY-GW-SSR-15](../STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000072
- **Skill declared:** python-pro
- **Depends on:** SSR-13 Done (G13 PASS; public routes `/node/*`)
- **Scaffolded:** 2026-08-29T19:41:20Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md` T01

## Purpose
All HTTP asserts `/node/…`. Rename `test_req24_tallinn_issues_read_api.py` → `test_req24_issues_read_api.py` (preferred). Walk inventory table; leftover `tests/` HTTP `/tallinn/(issues|network-pulse|emerging-signals)` same rule. Keep geo fixtures. Flip SSR-05/09 `@app.get` asserts to `/node/issues`. Keep SSR-11 hard-cut (`"/tallinn/issues" not in asgi`). G15: публичные URL в pytest = `/node/…`.

## Code Facts
- Public routes already `/node/*` — [`asgi_app.py:65`](../../../../../../../src/core/api/asgi_app.py) `PUBLIC_ROUTES`; GET/POST [`:462`](../../../../../../../src/core/api/asgi_app.py)/[`:518`](../../../../../../../src/core/api/asgi_app.py)
- req24 renamed + `/node/` HTTP — [`test_req24_issues_read_api.py`](../../../../../../../tests/test_req24_issues_read_api.py)
- SSR-05 `@app.get("/node/issues")` — [`test_gw_ssr_05_negative_ac_018_no_qry.py`](../../../../../../../tests/test_gw_ssr_05_negative_ac_018_no_qry.py)
- SSR-09 same — [`test_gw_ssr_09_packs_visible.py`](../../../../../../../tests/test_gw_ssr_09_packs_visible.py)
- SSR-11 already canon + hard-cut — [`test_gw_ssr_11_public_dict_no_dump.py:102–105`](../../../../../../../tests/test_gw_ssr_11_public_dict_no_dump.py) **N/A**
- `test_req35` no public HTTP path — **N/A** (geo token only)
- `conftest.py:16` `_SERVICE_WRITE_PATH_SUFFIXES = ("/node/issues",)` — HTTP suffix, not geo
- G15 — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.7

## Acceptance / DoD
- [x] Публичные URL в pytest = `/node/…`
- [x] Файл req24 без `tallinn` в имени (preferred rename; N/A in gate only if living nodeid breaks)
- [x] SSR-05/09 `@app.get` asserts → `/node/issues`
- [x] Geo fixtures `admin_settlement=tallinn` / `CLUSTER_GEO_SCOPE` unchanged
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/**` HTTP path hits only (inventory in approved P1 plan)

## Out of scope
- Geo `tallinn` fixtures. Alias. `src/**` route rewrite. SPA tests. Invent filter HTTP.
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens`. Не менять civic factory / `PromotionGatePolicy` default True.
  - Не invent HTTP filter / IDX/QRY / `story_dimensions`.
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/12. Не reopen 01–05/08–11/13/14 product.
  - Не alias 200 на `/tallinn/*`. Негатив = **404** only (T05).
  - Не `live_integration` как proof.
  - Не менять geo vocabulary `tallinn` / pack id `tallinn_civic`.
  - Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md` / `spa-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - SPA repository unit tests — **not this story**.
  - SSR-10 Done — include T-dual, **do not skip**.

## Verification commands
```bash
rg -n 'client\.(get|post)\("/tallinn' doge-complaints-gateway/tests --glob '*.py'
rg -n '@app.get\("/tallinn' doge-complaints-gateway/tests --glob '*.py'
ls doge-complaints-gateway/tests/test_req24_issues_read_api.py
```
