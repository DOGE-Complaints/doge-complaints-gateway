# EPIC-M2-10: Demo-to-Pilot Adapters (Tokenization-Ready Foundations)

## Epic Meta
- Status: Implemented (stories committed; приёмка на стороне продукта — по pipeline)
- Priority: High
- Owner: TBD
- Target: Sprint 4

## Business Goal
Подготовить архитектурные адаптеры для перехода от demo к pilot без полного рефакторинга.

## Problem Statement
Если отложить adapter layer до pilot-фазы, demo-реализация станет техническим тупиком.

## Scope
### In Scope
- adapter contracts для wallet push/sign request/tx broadcast;
- demo stubs (in-memory) для всех adapter interfaces;
- feature-flag переключение demo/pilot режимов;
- интеграционный prepare/sign/callback skeleton без real chain.

### Out of Scope
- реальный blockchain broadcast;
- production wallet transport.

## Stakeholders
- CTO/Architecture
- Backend team
- Pilot program owner

## Dependencies
- EPIC-M2-01, EPIC-M2-07, EPIC-M2-09 completed

## Success Metrics
- pilot adapters включаются без breaking changes доменных модулей;
- demo flow проходит через те же интерфейсы, что и pilot.

## Epic Acceptance Criteria
- все external-facing пилотные потоки абстрагированы интерфейсами;
- demo stubs покрыты integration тестами;
- feature flags управляют режимами deterministic way;
- pilot activation checklist подготовлен.

## Risks and Mitigation
- Риск: интерфейсы будут “слишком демо-специфичны”.  
  Mitigation: contract-first design и ранний review с pilot stakeholders.

## Definition of Done
- архитектура готова к pilot включению адаптеров без пересборки core.

## Связанная post-demo область (отдельный эпик)

- Продуктовые сценарии **токенизации на уровне story** и **уведомлений авторам** не входят в обязательный deliverable этого эпика; ведутся в **EPIC-M2-12** и `docs/requirements/21-post-demo-story-tokenization-and-contributor-notifications.md` (дисклеймер post-demo).

## Stories (декомпозиция)

| Key | Документ |
|-----|----------|
| M2-10-01 | [`stories/STORY-M2-10-01-define-adapter-interfaces-wallet-push-sign-tx.md`](./EPIC-M2-10-demo-to-pilot-adapters/stories/STORY-M2-10-01-define-adapter-interfaces-wallet-push-sign-tx.md) |
| M2-10-02 | [`stories/STORY-M2-10-02-demo-stub-adapters.md`](./EPIC-M2-10-demo-to-pilot-adapters/stories/STORY-M2-10-02-demo-stub-adapters.md) |
| M2-10-03 | [`stories/STORY-M2-10-03-feature-flag-registry-and-bundle.md`](./EPIC-M2-10-demo-to-pilot-adapters/stories/STORY-M2-10-03-feature-flag-registry-and-bundle.md) |
| M2-10-04 | [`stories/STORY-M2-10-04-pilot-activation-playbook.md`](./EPIC-M2-10-demo-to-pilot-adapters/stories/STORY-M2-10-04-pilot-activation-playbook.md) |
