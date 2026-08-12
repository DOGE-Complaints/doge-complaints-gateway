# task-gw-rc-04-t01

## Meta
- **Story:** [STORY-GW-RC-04](../STORY-GW-RC-04-columnar-model-migration.md)
- **Type:** docs
- **Status:** 🔵 Done
- **Package:** pkg-000033
- **Skill declared:** python-pro
- **Depends on:** GW-RC-01..03 (read contract stable)
- **Wave gate:** T02–T08 blocked until ADR artifact signed

## Purpose
ADR: финальная схема колонок (scalars + jsonb vs explode i18n); решение по `geo`; судьба view `issues_dashboard` (migration [`20260427_1615_spa_issues_dashboard_view.sql`](../../../../../../../supabase/migrations/20260427_1615_spa_issues_dashboard_view.sql)).

## Code Facts
- Duplicate write — [`db_supabase.py:617-638`](../../../../../../../src/core/infrastructure/db_supabase.py#L617-L638)
- Contract field set — [`dto.py:26-50`](../../../../../../../src/core/projection/dto.py#L26-L50)
- Current table — [`000_full_init.sql:84-91`](../../../../../../../supabase/bootstrap/000_full_init.sql#L84-L91)
- View reads `payload_json->>` — [`20260427_1615_spa_issues_dashboard_view.sql`](../../../../../../../supabase/migrations/20260427_1615_spa_issues_dashboard_view.sql)

## Acceptance / DoD
- Traces parent AC#1: ADR documents i18n/geo representation and view fate
- Resolves open questions from pipeline story (or documents explicit defer with rationale)
- ADR artifact path linked from story Product decisions
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- New ADR markdown in task folder (e.g. `adr-column-schema-d-rc-5.md`)

## Out of scope
- SQL migration (T02)
- Runtime code changes

## Verification commands
```bash
# docs-only task — review ADR completeness against parent AC#1
test -f docs/tasks/epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-04-columnar-model-migration/task-gw-rc-04-t01-adr-column-schema-and-view-decision/adr-column-schema-d-rc-5.md
```
