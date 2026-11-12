# STORY-GW-REQ11-03 — Profiled API replay + multi-fixture submitters

## Meta
- **Key:** `STORY-GW-REQ11-03-profiled-api-replay-multi-submitter`
- **Parent Epic:** [`../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md`](../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md)
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/INDEX.md)
- **Status:** ✅ Done (P3)
- **Тип:** tooling / replay orchestration
- **source:** [`../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md)
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md) §4.5, §4.7; **GW-11-04**, **GW-11-06**; D1/D2; K1/K4
- **decision_ref:** backlog REQ11-03 · REQ55 §4.5/§4.7 · GW-11-04/06 · D1/D2 · K1/K4 · pool M=20
- **Skill declared:** python-pro
- **Operative package:** [`../../../../gateway-active-packages/pkg-000102-20260929-gw-req11-03-profiled-api-replay-multi-submitter.yaml`](../../../../gateway-active-packages/pkg-000102-20260929-gw-req11-03-profiled-api-replay-multi-submitter.yaml)
- **Git:** `dev`
- **Operator lock (auth):** pool **M=20** admin-bootstrapped verified users; map **200** fixture users → pool; no SPA login per run
- **Зависит от:** STORY-GW-REQ11-01, STORY-GW-REQ11-02
- **Blocks:** STORY-GW-REQ11-04
- **Scaffolded:** 2026-09-29T14:13:56Z
- **P3 Done:** 2026-09-29T14:21:44Z

## Nested tasks (pkg-000102)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req11-03-t01-wire-fixtures-and-profile`](./task-gw-req11-03-t01-wire-fixtures-and-profile/README.md) | Done |
| T02 | [`task-gw-req11-03-t02-pool-bootstrap-m20`](./task-gw-req11-03-t02-pool-bootstrap-m20/README.md) | Done |
| T03 | [`task-gw-req11-03-t03-map-200-to-pool-multi-bearer`](./task-gw-req11-03-t03-map-200-to-pool-multi-bearer/README.md) | Done |
| T04 | [`task-gw-req11-03-t04-wipe-profiled-replay-runner`](./task-gw-req11-03-t04-wipe-profiled-replay-runner/README.md) | Done |
| T05 | [`task-gw-req11-03-t05-operator-docs-no-spa`](./task-gw-req11-03-t05-operator-docs-no-spa/README.md) | Done |
| T06 | [`task-gw-req11-03-t06-story-gate`](./task-gw-req11-03-t06-story-gate/README.md) | Done |
| T07 | [`task-gw-req11-03-t07-audit-g2-as-of-done-ssot`](./task-gw-req11-03-t07-audit-g2-as-of-done-ssot/README.md) | Done (`gw_req11_03_audit_followup`) |

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
| stash→submit HTTP | `tests/simulation_intake_http.py:184-217` `post_stash_and_submit_http` |
| Single Bearer via email+password | `simulation_intake_http.py:79-101` `resolve_user_bearer_token` |
| 403 messaging assumes `phone_verified` | `simulation_intake_http.py:106-109`; `simulation-runner-manual.md` |
| Multi-fixture submitters / pool map | **Present** — `life_sim_pool_m20.json` + `life_sim_fixture_to_pool_map_v0_1.json` + `resolve_pool_slot_bearer_token` |

## Target / AC

- [x] **AC-GW-REQ1103-01:** Wipe/zero → profiled replay → stories enter gateway pipeline (D1 / GW-11-04).
- [x] **AC-GW-REQ1103-02:** Replay uses fixture scale from REQ11-01 (D2).
- [x] **AC-GW-REQ1103-03:** Multi-submitter via pool M=20 mapped from 200 fixtures (GW-11-06).
- [x] **AC-GW-REQ1103-04:** No SPA resident login required for Pass path (K1); primary = API+JSON (K4).

## Code touchpoints

- `tests/simulation_runner.py`, `tests/simulation_intake_http.py`, `Makefile:31-32`
- Admin bootstrap for pool: design at P3 (no invent public resident APIs)

## Dependencies

- Done fixtures + profiles.
- Auth lock in package INDEX (pool 20 + map).
