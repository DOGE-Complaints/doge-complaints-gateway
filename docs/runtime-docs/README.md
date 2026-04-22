# Runtime Docs: CTO Guide

## Контекст и управленческий вопрос

Этот пакет отвечает на вопрос: **что именно уже реализовано в runtime `doge-complaints-gateway`, насколько это операционно надежно сейчас, и какие расширения остаются roadmap, а не фактом**.

Документы ориентированы на архитектурное и операционное управление: где технические границы, какой риск-профиль у текущего режима, и какие изменения нужны для перехода к следующему уровню зрелости.

## Scope and truth source

Единственный источник фактов для этого пакета:

- Runtime code: `src/core/**`
- Test evidence: `tests/**`
- Contract baseline: `docs/requirements/**`
- Architectural intent baseline: `docs/solution architecture/**`
- Epic delivery evidence: `docs/tasks/**`
- Analysis method: `/.cursor/rules/analysis.mdc`

## Метод чтения и правило достоверности

Каждый профильный документ разделен на:

1. `Current state (implemented now)` — фактическое поведение в коде.
2. `Planned target` — целевой контур, который еще не внедрен.
3. `Gaps / risks` — операционные и архитектурные ограничения.

Если утверждение нельзя доказать ссылкой на `src/core`/`tests`, оно не считается частью текущего runtime baseline.

## Карта документов и управленческие вопросы

1. [Architecture & Layers (as-is)](./architecture-and-layers-as-is.md)  
   Вопрос: как устроена ответственность слоев, где реальные границы и как контролируется architectural drift.
2. [Security, Env, API Access](./security-env-api-access.md)  
   Вопрос: как устроен service-to-service доступ, где trust boundary, и как включается строгая защита.
   Дополнительно: где и как в runtime проходит user identifier (`submitter.external_user_id`) и как он связывается с `StoryRecord`.
3. [Arweave / On-chain Status and Runbook](./arweave-status-and-runbook.md)  
   Вопрос: что реально есть в chain-контуре сейчас, а что остается pilot roadmap.
4. [Test Matrix by Type, Layer and Mocks](./test-matrix-by-type-layer-mocks.md)  
   Вопрос: какую уверенность дает текущий набор тестов и где остаются blind spots.
5. [Database State and Integration Roadmap](./database-state-and-integration-roadmap.md)  
   Вопрос: каков фактический persistence baseline и что нужно для перехода к real DB.
6. [Operations Playbook](./operations-playbook.md)  
   Вопрос: как запускать и сопровождать текущий runtime, и как готовиться к DB/chain расширениям.
7. [Quickstart: server/env](./server-env-quickstart.md)  
   Вопрос: как быстро поднять локальное окружение, выставить env и проверить runtime boundary стандартным dev-путем.
8. [Cross-check and quality gates](./cross-check-and-quality-gates.md)  
   Вопрос: как поддерживать консистентность документации и верификацию claims.

## Дополнительные приложения

- [Карта доказательств (claim-to-source)](./appendix/evidence-trace-map-ru.md)
- [Architecture deep dive (RU)](./appendix/architecture-deep-dive-ru.md)
- [Security operational scenarios (RU)](./appendix/security-operational-scenarios-ru.md)
- [Testing rationale (RU)](./appendix/testing-rationale-ru.md)

## English API reference package

- [OpenAPI 3.1 spec](./api-reference/openapi.yaml)
- [Narrative API reference](./api-reference/API_REFERENCE.md)
  - Включает отдельный раздел `Identity linkage for stories` с полями submitter и фактическим status маршрутизации.

## Current runtime boundary

- Пакет описывает **non post-demo runtime baseline**.
- Темы `requirements/20` и `requirements/21` трактуются только как future dependencies.
