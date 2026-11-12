# STORY-GW-REQ11-02 — Named profiles: local + Uus Veerenni deploy

## Meta
- **Key:** `STORY-GW-REQ11-02-named-profiles-local-uus-veerenni`
- **Parent Epic:** [`../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md`](../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md)
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Тип:** config / profiled targets
- **source:** [`../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni.md`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni.md)
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md) §4.4; **GW-11-03**; D3
- **decision_ref:** backlog REQ11-02 · REQ55 §4.4 · GW-11-03 · D3 · local-five lock
- **Skill declared:** python-pro · soft code-documenter
- **Operative package:** [`../../../../gateway-active-packages/pkg-000101-20260929-gw-req11-02-named-profiles-local-uus-veerenni.yaml`](../../../../gateway-active-packages/pkg-000101-20260929-gw-req11-02-named-profiles-local-uus-veerenni.yaml)
- **Git:** `dev`
- **Operator lock (`local`):** identity 8100, gateway 8000, threads 8001, aibridge 8080, spa 5173
- **Зависит от:** —
- **Blocks:** STORY-GW-REQ11-03
- **Scaffolded:** 2026-09-29T13:56:20Z
- **P3 Done:** 2026-09-29T14:00:57Z
- **Gate:** [`task-gw-req11-02-t04-story-gate/story-acceptance-gate-STORY-GW-REQ11-02.md`](./task-gw-req11-02-t04-story-gate/story-acceptance-gate-STORY-GW-REQ11-02.md) PASS
- **Run-summary:** [`../../../../run-reports/run-summary-20260929-1400-gw-req11-02-p3.md`](../../../../run-reports/run-summary-20260929-1400-gw-req11-02-p3.md)
## Nested tasks (pkg-000101)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req11-02-t01-profile-local-five`](./task-gw-req11-02-t01-profile-local-five/README.md) | Done |
| T02 | [`task-gw-req11-02-t02-profile-uus-veerenni-deploy`](./task-gw-req11-02-t02-profile-uus-veerenni-deploy/README.md) | Done |
| T03 | [`task-gw-req11-02-t03-env-refs-and-selection-doc`](./task-gw-req11-02-t03-env-refs-and-selection-doc/README.md) | Done |
| T04 | [`task-gw-req11-02-t04-story-gate`](./task-gw-req11-02-t04-story-gate/README.md) | Done |
| T05 | [`task-gw-req11-02-t05-audit-g1-as-of-done-ssot`](./task-gw-req11-02-t05-audit-g1-as-of-done-ssot/README.md) | Done (audit follow-up) |

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
