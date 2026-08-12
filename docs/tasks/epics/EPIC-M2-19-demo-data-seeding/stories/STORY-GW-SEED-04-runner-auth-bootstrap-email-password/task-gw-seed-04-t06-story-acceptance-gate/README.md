# task-gw-seed-04-t06

## Meta
- **Story:** [STORY-GW-SEED-04](../STORY-GW-SEED-04-runner-auth-bootstrap-email-password.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000051
- **Skill declared:** python-pro
- **Depends on:** T01–T05

## Purpose
Backlog T06: story acceptance gate per [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md).

## Code Facts
- Parent AC — [`STORY-GW-SEED-04-runner-auth-bootstrap-email-password.md`](../STORY-GW-SEED-04-runner-auth-bootstrap-email-password.md) §Acceptance Criteria
- Active pkg — [`pkg-000051-20260711-gw-seed-04-runner-auth-bootstrap-email-password.yaml`](../../../../../../gateway-active-packages/pkg-000051-20260711-gw-seed-04-runner-auth-bootstrap-email-password.yaml)
- Gate grep scope (backlog T06): `src/` + `tests/` + active runtime docs; exclude `docs/analysis/` and historical audit/task docs

## Acceptance / DoD
- All 6 parent AC PASS in [`story-acceptance-gate-STORY-GW-SEED-04.md`](./story-acceptance-gate-STORY-GW-SEED-04.md)
- `rg 'GATEWAY_USER_TOKEN|SMOKE_USER_BEARER_TOKEN'` → 0 in `src/`, `tests/`, `docs/runtime-docs/` (exclude analysis + docs/tasks history per backlog)
- `python3 -m pytest -q -m "not live_integration"` green
- `builder_resolve_queue --project gateway --verify` → ok 6 paths
- Manual smoke per runbook §Шаг2 documented for operator (Date in gate only after P3 live verify)

## Where to change
- [`story-acceptance-gate-STORY-GW-SEED-04.md`](./story-acceptance-gate-STORY-GW-SEED-04.md)
- [`bullrun-launch-index.md`](../../../../../../bullrun-launch-index.md) story row on PASS

## Out of scope
- P8 commits (unless operator requests)
- Gateway_builder.plan.md changes

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"
rg 'GATEWAY_USER_TOKEN|SMOKE_USER_BEARER_TOKEN' doge-complaints-gateway/src doge-complaints-gateway/tests doge-complaints-gateway/docs/runtime-docs
```
