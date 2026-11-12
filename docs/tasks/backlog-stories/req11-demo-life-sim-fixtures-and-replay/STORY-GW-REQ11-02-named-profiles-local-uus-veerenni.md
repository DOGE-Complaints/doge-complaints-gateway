# STORY-GW-REQ11-02 — Named profiles: local + Uus Veerenni deploy

## Meta
- **Key:** `STORY-GW-REQ11-02-named-profiles-local-uus-veerenni`
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) · P3 2026-09-29T14:00:57Z · gate PASS · audit T05 Done G1 CLOSED (`gw_req11_02_audit_followup` 2026-09-29T14:08:13Z)
- **Тип:** config / profiled targets
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md) §4.4; **GW-11-03**; D3
- **Skill declared (future P3):** `python-pro` · soft `code-documenter`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Pipeline:** [`../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni.md`](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni.md)
- **pkg:** [`../../gateway-active-packages/pkg-000101-20260929-gw-req11-02-named-profiles-local-uus-veerenni.yaml`](../../gateway-active-packages/pkg-000101-20260929-gw-req11-02-named-profiles-local-uus-veerenni.yaml)
- **Profiles:** `tests/sandbox/profiles/{local,uus-veerenni,index}.json`
- **Selection note:** [`../../analysis/note-gw-req11-02-profile-selection-2026-09-29.md`](../../analysis/note-gw-req11-02-profile-selection-2026-09-29.md)
- **Audit follow-up:** T05 **Done** G1 CLOSED · [`task-gw-req11-02-t05-audit-g1-as-of-done-ssot`](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni/task-gw-req11-02-t05-audit-g1-as-of-done-ssot/README.md) · `run_mode=gw_req11_02_audit_followup`
- **Operator lock (`local`):** ports/URLs from [`local-five-serve-and-health.sh`](../../../../../scripts/shell/local-five-serve-and-health.sh) — identity 8100, gateway 8000, threads 8001, aibridge 8080, spa 5173
- **Зависит от:** —
- **Blocks:** STORY-GW-REQ11-03
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)

---

## Scope

1. Named selectable profiles: at least `local` + Uus Veerenni deploy.
2. Profile holds URLs + token **env refs** (not secrets in git).
3. Document how operator selects profile for replay.
4. `local` mirrors local-five defaults (PORT overrides from each service `.env` still allowed at runtime).

## Out of scope

- Fixture JSON content (→ REQ11-01).
- Replay loop / multi-submitter (→ REQ11-03).
- Literal secret values; invent undocumented public APIs.

## Verified current state

| Fact | Path |
|------|------|
| Local-five service ports | `scripts/shell/local-five-serve-and-health.sh:17-23` |
| Runner uses `GATEWAY_URL` + API token + single user Bearer | `tests/simulation_runner.py:152-154` |
| Make `simulate` | `Makefile:31-32` |
| `.env.test.example` shows deploy-style `GATEWAY_URL` | `.env.test.example:11-14` (example host; not invent new products) |
| Named multi-profile selector | **Present** — `tests/sandbox/profiles/` (`local`, `uus-veerenni`); `DEMO_LIFE_SIM_PROFILE` |

## Target / AC

- [x] **AC-GW-REQ1102-01:** Profile `local` selectable with local-five URL/env refs (D3 / GW-11-03).
- [x] **AC-GW-REQ1102-02:** Profile Uus Veerenni deploy selectable with documented URL/env refs (D3).
- [x] **AC-GW-REQ1102-03:** Secrets stay in env; profile files only reference env names.
## Code touchpoints

- `scripts/shell/local-five-serve-and-health.sh`
- `tests/simulation_runner.py` env contract
- `.env.test.example` as pattern for env refs (no secret commit)

## Dependencies

- Deploy URL/token values remain ops env (refs only in repo).
