# task-gw-ssr-15-t03-pack-scenario

## Task: tests — bound pack → same `GET /node/issues` (T03)

## Meta
- **Story:** [STORY-GW-SSR-15](../STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000072
- **Skill declared:** python-pro
- **Depends on:** T01; SSR-08 Done
- **Scaffolded:** 2026-08-29T19:41:20Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md` T03 / scenario 2

## Purpose
Schema-bound pack (`legal_process` **or** `tallinn_civic` — both exist; 08 Done) → card on **the same** `GET /node/issues`. No new filter route.

## Code Facts
- Same public path — [`asgi_app.py:462`](../../../../../../../src/core/api/asgi_app.py) `GET /node/issues`
- Packs on disk — `schema-packs/legal_process/v1/`, `schema-packs/tallinn_civic/v1/`
- SSR-08 Done — G8 PASS 2026-08-29T17:52:54Z
- SSR-11 `schema_card` sidecar — [`test_gw_ssr_11_public_dict_no_dump.py`](../../../../../../../tests/test_gw_ssr_11_public_dict_no_dump.py) (no `client.get("/node/` this draft)

## Acceptance / DoD
- [x] Сценарий 2 зелёный: bound pack → card on `GET /node/issues`
- [x] No new HTTP filter path
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_15_*.py` (or extend existing pack+HTTP test if one exists after T01)

## Out of scope
- Dump `structured_payload`. IDX/QRY HTTP. New path.
- INDEX/runbook §8 + fence hard bans:
  - Не invent HTTP filter / IDX/QRY / `story_dimensions`.
  - Не alias 200. Не `live_integration` proof.
  - Не менять geo `tallinn` / pack id `tallinn_civic`.
  - Не переписывать T-wave G3 / §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не реализовывать SSR-06/07/12. Не reopen 01–05/08–11/13/14.
  - SPA repository unit tests — **not this story**.

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration" -k "ssr_15 or node/issues"
```
