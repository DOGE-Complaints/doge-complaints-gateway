# task-gw-seed-01-t06

## Meta
- **Story:** [STORY-GW-SEED-01](../STORY-GW-SEED-01-loader-and-hosted-readiness.md)
- **Type:** ops
- **Status:** ⚪ Todo
- **Package:** — (audit override, вне pkg-000036)
- **Skill declared:** python-pro
- **Depends on:** T01–T05
- **Wave:** audit override (`run_mode=gw_seed_01_audit_followup`)
- **Decision Ref:** [`audit-gw-seed-01-loader-and-hosted-readiness-2026-06-22.md`](../../../../../../analysis/audit-gw-seed-01-loader-and-hosted-readiness-2026-06-22.md) §2 R1

## Purpose
Закрыть audit R1: независимо подтвердить `CLUSTER_CRON_ENABLED=true` на hosted Railway (не schema-default). При `false` — выставить на таргете и зафиксировать evidence.

## Code Facts
- Env spec default — [`schema.py:216-218`](../../../../../../../src/core/config/schema.py#L216-L218) `CLUSTER_CRON_ENABLED` default=`"true"`
- Контрфакт переопределения — [`.env`](../../../../../../../.env) `CLUSTER_CRON_ENABLED=false` (локально)
- Startup логирует фактическое значение — [`asgi_app.py:100-106`](../../../../../../../src/core/api/asgi_app.py#L100-L106) `cron_enabled=%s`
- T01 R1 gap — [`hosted-readiness-checklist.md`](../task-gw-seed-01-t01-hosted-readiness-checklist-and-columnar-migrations/hosted-readiness-checklist.md) (PASS по schema-default only)
- Audit R1 — [`audit-gw-seed-01-...-2026-06-22.md`](../../../../../../analysis/audit-gw-seed-01-loader-and-hosted-readiness-2026-06-22.md) §2

## Acceptance / DoD
- (P0) Фактическое значение `CLUSTER_CRON_ENABLED` на Railway hosted зафиксировано в `railway-cron-env-evidence.md` (dashboard screenshot/export или deploy log `cron_enabled=True`)
- (P0) Если было `false` — установлено `true` на Railway + redeploy при необходимости; post-check подтверждает `cron_enabled=true`
- (P1) Обновить T01 `hosted-readiness-checklist.md` и `acceptance-verification-gw-seed-01-t01.md` — снять R1 qualifier
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P6)

## Where to change
- Railway Variables (operator ops) — `CLUSTER_CRON_ENABLED`
- Task artifacts: `railway-cron-env-evidence.md` in this task folder
- T01 artifacts (remediation note, no code)

## Out of scope
- G1 board fill (defer SEED-02)
- G2 local `.env` cron OFF (info only)
- Новый pkg / смена [`gateway-active-package.current.yaml`](../../../../../../gateway-active-package.current.yaml)
- Expose cron in `/ready` or `src/core/` code changes

## Verification commands
```bash
# Railway deploy logs (after restart/redeploy) — grep:
# startup.config ... cron_enabled=True

# Or Railway dashboard → Variables → CLUSTER_CRON_ENABLED=true
```
