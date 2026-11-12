# Story acceptance gate — STORY-GW-REQ11-01

- **Story:** Users+stories JSON fixtures (scale, languages, 2026 curve)
- **Package:** `pkg-000100-20260929-gw-req11-01-fixtures-users-stories-scale.yaml`
- **Result:** PASS
- **Date:** 2026-09-29T13:43:36Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ1101-01: Fixture artifacts on disk (users + stories) at locked scale (D2 / GW-11-01) | PASS | `tests/sandbox/dogestonia_life_sim_users_v0_1.json` (200) + `…_stories_v0_1.json` (1661); Gaussian mean 8.305 clamp [3,13]⊂[1,20]; generator `generate_dogestonia_life_sim_fixtures_v0_1.py`; pytest `test_ac01_*` |
| AC-GW-REQ1101-02: Language mix measurable ≈ 60/30/10 (D5 / GW-11-02) | PASS | et 0.602 / ru 0.2926 / en 0.1054; meta + `test_ac02_*` |
| AC-GW-REQ1101-03: Timestamps follow 2026 exponential curve per lock (D6 / GW-11-02) | PASS | span 2026-01-01…2026-12-31; breakpoint 2026-09-30; pre 0.2498 / post 0.7502; post density > pre; `test_ac03_*` |
| AC-GW-REQ1101-04: Documented how fixtures relate to canvas v0_1/v0_2 for life-sim | PASS | [`note-gw-req11-01-life-sim-vs-canvas-2026-09-29.md`](../../../../../../analysis/note-gw-req11-01-life-sim-vs-canvas-2026-09-29.md) — life-sim supersedes canvas for multi-user scale; canvas remains runner scenario array |

## Commands (live verification 2026-09-29T13:43:36Z)

```text
--verify ok 5 (pkg-000100)
--verify --check-dates → ok date-check
.venv/bin/python -m pytest -q tests/test_gw_req11_01_life_sim_fixtures.py → 4 passed
utc_now: 2026-09-29T13:43:36Z
branch: dev
no invent public APIs; profiles/replay/backdate out of scope; §Актуальная точка untouched
```
