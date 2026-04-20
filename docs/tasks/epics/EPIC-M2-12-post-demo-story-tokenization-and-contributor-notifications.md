# EPIC-M2-12: Post-demo — Story-level Tokenization and Contributor Notifications

## Epic Meta
- Status: Draft
- Priority: Medium
- Owner: TBD
- Target: Post-demo; **срок не зафиксирован** (см. дисклеймер в требованиях)

## Business Goal
Исследовать и приоритизировать сценарий **вклада на уровне story** и **уведомляемости** авторов о попадании материала в **distinct issues**, с опорой на adapter-first и lineage, без обязательств для demo.

## Problem Statement
Без явного эпика post-demo продуктовые обсуждения (токенизация, on-chain/off-chain уведомления, территориальный обмен) размазываются по чатам и не попадают в backlog.

## Scope
### In Scope (когда эпик будет активирован)
- уточнение продукта: что фиксируется on-chain vs off-chain;
- событийная модель «story ↔ issue» после promotion/projection с machine-readable provenance;
- интеграция с **EPIC-M2-10** (адаптеры) без поломки demo-контуров;
- политики приватности и согласий для связи автора с issue.

### Out of Scope
- обязательная реализация в текущем demo;
- финальная экономика токена и governance сети.

## Stakeholders
- Product Lead
- CTO/Architecture
- Legal/Privacy (по мере зрелости)

## Dependencies
- EPIC-M2-05, EPIC-M2-06, EPIC-M2-07 (promotion, projection, evidence/lineage)
- EPIC-M2-10 (pilot adapters baseline)
- `docs/requirements/21-post-demo-story-tokenization-and-contributor-notifications.md`
- `docs/solution architecture/17-post-demo-story-tokenization-context.md`

## Success Metrics
- принятые архитектурные решения зафиксированы (ADR/decision log);
- PoC или pilot path не ломает SPA-контракт и story lineage.

## Epic Acceptance Criteria
- дисклеймер и границы MVP соблюдены (см. req `21`);
- нет скрытого scope creep в demo-код без feature flag.

## Risks and Mitigation
- Риск: преждевременная on-chain сложность. Mitigation: off-chain MVP уведомлений + явный decision gate.

## Definition of Done
- зафиксирован roadmap-пакет (что делаем в pilot vs позже) и обновлены открытые решения.

## Initial Story Decomposition (Draft)
- STORY-M2-12-01: product/architecture decision package (story-level asset model)
- STORY-M2-12-02: event model for “story included in issue” + provenance
- STORY-M2-12-03: notification channel strategy (off-chain first vs chain events)
- STORY-M2-12-04: privacy/consent and territorial sharing boundaries
