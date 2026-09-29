# Note — GW-REQ11-01 life-sim fixtures vs canvas v0_1 / v0_2

| Field | Value |
|-------|--------|
| **utc** | `2026-09-29T13:42:06Z` (P3; refresh if re-stamped) |
| **Story** | STORY-GW-REQ11-01 · AC-GW-REQ1101-04 |
| **Package** | pkg-000100 |
| **Method** | disk facts only; no invent public APIs |

## Verdict

For **demo life-sim multi-user scale** (200 users × Gaussian ~8.5 stories, langs 60/30/10, 2026 exponential timestamps), the on-disk life-sim JSON **supersedes** canvas `v0_1` / `v0_2` as the **scale dataset**. Canvas remains the **scenario-array** input for today’s `simulation_runner.py` stash→submit path.

## Relation (facts)

| Asset | Path | Role |
|-------|------|------|
| Canvas v0_1 | `tests/sandbox/dogestonia_simulation_canvas_v0_1.json` | 130 scenario objects; single-array runner load |
| Canvas v0_2 | `tests/sandbox/dogestonia_simulation_canvas_v0_2.json` | 18 dense-cluster scenarios (SEED-02) |
| Canvas generator | `tests/sandbox/generate_dogestonia_canvas_v0_2.py` | Regenerates v0_2 |
| Life-sim users | `tests/sandbox/dogestonia_life_sim_users_v0_1.json` | **200** fixture users (REQ11-01) |
| Life-sim stories | `tests/sandbox/dogestonia_life_sim_stories_v0_1.json` | **~1700-order** stories with `language` + `created_at` |
| Life-sim generator | `tests/sandbox/generate_dogestonia_life_sim_fixtures_v0_1.py` | Regenerates users/stories/meta |
| Meta | `tests/sandbox/dogestonia_life_sim_fixtures_v0_1_meta.json` | Measured counts / fractions |

## What is not claimed

- Life-sim JSON is **not** wired into `simulation_runner.py` in this story (runner still expects canvas scenario shape).
- Replay / multi-Bearer / profiles / backdate → REQ11-02/03/04.
- No new public HTTP field names invented here (`fixture_*` keys are on-disk only).

## Consumer handoff

REQ11-03 may map life-sim stories → intake; until then canvas + runner remain the live stash→submit tool. Keep both families on disk; do not delete canvas.
