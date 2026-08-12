# task-gw-rc-07-t06

## Meta
- **Story:** [STORY-GW-RC-07](../STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** audit override (not in pkg-000047)
- **Skill declared:** python-pro
- **Wave:** audit override (`run_mode=gw_rc_07_audit_followup`)
- **Depends on:** T05 (story gate PASS)
- **Audit ref:** [`audit-gw-rc-07-hosted-tallinn-issues-internal-error-2026-07-10`](../../../../../../analysis/audit-gw-rc-07-hosted-tallinn-issues-internal-error-2026-07-10.md) **G1**

## Purpose
Закрыть audit **G1**: снять мисатрибуцию CF-B (2026-06-22) к отсутствию `columnar_storage.py`. Зафиксировать: CF-B **causa undetermined** (prod self-resolved до P3 2026-07-10); отдельно — июльская missing-module регрессия GW-DRAFT-01 (`e832302` 2026-07-03 → `543a38b` 2026-07-08), не причина исходного INTERNAL_ERROR.

## Code Facts
- Misattributed narrative — [`../task-gw-rc-07-t02-deploy-version-parity-vs-local-rc/deploy-parity-summary.md`](../task-gw-rc-07-t02-deploy-version-parity-vs-local-rc/deploy-parity-summary.md), [`../task-gw-rc-07-t04-fix-hosted-read-path-root-cause/fix-summary.md`](../task-gw-rc-07-t04-fix-hosted-read-path-root-cause/fix-summary.md)
- Git timeline — audit §G1: CF-B 2026-06-22; import `columnar_storage` in `db_supabase.py` → `e832302` 2026-07-03; file created → `543a38b` 2026-07-08
- `/ready` `columns_v2` — DB column check ([`dependencies.py:79`](../../../../../../../src/core/api/dependencies.py)), distinct from Python module `columnar_storage.py`
- Operational outcome unchanged — hosted 9 cards verified 2026-07-10 ([`hosted-internal-error-evidence.md`](../task-gw-rc-07-t01-reproduce-and-collect-hosted-evidence/hosted-internal-error-evidence.md))

## Acceptance / DoD
- Traces audit G1: T02/T04 artifacts no longer attribute CF-B 2026-06-22 to missing `columnar_storage.py`
- Closure text states: CF-B self-resolved; June cause undetermined; July missing-module = separate incident (GW-DRAFT-01)
- Pipeline story §resolved questions corrected (no `543a38b` as CF-B fix)
- BULLRUN phases complete
- [`acceptance-verification-gw-rc-07-t06.md`](./acceptance-verification-gw-rc-07-t06.md) signed (Date post P6 verify only)

## Where to change
- [`../task-gw-rc-07-t02-deploy-version-parity-vs-local-rc/deploy-parity-summary.md`](../task-gw-rc-07-t02-deploy-version-parity-vs-local-rc/deploy-parity-summary.md)
- [`../task-gw-rc-07-t04-fix-hosted-read-path-root-cause/fix-summary.md`](../task-gw-rc-07-t04-fix-hosted-read-path-root-cause/fix-summary.md)
- [`../STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md`](../STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md) §resolved questions

## Out of scope
- Re-opening T05 gate (operational PASS stands)
- Historical Railway logs ~2026-06-22 (audit G1 option b)
- R1 backlog sync, G3 pkg-000038 superseded (`activation: none`)
- `src/core/` code changes

## Verification commands
```bash
rg 'columnar_storage.*CF-B|deploy drift.*543a38b' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-07-hosted-tallinn-issues-internal-error/task-gw-rc-07-t0{2,4}*/
# expect corrected narrative after P6
```
