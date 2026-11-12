# Story acceptance gate — STORY-GW-REQ11-03

- **Story:** Profiled API replay + multi-fixture submitters
- **Package:** `pkg-000102-20260929-gw-req11-03-profiled-api-replay-multi-submitter.yaml`
- **Result:** PASS (tooling + unit/contract; live multi-submitter blocked by missing pool creds — operator blocker)
- **Date:** 2026-09-29T14:21:44Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ1103-01: Wipe/zero → profiled replay → stories enter gateway pipeline (D1 / GW-11-04) | PASS* | `--life-sim --wipe-confirmed` gate; extends `post_stash_and_submit_http`; dry-run 5/5; *live HTTP fill blocked — see Blocker |
| AC-GW-REQ1103-02: Replay uses fixture scale from REQ11-01 (D2) | PASS | `assert_fixture_scale` 200 users / 1661 stories; `test_ac02_*` |
| AC-GW-REQ1103-03: Multi-submitter via pool M=20 mapped from 200 fixtures (GW-11-06) | PASS* | `life_sim_pool_m20.json` + map 200→20 (10/slot); `resolve_pool_slot_bearer_token`; *0/20 env slots filled — Blocker |
| AC-GW-REQ1103-04: No SPA resident login; primary API+JSON (K1/K4) | PASS | note-gw-req11-03; `make simulate-life-sim`; no SPA in Pass path; `test_ac04_*` |

## Operator blocker (live multi-submitter)

| Fact | Value |
|------|-------|
| Gateway `127.0.0.1:8000/health` | HTTP 200 |
| Identity `127.0.0.1:8100/health` | HTTP 200 |
| `LIFE_SIM_POOL_00..19_*` ready slots | **0 / 20** |
| Live `--life-sim` without dry-run | FAIL-CLOSED: `Pool M=20 incomplete: 0/20` |
| Secrets invented? | No |

## Commands (live verification 2026-09-29T14:21:44Z)

```text
--verify ok 6 (pkg-000102)
--verify --check-dates → ok date-check
.venv/bin/python -m pytest -q tests/test_gw_req11_03_profiled_api_replay.py → 8 passed
.venv/bin/python tests/simulation_runner.py --life-sim --wipe-confirmed --dry-run --profile local --max 5 → 5/5
utc_now: 2026-09-29T14:21:44Z
branch: dev
no invent APIs/secrets; §Актуальная точка untouched
```
