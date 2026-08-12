# task-gw-rc-07-t01

## Meta
- **Story:** [STORY-GW-RC-07](../STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md)
- **Type:** analyze
- **Status:** 🟢 Done
- **Package:** pkg-000047
- **Skill declared:** python-pro

## Purpose
Воспроизвести CF-B на hosted и собрать evidence: curl response, trace_id, HTTP status/body, сравнение с `/ready`.

## Code Facts
- Route — [`asgi_app.py:429`](../../../../../../../src/core/api/asgi_app.py) `GET /tallinn/issues`
- Handler — [`handlers.py:368`](../../../../../../../src/core/api/handlers.py) `handle_tallinn_issues_list`
- Audit CF-B — [`audit-gw-seed-02-...-2026-06-22.md`](../../../../../../analysis/audit-gw-seed-02-dataset-expansion-for-clustering-2026-06-22.md) §3 (trace `d7581fb1-…`)
- RC-06 working baseline — [`tallinn-issues-live-response.json`](../../STORY-GW-RC-06-hosted-status-data-hygiene/task-gw-rc-06-t04-verify-tallinn-issues-and-board-cards/tallinn-issues-live-response.json)

## Acceptance / DoD
- Traces parent AC: `hosted-internal-error-evidence.md`: воспроизведение CF-B задокументировано.
- Artifact [`hosted-internal-error-evidence.md`](./hosted-internal-error-evidence.md): curl output, trace_id, timestamp
- BULLRUN phases complete
- [`acceptance-verification-gw-rc-07-t01.md`](./acceptance-verification-gw-rc-07-t01.md) signed (Date post live verify)

## Where to change
- Task artifact: `hosted-internal-error-evidence.md`
- Acceptance: `acceptance-verification-gw-rc-07-t01.md`

## Out of scope
- Root cause fix (T04)
- Code changes in this task

## Verification commands
```bash
curl -sS "https://dogestonia-tallinn.up.railway.app/tallinn/issues"
curl -sS "https://dogestonia-tallinn.up.railway.app/ready"
```
