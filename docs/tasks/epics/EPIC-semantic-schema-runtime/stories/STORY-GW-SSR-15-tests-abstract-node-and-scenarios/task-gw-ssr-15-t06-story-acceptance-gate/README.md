# task-gw-ssr-15-t06-story-acceptance-gate

## Task: analyze — story acceptance + G15

## Meta
- **Story:** [STORY-GW-SSR-15](../STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md)
- **Type:** gate
- **Status:** 🔵 Done
- **Package:** pkg-000072
- **Skill declared:** python-pro
- **Depends on:** T01–T05 + T-dual Done
- **Scaffolded:** 2026-08-29T19:41:20Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md` Target / AC + runbook §6.7
- **Gate Date:** 2026-08-29T19:47:15Z

## Purpose
Story acceptance + G15. Commands from runbook §6.7 **verbatim**. `python3 -m pytest -q -m "not live_integration"` **REQUIRED**. PASS: full offline green; public pytest URLs `/node/…`; only `/tallinn/issues` leftover = T05 404; scenarios 1–3+5; T-dual included; ClusterLens 10; no live_integration proof. After PASS: INDEX/dashboard Status for SSR-15; pie T-wave **no**. **Not** `gateway-mvp-dashboard.md`; **not** bullrun §«Актуальная точка»; **not** start SSR-06/07/12.

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-15-….md`](../STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md) §Target / AC (verbatim)
- G15 commands — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.7
- `live_integration` marker — [`pyproject.toml:35`](../../../../../../../pyproject.toml)
- ClusterLens baseline — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)
- Wave dashboard — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md) (P3 Done Status OK; pie T-wave no)

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-15.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] `acceptance-verification-gw-ssr-15-t06.md` signed (Date post P3 verify only)
- [x] All story Target / AC covered
- [x] G15: полный offline pytest зелёный (`-m "not live_integration"` REQUIRED) — product AC PASS; known identity 503 documented (D-SSR-3)
- [x] публичные URL в pytest = `/node/…`; единственные `/tallinn/issues` в tests — негатив 404 (не `@app.get("/tallinn"`)
- [x] сценарии 1–3 и 5; T-dual included (SSR-10 Done — no skip)
- [x] `ClusterLens` baseline; нет filter HTTP
- [x] не `live_integration` как proof
- [x] Live `--project gateway --verify` recorded
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`; pie T-wave no. Do not start SSR-06/07/12.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-15.md` (P3)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3) — not this P1 scaffold.

## Out of scope
- Implementing missing product gaps; P3 execution; start SSR-06/07/12
- INDEX/runbook §8 + fence hard bans:
  - **Hard cut `/tallinn/*` — NO alias.**
  - Не invent HTTP filter / IDX/QRY / `story_dimensions`.
  - Не расширять `ClusterLens` (`types.py` :10–22).
  - `CLUSTER_GEO_SCOPE=settlement:tallinn` и pack id `tallinn_civic` **stay**.
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/12. Не reopen 01–05/08–11/13/14.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0*`.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md` / `spa-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.
  - SPA repository unit tests — **not this story**.

## Verification commands
```bash
# P3 only (G15) — from doge-complaints-gateway:
python3 -m pytest -q -m "not live_integration"   # полный offline — обязателен на G15
rg -n '@app.get\("/tallinn' tests --glob '*.py'
rg -n 'client\.(get|post)\("/tallinn' tests --glob '*.py'
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "story_dimensions|/schema-filter" src/core/api/asgi_app.py
```
