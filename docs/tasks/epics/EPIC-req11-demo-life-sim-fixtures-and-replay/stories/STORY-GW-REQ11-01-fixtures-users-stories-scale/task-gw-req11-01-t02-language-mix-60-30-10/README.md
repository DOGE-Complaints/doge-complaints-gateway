# task-gw-req11-01-t02-language-mix-60-30-10

## Task: implement/verify — language mix ≈ 60/30/10 (T02)

## Meta
- **Story:** [STORY-GW-REQ11-01](../STORY-GW-REQ11-01-fixtures-users-stories-scale.md)
- **Type:** implement / verify
- **Status:** 🟢 Done
- **Closed:** 2026-09-29T13:43:36Z
- **Package:** pkg-000100
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-09-29T13:22:23Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-01-fixtures-users-stories-scale.md`

## Purpose
Language mix measurable ≈ 60% et / 30% ru / 10% en on fixture stories. Scope #2 · AC-GW-REQ1101-02.

## Code Facts
1. Operator lock langs: **60% et / 30% ru / 10% en** (package INDEX / story Meta).
2. Canvas fixtures exist but are not life-sim multi-lang scale set: `tests/sandbox/dogestonia_simulation_canvas_v0_1.json` / `v0_2.json`.
3. **As-of-Done:** measurable mix on life-sim stories — et **0.602** / ru **0.2926** / en **0.1054** (`…_fixtures_v0_1_meta.json`; `test_ac02_*`).
4. **Historical:** Multi-user / Gaussian / 2026 exp fixtures were **Absent** until T01/P3.

## Gap
**CLOSED (P3):** language mix measurable ≈60/30/10. Present-tense absence moved to Historical (P6 G1 SSOT).

## Acceptance / DoD
- [x] Language mix measurable ≈ 60/30/10 (AC-GW-REQ1101-02)
- [x] Measurement command/evidence recorded (pytest or script output)
- [x] BULLRUN phases complete when closed

## Where to change
- Fixture generation / story language fields (same artifacts as T01)
- Optional verify helper/test asserting mix within tolerance (P3)

## Out of scope
Scale generation (T01); timestamps (T03); canvas doc (T04); gate (T05); invent public APIs; profiles/replay.
- Overlay bans:
  - Stay `dev`.
  - Pointer pkg-000100; do not mutate pkg-000099.

## Verification commands
```bash
# P3: measure et/ru/en fractions on stories fixture
rg -n 'et|ru|en|language|locale' doge-complaints-gateway/tests/sandbox --glob '*life*' --glob '*req11*' | head -40
```
