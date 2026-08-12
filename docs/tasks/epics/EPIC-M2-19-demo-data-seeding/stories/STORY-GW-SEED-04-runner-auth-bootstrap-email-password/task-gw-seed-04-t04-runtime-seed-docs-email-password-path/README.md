# task-gw-seed-04-t04

## Meta
- **Story:** [STORY-GW-SEED-04](../STORY-GW-SEED-04-runner-auth-bootstrap-email-password.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000051
- **Skill declared:** python-pro

## Purpose
Backlog §C + T04: sync runtime SSOT — [`seed-demo-data-runbook-ru.md`](../../../../../../runtime-docs/manuals/seed-demo-data-runbook-ru.md) §Шаг1 + предусловия; [`simulation-runner-manual.md`](../../../../../../runtime-docs/testing/simulation-runner-manual.md) env table, refusal codes, «где взять» → «свой verified аккаунт»; email+password path; requirement «аккаунт уже phone_verified».

## Code Facts
- Runbook stale token refs — [`seed-demo-data-runbook-ru.md:36-58`](../../../../../../runtime-docs/manuals/seed-demo-data-runbook-ru.md)
- Runner manual SSOT — [`simulation-runner-manual.md:47-61`](../../../../../../runtime-docs/testing/simulation-runner-manual.md)
- SSOT split — runbook = e2e chain; runner-manual = loader details (SEED-03 T04)

## Acceptance / DoD
- Traces parent AC#5: runbook + simulation-runner-manual + `.env.test.example` aligned (with T03)
- No `GATEWAY_USER_TOKEN` / `SMOKE_USER_BEARER_TOKEN` in these two runtime docs
- Document Supabase password grant as submit auth path (not OAuth authorize flow)
- Document 403/401 troubleshooting per backlog §B

## Where to change
- [`docs/runtime-docs/manuals/seed-demo-data-runbook-ru.md`](../../../../../../runtime-docs/manuals/seed-demo-data-runbook-ru.md)
- [`docs/runtime-docs/testing/simulation-runner-manual.md`](../../../../../../runtime-docs/testing/simulation-runner-manual.md)

## Out of scope
- Mass stale `/intake/stories` cleanup in other manuals
- `docs/tasks/**` historical GAUTH docs
- Code (T01–T02)

## Verification commands
```bash
rg 'GATEWAY_USER_EMAIL|GATEWAY_USER_PASSWORD' doge-complaints-gateway/docs/runtime-docs/manuals/seed-demo-data-runbook-ru.md doge-complaints-gateway/docs/runtime-docs/testing/simulation-runner-manual.md
rg 'GATEWAY_USER_TOKEN|SMOKE_USER_BEARER_TOKEN' doge-complaints-gateway/docs/runtime-docs/manuals/seed-demo-data-runbook-ru.md doge-complaints-gateway/docs/runtime-docs/testing/simulation-runner-manual.md && exit 1 || echo ok
```
