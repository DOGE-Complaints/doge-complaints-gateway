# task-gw-ssr-15-t07-audit-g1-suite-isolation

## Task: tests — isolate G15 suite-order so offline pytest exits 0

## Meta
- **Story:** [STORY-GW-SSR-15](../STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000072 (parent product URL AC Done); wave `run_mode=gw_ssr_15_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-15
- **Depends on:** T01–T06 + T-dual Done (product URL AC)
- **Audit ref:** [`audit-gw-ssr-15-tests-abstract-node-and-scenarios-2026-08-29.md`](../../../../../../analysis/audit-gw-ssr-15-tests-abstract-node-and-scenarios-2026-08-29.md) **G1**
- **Scaffolded:** 2026-08-29T19:54:57Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-15_gap_20260829T195257Z.plan.md` G1 TASKED follow_up=none
- **Gate Date:** 2026-08-29T19:57:04Z

## Purpose
Закрыть G1 (HIGH): G15 suite EXIT 1 vs gate/SSOT «PASS». OP: 2 failed / 743 passed; оба fail **pass isolated**. Isolation/fixtures в **gateway tests only** так чтобы `pytest -q -m "not live_integration"` **exit 0**. Не skip G15. Не WAIVE out-of-DoD. Не rewrite `doge-identity-service`. Не invent identity product AC. После exit 0 — align gate Residual + epic/INDEX/dashboard G15 counts.

## Code Facts
1. Audit G1 — [`audit-gw-ssr-15-tests-abstract-node-and-scenarios-2026-08-29.md`](../../../../../../analysis/audit-gw-ssr-15-tests-abstract-node-and-scenarios-2026-08-29.md) §3 / §5.
2. G15 iff полный offline pytest зелёный — [`orchestrator-post-t-wave-runbook.md:384–386`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md).
3. Fail A — [`test_gw_draft_02_get_auth_contract.py:157`](../../../../../../../tests/test_gw_draft_02_get_auth_contract.py) `delenv IDENTITY_BASE_URL`; autouse setenv — [`conftest.py:75`](../../../../../../../tests/conftest.py).
4. Fail B — [`test_concurrent_intake_contract.py:58`](../../../../../../../tests/test_concurrent_intake_contract.py) `test_cc01_parallel_intake_returns_five_unique_story_ids`.
5. Empty `IDENTITY_BASE_URL` = None — [`schema.py:625–632`](../../../../../../../src/core/config/schema.py). `delenv` re-opens dotenv fill — [`env_file.py:15`](../../../../../../../src/core/config/env_file.py).
6. Pointer stays pkg-000072 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
7. Product URL AC yes; G15 suite green no until this task.

## Gap / Проблема
Suite-order pollution: identity 503 + cc01 pass isolated, fail in full `-m "not live_integration"`. Runbook G15 = continue-gate этой стори.

## Acceptance / DoD
- [x] `cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration"` **exit 0**
- [x] Isolation only: `conftest.py` / `test_gw_draft_02_get_auth_contract.py` / `test_concurrent_intake_contract.py` (gateway tests)
- [x] Cover identity 503 **and** cc01
- [x] No `doge-identity-service` edits; no invent identity product AC
- [x] After exit 0: gate Residual + epic/INDEX/dashboard G15 counts = live OP
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000072
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-15-t07.md` signed (Date post P6 live suite + `--print-utc-now`)

## Where to change
- `doge-complaints-gateway/tests/test_gw_draft_02_get_auth_contract.py`
- `doge-complaints-gateway/tests/test_concurrent_intake_contract.py`
- `doge-complaints-gateway/tests/conftest.py` only if needed for isolation
- After exit 0: gate / epic / INDEX / dashboard G15 residual counts (not product URL reopen)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- `doge-identity-service` (D-SSR-3)
- Invent identity product AC
- `gateway-mvp-dashboard.md`; pie T-wave
- New pkg; `gateway-active-package.current.yaml` stays pkg-000072
- SSR-06/07/12 execute; reopen 01–05/08–11/13/14 product URL
- T-wave G3 / `audit-gw-ssr-0*` rewrite
- `live_integration` as proof
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens`.
  - Не invent HTTP filter / IDX/QRY.
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/12. Не reopen 01–05/08–11/13/14 product.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration"
```
