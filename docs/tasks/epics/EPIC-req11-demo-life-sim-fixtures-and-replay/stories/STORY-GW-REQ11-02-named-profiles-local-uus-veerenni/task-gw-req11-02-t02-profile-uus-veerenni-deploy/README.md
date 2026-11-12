# task-gw-req11-02-t02-profile-uus-veerenni-deploy

## Task: implement — profile Uus Veerenni deploy (T02)

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
Profile Uus Veerenni deploy selectable with documented URL/env refs (D3 / AC-GW-REQ1102-02). Pattern from `.env.test.example` civic host — **refs only**, no secret values in git.

## Code Facts
1. `.env.test.example:11-14` — civic example `GATEWAY_URL=https://uus-veerenni-civic-gateway.dogestonia.me` + placeholder token names.
2. Runner requires `GATEWAY_URL` / `GATEWAY_API_TOKEN` — `tests/simulation_runner.py:152-154`.
3. **As-of-Done:** profile `uus-veerenni` selectable — `tests/sandbox/profiles/uus-veerenni.json`; `GATEWAY_URL` / `GATEWAY_API_TOKEN` env refs; documented_example_url from `.env.test.example`.
4. Literal deploy secrets: ops env only (story Dependencies).
5. **Historical:** Named multi-profile selector / Uus Veerenni profile artifact was **Absent** pre-P3.

## Gap
**CLOSED (P3):** Uus Veerenni deploy profile on disk. Present-tense absence claims moved to Historical (P6 G1 SSOT).

## Acceptance / DoD
- [x] Profile Uus Veerenni deploy selectable with documented URL/env refs (AC-GW-REQ1102-02)
- [x] No literal secrets committed
- [x] BULLRUN phases complete when closed

## As-of-Done
- Artifact: `tests/sandbox/profiles/uus-veerenni.json`
- Evidence: pytest `test_ac02_*`; BULLRUN-PHASE-LOG Done 2026-09-29T14:00:57Z

## Where to change
- Same profile family as T01 (P3 path)
- Document env names for gateway (+ related services if profile includes them) without inventing undocumented public APIs

## Out of scope
`local` profile (T01); selection doc (T03); gate (T04); fixtures; replay; invent APIs.
- Overlay bans:
  - Stay `dev`.
  - Pointer pkg-000101; do not mutate pkg-000100.
  - Secrets stay in env.

## Verification commands
```bash
rg -n 'uus-veerenni|Veerenni|GATEWAY_URL|profile' doge-complaints-gateway/.env.test.example doge-complaints-gateway/tests doge-complaints-gateway/docs --glob '*profile*' --glob '*req11*' | head -40
```
