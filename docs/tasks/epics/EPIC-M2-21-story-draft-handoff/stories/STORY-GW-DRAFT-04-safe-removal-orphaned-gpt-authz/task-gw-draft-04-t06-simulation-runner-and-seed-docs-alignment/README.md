# task-gw-draft-04-t06-simulation-runner-and-seed-docs-alignment

## Meta
- **Story:** [STORY-GW-DRAFT-04](../STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md)
- **Type:** fix
- **Status:** 🟢 Done
- **Package:** pkg-000046
- **Skill declared:** python-pro
- **Depends on:** T04

## Purpose
Backlog T04 (part 2): [`tests/simulation_runner.py`](../../../../../../../tests/simulation_runner.py) — убрать `GATEWAY_USER_TOKEN`/`X-User-Token` для legacy `/intake/stories`; align с service-only route deps; обновить runtime seed/simulation docs если код изменился.

## Code Facts
- Simulation user token — [`simulation_runner.py`](../../../../../../../tests/simulation_runner.py) (~L172 `GATEWAY_USER_TOKEN`)
- Docs (GW-DRAFT-03 legacy labels) — [`simulation-runner-manual.md`](../../../../../../../docs/runtime-docs/testing/simulation-runner-manual.md), [`seed-demo-data-runbook-ru.md`](../../../../../../../docs/runtime-docs/manuals/seed-demo-data-runbook-ru.md)
- Legacy path — `POST /intake/stories` service-only after T04

## Acceptance / DoD
- Traces parent AC #6: `simulation_runner.py`/seed-docs aligned with service-only legacy intake
- No required `GATEWAY_USER_TOKEN` for default simulation path
- Docs state legacy intake = service token only (user submit = story-draft handoff)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3)

## Where to change
- [`tests/simulation_runner.py`](../../../../../../../tests/simulation_runner.py)
- [`docs/runtime-docs/testing/simulation-runner-manual.md`](../../../../../../../docs/runtime-docs/testing/simulation-runner-manual.md) (if code delta)
- [`docs/runtime-docs/manuals/seed-demo-data-runbook-ru.md`](../../../../../../../docs/runtime-docs/manuals/seed-demo-data-runbook-ru.md) (if code delta)

## Out of scope
Full hosted seed E2E; identity canon (GW-DRAFT-03 G1)

## Verification commands
```bash
rg 'GATEWAY_USER_TOKEN|X-User-Token' doge-complaints-gateway/tests/simulation_runner.py
cd doge-complaints-gateway && python tests/simulation_runner.py --help 2>/dev/null || true
```
