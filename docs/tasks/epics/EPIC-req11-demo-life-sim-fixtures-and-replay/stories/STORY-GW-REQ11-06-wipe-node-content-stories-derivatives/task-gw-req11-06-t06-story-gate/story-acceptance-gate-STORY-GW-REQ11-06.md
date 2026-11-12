# Story acceptance gate — STORY-GW-REQ11-06

- **Story:** Wipe node content (stories + derivatives + threads)
- **Package:** `pkg-000105-20260930-gw-req11-06-wipe-node-content-stories-derivatives.yaml`
- **Result:** PASS
- **Date:** 2026-09-30T07:56:35Z

## AC checklist (verbatim from backlog)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ1106-01: Script + Make present; refuses without confirm flag | PASS | `life_sim_wipe_node_content.py` + `make life-sim-wipe-node-content`; refuse exit 2 without confirm |
| AC-GW-REQ1106-02: Wipes gateway story stack + threads; does **not** touch Identity users | PASS | Live DELETE 204 gateway readiness tables + threads marks/comments/threads; no auth.users paths |
| AC-GW-REQ1106-03: Manual § wipe links to Present script; dry-run documented | PASS | `life-sim-demo-node-load-manual-ru.md` §5; `--dry-run` / `LIFE_SIM_WIPE_DRY_RUN=1` |
| AC-GW-REQ1106-04: Offline/unit or smoke for confirm-gate + ordered deletes | PASS | `tests/test_gw_req11_06_wipe_node_content.py` **8 passed**; live wipe smoke 204 |

## Commands (live verification 2026-09-30T07:56:35Z)

```text
--verify ok 6 (pkg-000105)
.venv/bin/python -m pytest -q tests/test_gw_req11_06_wipe_node_content.py → 8 passed
.venv/bin/python tests/sandbox/life_sim_wipe_node_content.py → REFUSED exit 2
.venv/bin/python tests/sandbox/life_sim_wipe_node_content.py --dry-run → plan listed
LIFE_SIM_WIPE_CONFIRMED=1 … --confirm-wipe --gateway-only → all 204 ok
LIFE_SIM_WIPE_CONFIRMED=1 … --confirm-wipe --threads-only → all 204 ok
utc_now: 2026-09-30T07:56:35Z
branch: dev
no invent wipe HTTP; no Identity DELETE; §Актуальная точка untouched; no push
```
