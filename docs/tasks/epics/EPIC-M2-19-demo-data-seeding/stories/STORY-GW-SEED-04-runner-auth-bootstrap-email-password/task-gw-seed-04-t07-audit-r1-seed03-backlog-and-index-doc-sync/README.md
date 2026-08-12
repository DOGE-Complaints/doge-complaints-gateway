# task-gw-seed-04-t07-audit-r1-seed03-backlog-and-index-doc-sync

## Meta
- **Story:** [STORY-GW-SEED-04](../STORY-GW-SEED-04-runner-auth-bootstrap-email-password.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** audit override (not in pkg-000051)
- **Skill declared:** python-pro
- **Wave:** audit override (`run_mode=gw_seed_04_audit_followup`)
- **Depends on:** T01–T06 (P3 Done)
- **Audit ref:** [`audit-gw-seed-04-runner-auth-bootstrap-2026-07-11`](../../../../../../analysis/audit-gw-seed-04-runner-auth-bootstrap-2026-07-11.md) **R1**

## Purpose
Устранить doc-drift после GW-SEED-04: operator-facing записи для GW-SEED-03 не должны направлять к удалённому `GATEWAY_USER_TOKEN`. Синхронизировать backlog story и bullrun index с email+password путём (GW-SEED-04).

## Code Facts
- Audit finding — [`audit-gw-seed-04-runner-auth-bootstrap-2026-07-11.md:35-36`](../../../../../../analysis/audit-gw-seed-04-runner-auth-bootstrap-2026-07-11.md) R1 MEDIUM
- Backlog drift — [`STORY-GW-SEED-03-end-to-end-seed-runbook.md:23-24`](../../../../backlog-stories/demo-data-seeding/STORY-GW-SEED-03-end-to-end-seed-runbook.md) всё ещё `GATEWAY_USER_TOKEN`
- Index GW-SEED-03 row — [`bullrun-launch-index.md:943`](../../../../bullrun-launch-index.md) уже email+password (verify; не регрессировать)
- Stale audit warning — [`bullrun-launch-index.md:944`](../../../../bullrun-launch-index.md) GW-SEED-04 row: «R1 MEDIUM строка GW-SEED-03 ниже ещё зовёт…» — устарело после fix §943
- Active code truth — [`simulation_intake_http.py:79`](../../../../../../../tests/simulation_intake_http.py) password grant; grep `GATEWAY_USER_TOKEN` в src/tests/runtime-docs = 0

## Acceptance / DoD
- [x] [`STORY-GW-SEED-03-end-to-end-seed-runbook.md`](../../../../backlog-stories/demo-data-seeding/STORY-GW-SEED-03-end-to-end-seed-runbook.md) §Env/Ops: `GATEWAY_USER_EMAIL`/`PASSWORD` + `SUPABASE_URL`/`ANON_KEY` (GW-SEED-04); без инструкции «положить GATEWAY_USER_TOKEN»
- [x] Bullrun GW-SEED-04 story row (`:944`) — убрать stale «R1 open» warning; audit summary без противоречия с §943
- [x] Bullrun GW-SEED-03 row (`:943`) — operator re-seed ops = email+password (без «используй GATEWAY_USER_TOKEN» как action)
- [x] `rg 'GATEWAY_USER_TOKEN'` в operator-facing строках GW-SEED-03 (backlog + bullrun §943) = 0 except historical «removed» prose if any
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-seed-04-t07.md`](./acceptance-verification-gw-seed-04-t07.md) signed (Date post P6 verify only)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/demo-data-seeding/STORY-GW-SEED-03-end-to-end-seed-runbook.md` — `:23-24`
- `doge-complaints-gateway/docs/tasks/bullrun-launch-index.md` — GW-SEED-03/04 rows §943–944; §audit follow-up `:81`

## Out of scope
- Runtime docs (already synced in T04 P3)
- Code / pytest
- P8 commits
- Rewriting GW-SEED-04 pipeline/backlog historical «as-is» sections (pre-implementation context)

## Verification commands
```bash
rg 'GATEWAY_USER_TOKEN' doge-complaints-gateway/docs/tasks/backlog-stories/demo-data-seeding/STORY-GW-SEED-03-end-to-end-seed-runbook.md
# expect 0 after P6
rg 'R1 MEDIUM.*GW-SEED-03.*ещё зовёт' doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
# expect 0 after P6
```
