# EPIC-M2-10: Demo-to-Pilot Adapters (Tokenization-Ready Foundations)

## Epic Meta
- Status: Draft
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

## Initial Story Decomposition (Draft)
- STORY-M2-10-01: define adapter interfaces (wallet/push/sign/tx)
- STORY-M2-10-02: implement demo stub adapters
- STORY-M2-10-03: implement feature-flag switching logic
- STORY-M2-10-04: prepare pilot activation playbook
