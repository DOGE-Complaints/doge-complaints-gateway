# task-gw-rc-06-t04

## Meta
- **Story:** [STORY-GW-RC-06](../STORY-GW-RC-06-hosted-status-data-hygiene.md)
- **Type:** verify
- **Status:** ⚪ Todo
- **Package:** pkg-000035
- **Skill declared:** python-pro
- **Depends on:** T01–T03

## Purpose
Верификация: `GET /tallinn/issues` → board-valid `status` + непустой текст; SPA-доска показывает карточки.

## Code Facts
- Read API — [`STORY-M2-06-06`](../../STORY-M2-06-06-tallinn-issues-read-api-req24/STORY-M2-06-06-tallinn-issues-read-api-req24.md) `GET /tallinn/issues`
- Board vocab — [`enums.py:6-11`](../../../../../../../src/core/projection/enums.py#L6-L11) `{NEW, IN_REVIEW, PUBLISHED}`
- Parent AC — [`STORY-GW-RC-06-hosted-status-data-hygiene.md`](../STORY-GW-RC-06-hosted-status-data-hygiene.md) §Acceptance Criteria

## Acceptance / DoD
- Traces parent AC#1: no `promoted` in API response (board-vocab only)
- Traces parent AC#3: `GET /tallinn/issues` отдаёт валидные карточки; доска не пустая
- curl/log evidence saved in task folder
- Board screenshot or operator sign-off captured (optional artifact)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- Task verification artifacts only
- Live hosted gateway + SPA (manual verify)

## Verification commands
```bash
curl -s "$GATEWAY_BASE/tallinn/issues" | jq '.issues[] | {id, status, title}'
# Expect: status in {NEW, IN_REVIEW, PUBLISHED}; title/summary non-empty for displayed cards
```
