# STORY-GW-REQ11-03 — Profiled API replay + multi-fixture submitters

## Meta
- **Key:** `STORY-GW-REQ11-03-profiled-api-replay-multi-submitter`
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](./INDEX.md)
- **Status:** Done (P3 tooling; live pool env blocker)
- **Тип:** tooling / replay orchestration
- **Parent REQ:** [`55-…`](../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md) §4.5, §4.7; **GW-11-04**, **GW-11-06**; D1/D2; K1/K4
- **Skill declared (future P3):** `python-pro`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Operator lock (auth):** pool **M=20** admin-bootstrapped verified users; map **200** fixture users → pool; no SPA login per run
- **Зависит от:** STORY-GW-REQ11-01, STORY-GW-REQ11-02
- **Blocks:** STORY-GW-REQ11-04
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)

---

## Scope

1. Scripted API replay into zero/wiped env via gateway intake (stash→submit or equivalent documented path); first run fills connected DB.
2. Multi-fixture submitters via locked pool map (not only one `GATEWAY_USER_EMAIL`/`PASSWORD`).
3. Leverage existing runner/HTTP helpers where fit; extend rather than invent parallel product APIs.
4. No SPA resident login requirement (K1); primary path API+JSON (K4).

## Out of scope

- Backdate persistence of fixture times (→ REQ11-04; lock B).
- Threads comment/reaction HTTP; spa UI; Identity SPA accounts for residents as product login.
- SQL dump as Pass path.

## Verified current state

| Fact | Path |
|------|------|
| stash→submit HTTP | `tests/simulation_intake_http.py` `post_stash_and_submit_http` |
| Multi-Bearer pool | `resolve_pool_slot_bearer_token` + `life_sim_pool_m20.json` |
| Map 200→20 | `tests/sandbox/life_sim_fixture_to_pool_map_v0_1.json` |
| Life-sim runner | `tests/simulation_runner.py --life-sim` |

## Target / AC

- [x] **AC-GW-REQ1103-01:** Wipe/zero → profiled replay → stories enter gateway pipeline (D1 / GW-11-04).
- [x] **AC-GW-REQ1103-02:** Replay uses fixture scale from REQ11-01 (D2).
- [x] **AC-GW-REQ1103-03:** Multi-submitter via pool M=20 mapped from 200 fixtures (GW-11-06).
- [x] **AC-GW-REQ1103-04:** No SPA resident login required for Pass path (K1); primary = API+JSON (K4).

## Code touchpoints

- `tests/simulation_runner.py`, `tests/simulation_intake_http.py`, `Makefile` `simulate-life-sim`
- Admin bootstrap for pool: env refs in `life_sim_pool_m20.json` (no invent public resident APIs)

## Dependencies

- Done fixtures + profiles.
- Auth lock in package INDEX (pool 20 + map).
