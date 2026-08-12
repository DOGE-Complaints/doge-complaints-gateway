# task-gw-cab-01-t03-story-activity-query-service-metrics-and-status-map

## Meta
- **Story:** [STORY-GW-CAB-01](../STORY-GW-CAB-01-story-activity-api.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000052
- **Skill declared:** python-pro
- **Depends on:** T01, T02

## Purpose
Application service: загрузить истории автора, разрешить cabinet row status через issue projection + `issue_story_links`, посчитать metrics (`submitted`, `published`, `under_review`) per D-CAB01-1..3.

## Code Facts
- MVP envelope — pipeline story §MVP-контракт
- Issue links — [`db_sqlite.py:277`](../../../../../../../../src/core/infrastructure/db_sqlite.py#L277) `issue_story_links(issue_id, story_id, ...)`
- Issue read store — [`service_factory.py:117`](../../../../../../../../src/core/infrastructure/service_factory.py#L117) `get_issue_projection_read_store`
- Status mapping SSOT — SPA §0 line 23 (`PUBLISHED→published`, `DRAFT→under_review`)

## Acceptance / DoD
- [x] Traces parent AC-1: `data.metrics` + `data.stories[]` shape matches MVP contract
- [x] Row `status` values only `published` | `under_review`
- [x] `metrics.submitted` = count user stories; `published`/`under_review` split per D-CAB01-3
- [x] Stories without issue link handled per D-CAB01-1
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-cab-01-t03.md`](./acceptance-verification-gw-cab-01-t03.md) signed

## Where to change
- New module under `src/core/application/` (e.g. `story_activity.py` or `cabinet/`) — match project layout after read
- Wire via [`service_factory.py`](../../../../../../../../src/core/infrastructure/service_factory.py) if needed

## Out of scope
- FastAPI route (T04)
- OpenAPI (T04)

## Verification commands
```bash
cd doge-complaints-gateway
python3 -m pytest -q -k 'gw_cab_01 and (metrics or status_map)' --tb=short
```
