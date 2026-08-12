# task-gw-seed-04-t03

## Meta
- **Story:** [STORY-GW-SEED-04](../STORY-GW-SEED-04-runner-auth-bootstrap-email-password.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000051
- **Skill declared:** python-pro

## Purpose
Backlog §C + T03: заменить блок `GATEWAY_USER_TOKEN` в [`.env.test.example`](../../../../../../../.env.test.example) на 4 переменные из backlog таблицы A (`GATEWAY_USER_EMAIL`, `GATEWAY_USER_PASSWORD`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`).

## Code Facts
- Current example — [`.env.test.example:13-15`](../../../../../../../.env.test.example) `GATEWAY_USER_TOKEN`
- Unchanged vars per backlog: `GATEWAY_API_TOKEN`, `GATEWAY_URL`, `SIMULATION_CANVAS_PATH`
- D-SEED04-3: remove `GATEWAY_USER_TOKEN` / `SMOKE_USER_BEARER_TOKEN` completely

## Acceptance / DoD
- Traces parent AC#1: example documents 4 new vars with comments (phone_verified account, SPA `VITE_*` source)
- `GATEWAY_USER_TOKEN` and `SMOKE_USER_BEARER_TOKEN` absent from `.env.test.example`
- Operator-facing comment: account must be phone_verified before seed

## Where to change
- [`doge-complaints-gateway/.env.test.example`](../../../../../../../.env.test.example) only

## Out of scope
- Operator local `.env.test` (not committed)
- Runtime runbook/manual (T04)
- Code changes (T01)

## Verification commands
```bash
rg 'GATEWAY_USER_EMAIL|GATEWAY_USER_PASSWORD|SUPABASE_ANON_KEY' doge-complaints-gateway/.env.test.example
rg 'GATEWAY_USER_TOKEN|SMOKE_USER_BEARER_TOKEN' doge-complaints-gateway/.env.test.example && exit 1 || echo ok
```
