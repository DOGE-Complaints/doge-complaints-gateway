# task-gw-rc-07-t02

## Meta
- **Story:** [STORY-GW-RC-07](../STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md)
- **Type:** verify
- **Status:** 🟢 Done
- **Package:** pkg-000047
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Сверить задеплоенную версию gateway на Railway с локальным HEAD (RC-04→06 commits applied on prod?).

## Code Facts
- RC-04 columnar — [`audit-gw-rc-04-columnar-model-migration-2026-06-20.md`](../../../../../../analysis/audit-gw-rc-04-columnar-model-migration-2026-06-20.md)
- `/ready` column checks — hosted green per audit CF-B
- Audit hypothesis — [`audit-gw-seed-02-...`](../../../../../../analysis/audit-gw-seed-02-dataset-expansion-for-clustering-2026-06-22.md) §CF-B (deploy drift vs local)

## Acceptance / DoD
- Artifact [`deploy-parity-summary.md`](./deploy-parity-summary.md): Railway build/commit or image tag vs local; RC-04→06 feature parity assessment
- BULLRUN phases complete
- [`acceptance-verification-gw-rc-07-t02.md`](./acceptance-verification-gw-rc-07-t02.md) signed

## Where to change
- Task artifact: `deploy-parity-summary.md`
- Acceptance: `acceptance-verification-gw-rc-07-t02.md`

## Out of scope
- Code fix (T04)

## Verification commands
```bash
curl -sS "https://dogestonia-tallinn.up.railway.app/ready" | jq .
# Railway dashboard / deploy logs — build SHA, startup version if logged
```
