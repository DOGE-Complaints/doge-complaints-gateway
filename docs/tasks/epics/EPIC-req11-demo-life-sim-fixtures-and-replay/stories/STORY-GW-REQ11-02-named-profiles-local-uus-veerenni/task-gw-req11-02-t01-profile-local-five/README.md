# task-gw-req11-02-t01-profile-local-five

## Task: implement — profile `local` (local-five) (T01)

## Meta
- **Story:** [STORY-GW-REQ11-02](../STORY-GW-REQ11-02-named-profiles-local-uus-veerenni.md)
- **Type:** implement / config
- **Status:** 🔵 Done
- **Package:** pkg-000101
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-09-29T13:56:20Z
- **Closed:** 2026-09-29T14:00:57Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni.md`

## Purpose
Profile `local` selectable with local-five URL/env refs. Scope #1+#4 · AC-GW-REQ1102-01. Ports: identity 8100, gateway 8000, threads 8001, aibridge 8080, spa 5173; PORT overrides from each service `.env` allowed at runtime.

## Code Facts
1. Local-five ports: `scripts/shell/local-five-serve-and-health.sh:17-23`.
2. Runner today: `GATEWAY_URL` / `GATEWAY_API_TOKEN` / user Bearer — `tests/simulation_runner.py:152-154`.
3. **As-of-Done:** profile `local` selectable — `tests/sandbox/profiles/local.json` + `index.json` + `demo_life_sim_profiles.py`; ports 8100/8000/8001/8080/5173; `GATEWAY_API_TOKEN` env ref.
4. Local comment pattern: `.env.test.example:11-14` (`http://127.0.0.1:8000`).
5. **Historical:** Named multi-profile selector was **Absent** pre-P3 (story Verified / T01 Gap).

## Gap
**CLOSED (P3):** `local` profile artifact on disk. Present-tense absence claims moved to Historical (P6 G1 SSOT).

## Acceptance / DoD
- [x] Profile `local` selectable with local-five URL/env refs (AC-GW-REQ1102-01)
- [x] Ports match operator lock 8100/8000/8001/8080/5173 (env refs, not hard secrets)
- [x] Runtime PORT overrides from service `.env` documented as allowed
- [x] BULLRUN phases complete when closed

## As-of-Done
- Artifact: `tests/sandbox/profiles/local.json` (+ registry `index.json`, loader `demo_life_sim_profiles.py`)
- Evidence: pytest `test_ac01_*`; BULLRUN-PHASE-LOG Done 2026-09-29T14:00:57Z

## Where to change
- New profile config under gateway tests/docs/config path chosen at P3 (e.g. `tests/sandbox/profiles/` or similar)
- Optional loader hook (P3) — do not invent public APIs

## Out of scope
Uus Veerenni profile (T02); selection/env-ref doc (T03); gate (T04); fixtures; replay; literal secrets.
- Overlay bans:
  - Stay `dev`.
  - Do not mutate pkg-000100; pointer is pkg-000101.
  - No secrets in git.

## Verification commands
```bash
rg -n '8100|8000|8001|8080|5173|local-five|profile.*local' doge-complaints-gateway/tests doge-complaints-gateway/docs --glob '*req11*' --glob '*profile*' | head -40
```
