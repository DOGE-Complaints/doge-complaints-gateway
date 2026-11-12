# task-gw-req11-02-t03-env-refs-and-selection-doc

## Task: docs/config — env refs only + operator selection (T03)

## Meta
- **Story:** [STORY-GW-REQ11-02](../STORY-GW-REQ11-02-named-profiles-local-uus-veerenni.md)
- **Type:** docs / config hygiene
- **Status:** 🔵 Done
- **Package:** pkg-000101
- **Skill declared:** python-pro
- **Depends on:** T01, T02 (prefer profiles exist or paths named)
- **Scaffolded:** 2026-09-29T13:56:20Z
- **Closed:** 2026-09-29T14:00:57Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni.md`

## Purpose
Profiles hold URLs + token **env refs** (not secrets in git). Document how operator selects profile for replay. Scope #2+#3 · AC-GW-REQ1102-03.

## Code Facts
1. `.env.test.example` pattern: placeholder values / env names — do not commit `.env.test`.
2. Runner reads env at runtime: `tests/simulation_runner.py:152-154`.
3. Make `simulate`: `Makefile:31-32`.
4. Replay loop itself → REQ11-03 (out of scope here — only selection handoff doc).
5. **As-of-Done:** selection via `DEMO_LIFE_SIM_PROFILE` + note [`note-gw-req11-02-profile-selection-2026-09-29.md`](../../../../../../analysis/note-gw-req11-02-profile-selection-2026-09-29.md); profiles hold `*_env` names only.
6. **Historical:** No written selection procedure / profile env-ref SSOT pre-P3.

## Gap
**CLOSED (P3):** selection procedure documented; profile files env names only. Present-tense open Gap moved to Historical (P6 G1 SSOT).

## Acceptance / DoD
- [x] Secrets stay in env; profile files only reference env names (AC-GW-REQ1102-03)
- [x] Documented how operator selects profile for replay
- [x] `rg` / review: no committed secret literals in profile artifacts
- [x] BULLRUN phases complete when closed

## As-of-Done
- Note: [`docs/analysis/note-gw-req11-02-profile-selection-2026-09-29.md`](../../../../../../analysis/note-gw-req11-02-profile-selection-2026-09-29.md)
- Evidence: pytest `test_ac03_*` + `test_selection_via_env_and_default`; BULLRUN-PHASE-LOG Done 2026-09-29T14:00:57Z

## Where to change
- Profile YAML/JSON/TOML (env **names** only)
- Short note under `doge-complaints-gateway/docs/analysis/` or runtime testing docs (P3)
- Optional cross-link from package INDEX

## Out of scope
Implement replay (REQ11-03); fixtures; invent APIs; §Актуальная точка rewrite.
- Overlay bans:
  - Stay `dev`.
  - Pointer pkg-000101.
  - No secrets in git.

## Verification commands
```bash
rg -n 'select|profile|GATEWAY_API_TOKEN|env ref|secret' doge-complaints-gateway/docs doge-complaints-gateway/tests --glob '*req11*' --glob '*profile*' | head -40
```
