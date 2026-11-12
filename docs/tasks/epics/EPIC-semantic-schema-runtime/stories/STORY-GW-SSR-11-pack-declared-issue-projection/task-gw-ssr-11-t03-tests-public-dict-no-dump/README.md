# task-gw-ssr-11-t03-tests-public-dict-no-dump

## Task: tests — public dict without payload dump (T03)

## Meta
- **Story:** [STORY-GW-SSR-11](../STORY-GW-SSR-11-pack-declared-issue-projection.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000070
- **Skill declared:** python-pro
- **Depends on:** T00–T02
- **Scaffolded:** 2026-08-29T19:08:43Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-11-pack-declared-issue-projection.md` T03

## Purpose
`tests/test_gw_ssr_11_*.py`: public dict without full `structured_payload`; `forbidden`/`node_private` absent; civic Issue unchanged; pack with allowlist has named leaves only; absent key = civic form. Public read cite `GET /node/issues`.

## Code Facts
- Public card — [`dto.py:26–50`](../../../../../../../src/core/projection/dto.py)
- G11 pytest — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.5 `tests/test_gw_ssr_11_*.py`
- Civic gate default — [`gates.py:14`](../../../../../../../src/core/promotion/gates.py) `require_actionable_canonical_type: bool = True`

## Acceptance / DoD
- [x] Public dict без полного `structured_payload`
- [x] `forbidden` / `node_private` paths отсутствуют
- [x] Civic Issue unchanged (no new required keys)
- [x] Pack with allowlist: named leaves only; absent key = civic form
- [x] Public read cite `GET /node/issues`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_11_*.py` (new)

## Out of scope
- spa-app UI; rewrite `test_req24_*` (SSR-15); HALT on red `/tallinn/` pytest (G15)
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py:108–111`).
  - Не invent HTTP filter / IDX/QRY / `story_dimensions`. `GET /node/issues` stays (`asgi_app.py:462`).
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/12/14/15. Не reopen 01–05/08–10/13.
  - Не вызывать / не реализовывать `SchemaRuntime.project` (stub `runtime.py:68–72` stays `NotImplementedError`).
  - Не dump `structured_payload` на карточку; не проецировать `forbidden` / `node_private`.
  - Overlay UI spa-app — **not this story**.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0[1-5]*`.
  - `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_11_*.py
```
