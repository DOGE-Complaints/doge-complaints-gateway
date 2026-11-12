# task-gw-ssr-22-t04-story-acceptance-gate

## Task: analyze — story acceptance + G22

## Meta
- **Story:** [STORY-GW-SSR-22](../STORY-GW-SSR-22-civic-geo-gate-hardening.md)
- **Type:** gate
- **Status:** 🔵 Done · P4 PASS 2026-08-30T20:13:31Z
- **Package:** pkg-000079
- **Skill declared:** python-pro
- **Depends on:** T00–T03 Done
- **Scaffolded:** 2026-08-30T20:01:08Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-22-civic-geo-gate-hardening.md` Target / AC + runbook §6.1

## Purpose
Story acceptance + G22. Commands from runbook §6.1 **verbatim**. PASS: scope+no service не accept; optional/no-scope path зелёный; ClusterLens=10; нет полного geo_detail wire (это 23). After PASS: INDEX/dashboard Status for SSR-22; pie T-wave **no**. **Not** `gateway-mvp-dashboard.md`; **not** bullrun §«Актуальная точка»; **not** start SSR-23/06/07/12.

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-22-civic-geo-gate-hardening.md`](../STORY-GW-SSR-22-civic-geo-gate-hardening.md) §Target / AC
- G22 commands — [`orchestrator-geo-detail-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-geo-detail-runbook.md) §6.1
- `ClusterLens` baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-22.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] `acceptance-verification-gw-ssr-22-t04.md` signed (Date post P3 verify only)
- [x] All story Target / AC covered
- [x] G22: pytest 22 + req35; ClusterLens=10; no full geo_detail wire
- [x] Live `--project gateway --verify` recorded
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`; pie T-wave no. Do not start SSR-23/06/07/12.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-22.md` (P3 — replace Result/Date after live verify)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3)

## Out of scope
- Implementing missing product gaps; start SSR-23/06/07/12
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
# P3 only (G22) — from doge-complaints-gateway:
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_22_*.py
python3 -m pytest -q -m "not live_integration" tests/test_req35_geo_scope_and_filter.py
rg -n "geo_service is None" src/core/api/handlers.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
```
