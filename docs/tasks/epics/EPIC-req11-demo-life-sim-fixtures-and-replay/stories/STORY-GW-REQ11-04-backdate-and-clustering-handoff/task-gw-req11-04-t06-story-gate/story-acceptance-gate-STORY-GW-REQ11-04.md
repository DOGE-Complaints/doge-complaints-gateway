# Story acceptance gate — STORY-GW-REQ11-04

- **Story:** Backdate contract + clustering wait handoff
- **Package:** `pkg-000103-20260929-gw-req11-04-backdate-and-clustering-handoff.yaml`
- **Result:** PASS (product lock-B + docs + unit/contract; live multi-submitter+backdate still blocked by pool creds from REQ11-03)
- **Date:** 2026-09-29T14:39:37Z

## AC checklist (verbatim from backlog)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ1104-01: Fixture times survive via lock-B service-auth backdate after stash→submit | PASS* | `PATCH /ops/stories/{id}/created-at` + `update_created_at` + runner wire; tests AC01; *live HTTP blocked by pool 0/20 |
| AC-GW-REQ1104-02: Runbook/script documents clustering wait (CLUSTER_MIN_SIZE/cron) before threads seed | PASS | note T04 + `tests/sandbox/life_sim_wait_clustering.sh` |
| AC-GW-REQ1104-03: Board card count follows clustering (K3); no invent cluster product APIs | PASS | note T05 explicit K3 + no-invent |

## Operator blocker (live backdate after submit)

| Fact | Value |
|------|-------|
| Pool slots `LIFE_SIM_POOL_NN_*` | **0 / 20** (carried from REQ11-03) |
| Live non-dry-run `--life-sim` | fail-closed incomplete pool |
| Contract path | dry-run shows fixture `created_at` + PATCH planned; unit tests exercise ops route |

## Commands (live verification 2026-09-29T14:39:37Z)

```text
--verify ok 6 (pkg-000103)
.venv/bin/python -m pytest -q tests/test_gw_req11_04_backdate_and_clustering.py → 6 passed
.venv/bin/python tests/simulation_runner.py --life-sim --wipe-confirmed --dry-run --profile local --max 3 → 3/3 (+ created_at lines)
utc_now: 2026-09-29T14:39:37Z
branch: dev
no invent public intake created_at / cluster APIs; §Актуальная точка untouched
```
