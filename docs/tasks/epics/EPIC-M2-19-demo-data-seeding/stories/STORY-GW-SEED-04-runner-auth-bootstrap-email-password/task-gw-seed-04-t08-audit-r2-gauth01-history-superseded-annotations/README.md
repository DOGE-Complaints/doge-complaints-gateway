# task-gw-seed-04-t08-audit-r2-gauth01-history-superseded-annotations

## Meta
- **Story:** [STORY-GW-SEED-04](../STORY-GW-SEED-04-runner-auth-bootstrap-email-password.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** audit override (not in pkg-000051)
- **Skill declared:** python-pro
- **Wave:** audit override (`run_mode=gw_seed_04_audit_followup`)
- **Depends on:** T07 (recommended same P6 batch)
- **Audit ref:** [`audit-gw-seed-04-runner-auth-bootstrap-2026-07-11`](../../../../../../analysis/audit-gw-seed-04-runner-auth-bootstrap-2026-07-11.md) **R2**

## Purpose
Пометить исторические GAUTH-01 audit-записи в bullrun, что seed manuals больше **не** документируют `GATEWAY_USER_TOKEN` (superseded by GW-SEED-04 email+password). Сохранить факт 2026-06-25, убрать ambiguity для оператора.

## Code Facts
- Audit finding — [`audit-gw-seed-04-runner-auth-bootstrap-2026-07-11.md:38-39`](../../../../../../analysis/audit-gw-seed-04-runner-auth-bootstrap-2026-07-11.md) R2 LOW
- History bullet — [`bullrun-launch-index.md:72`](../../../../bullrun-launch-index.md) «seed manuals … `GATEWAY_USER_TOKEN`»
- Task row — [`bullrun-launch-index.md:802`](../../../../bullrun-launch-index.md) TASK-GW-GAUTH-01-T06 Notes
- Current runtime truth — [`simulation-runner-manual.md`](../../../../../../../docs/runtime-docs/testing/simulation-runner-manual.md) email+password (GW-SEED-04 T04)

## Acceptance / DoD
- [x] [`bullrun-launch-index.md:72`](../../../../bullrun-launch-index.md) — добавить «(superseded by GW-SEED-04)» или эквивалент: manuals с 2026-07-11 → email+password
- [x] [`bullrun-launch-index.md:802`](../../../../bullrun-launch-index.md) TASK-GW-GAUTH-01-T06 Notes — та же пометка; исторический факт T06 Done 2026-06-25 сохранён
- [x] Не переписывать audit-артефакты GAUTH-01 (`docs/analysis/audit-gw-gauth-01-*.md`) — history only
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-seed-04-t08.md`](./acceptance-verification-gw-seed-04-t08.md) signed (Date post P6 verify only)

## Where to change
- `doge-complaints-gateway/docs/tasks/bullrun-launch-index.md` — `:72`, `:802`

## Out of scope
- Rewriting GAUTH-01 T06 task README or acceptance (historical PASS)
- Runtime manual body edits (already GW-SEED-04)
- Code / pytest

## Verification commands
```bash
rg 'superseded by GW-SEED-04' doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
# expect ≥2 matches (lines ~72 and ~802) after P6
```
