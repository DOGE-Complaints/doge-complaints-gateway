# task-gw-seed-01-t07

## Meta
- **Story:** [STORY-GW-SEED-01](../STORY-GW-SEED-01-loader-and-hosted-readiness.md)
- **Type:** ops
- **Status:** ⚪ Todo
- **Package:** — (audit override, вне pkg-000037)
- **Skill declared:** python-pro
- **Depends on:** T01–T05
- **Wave:** audit override (`run_mode=gw_seed_02_audit_cf_a_followup`)
- **Decision Ref:** [`audit-gw-seed-02-dataset-expansion-for-clustering-2026-06-22.md`](../../../../../../analysis/audit-gw-seed-02-dataset-expansion-for-clustering-2026-06-22.md) §3 CF-A; supersedes T06 R1 path when empirical evidence sufficient

## Purpose
Закрыть SEED-01 audit R1/G1 **эмпирическим** доказательством: hosted cron сработал и создал issue-карточки (1→8 `doge_issues`), без обязательного Railway dashboard для `CLUSTER_CRON_ENABLED`.

## Code Facts
- Cron batch — [`cluster_orchestrator.py:156-197`](../../../../../../../src/core/application/cluster_orchestrator.py#L156-L197) `process_all_pending`
- Env default — [`schema.py:216-218`](../../../../../../../src/core/config/schema.py#L216-L218) `CLUSTER_CRON_ENABLED` default=`"true"`
- T06 railway path — [`../task-gw-seed-01-t06-verify-hosted-cluster-cron-enabled-railway-env/README.md`](../task-gw-seed-01-t06-verify-hosted-cluster-cron-enabled-railway-env/README.md) (BLOCKED; optional supplement)
- CF-A audit — [`audit-gw-seed-02-...-2026-06-22.md`](../../../../../../analysis/audit-gw-seed-02-dataset-expansion-for-clustering-2026-06-22.md) §3 CF-A (8 PUBLISHED rows, 7 new INCIDENT ~2026-06-22)
- SEED-01 R1 — [`audit-gw-seed-01-...-2026-06-22.md`](../../../../../../analysis/audit-gw-seed-01-loader-and-hosted-readiness-2026-06-22.md) §2

## Acceptance / DoD
- (P0) `cf-a-cron-empirical-evidence.md`: hosted `doge_issues` count before/after, sample issue_ids, clustering timestamps (live verify)
- (P0) Подтверждено: 7+ новых issue от cron-кластеризации (не ручной seed)
- (P1) T01 `hosted-readiness-checklist.md` — снять R1 qualifier (cron enabled by empirical proof)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P6)

## Where to change
- Task artifacts: `cf-a-cron-empirical-evidence.md`, `acceptance-verification-gw-seed-01-t07.md`
- T01 `hosted-readiness-checklist.md` (remediation note only)

## Out of scope
- CF-B hosted `/tallinn/issues` INTERNAL_ERROR (GW-RC-07)
- Railway env screenshot (optional; T06 path)
- Новый pkg / смена [`gateway-active-package.current.yaml`](../../../../../../gateway-active-package.current.yaml)
- `src/core/` code changes

## Verification commands
```bash
# Hosted Supabase SQL (or REST):
# SELECT count(*) FROM doge_issues WHERE status = 'PUBLISHED';
# SELECT issue_id, status, created_at FROM doge_issues ORDER BY created_at DESC LIMIT 10;
```
