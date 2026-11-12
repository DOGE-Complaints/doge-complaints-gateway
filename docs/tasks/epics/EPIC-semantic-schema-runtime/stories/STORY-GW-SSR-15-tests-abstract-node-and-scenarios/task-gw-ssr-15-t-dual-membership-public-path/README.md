# task-gw-ssr-15-t-dual-membership-public-path

## Task: tests — dual membership + `GET /node/issues` (T-dual)

## Meta
- **Story:** [STORY-GW-SSR-15](../STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000072
- **Skill declared:** python-pro
- **Depends on:** T01; SSR-10 Done (G10 PASS 2026-08-29T18:31:19Z)
- **Scaffolded:** 2026-08-29T19:41:20Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md` T-dual / scenario 4

## Purpose
SSR-10 **is Done** — **include** one test: dual membership (civic+exact) **and** the same public path `GET /node/issues`. Reuse SSR-10 helpers (`test_gw_ssr_10_orchestrator_dual.py` / pack flag); do **not** skip; do **not** invent a second dual engine.

## Code Facts
- SSR-10 Done — INDEX `:85`; epic Stories `:90`; G10 PASS `2026-08-29T18:31:19Z`
- Dual membership (no public HTTP) — [`test_gw_ssr_10_orchestrator_dual.py`](../../../../../../../tests/test_gw_ssr_10_orchestrator_dual.py)
- Pack flag — [`test_gw_ssr_10_dual_pack_flag.py`](../../../../../../../tests/test_gw_ssr_10_dual_pack_flag.py)
- Public path — [`asgi_app.py:462`](../../../../../../../src/core/api/asgi_app.py) `GET /node/issues`
- `ClusterLens` still 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)

## Acceptance / DoD
- [x] Сценарий 4: dual membership + `GET /node/issues` (не skip)
- [x] No new `ClusterLens` member
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_15_*.py` (or extend SSR-10 dual helper with HTTP client)

## Out of scope
- Skip «после 10». New `ClusterLens` member. New HTTP.
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens`. Civic factory default True stay.
  - Не invent HTTP filter / IDX/QRY.
  - Не alias 200. Не `live_integration` proof.
  - Не менять geo `tallinn` / pack id `tallinn_civic`.
  - Не переписывать T-wave G3 / §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не реализовывать SSR-06/07/12. Не reopen SSR-10 product.

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_10_orchestrator_dual.py -k "ssr_15 or dual"
```
