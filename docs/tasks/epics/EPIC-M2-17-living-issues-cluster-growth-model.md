# EPIC-M2-17: Living Issues Cluster Growth Model (Requirement 29)

## Epic Meta
- Status: Done
- Priority: High
- Owner: TBD
- Target: TBD

## Business Goal
Перейти к living-модели issue: один `cluster_id` -> один активный `DOGEIssue` с расширением существующего issue при новых волнах историй.

## Scope
### In Scope
- `create`/`extend` развилка в `IssueCreateService` через `find_promoted_by_cluster_id`.
- `extend_candidate()` в `IssuePromotionService`.
- Upsert/dedup инварианты persistence слоёв (`doge_issues`, embeddings, story links).
- Unit/integration/e2e покрытие AC-29-1..6.

### Out of Scope
- Изменение API boundary intake/cron beyond requirement 29.
- Новые внешние оркестраторы или очереди.

## Source Requirement
- [`29-living-issues-cluster-growth-model.md`](../../requirements/29-living-issues-cluster-growth-model.md)

## Stories

| Key | Story | Type | Status | Scope |
|-----|-------|------|--------|-------|
| M2-17-01 | [Living issues create/extend orchestration](./EPIC-M2-17-living-issues-cluster-growth-model/stories/STORY-M2-17-01/STORY-M2-17-01-living-issues-create-extend-orchestration.md) | implement | Done | Requirement 29 rollout: extend path, store invariants, tests. |
