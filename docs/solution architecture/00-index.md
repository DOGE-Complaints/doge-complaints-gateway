# DOGEComplaints Module 2 — Solution Architecture (Demo)

## Назначение

Этот пакет описывает целевую solution architecture для Demo-версии Module 2 (Web2 Core / Story Intelligence Layer):
- без активного blockchain runtime в demo;
- с заложенными интерфейсами и потоками для pilot (tokenization-ready);
- с полной совместимостью с текущим SPA-контрактом Issue.

Источник требований: `docs/requirements/*`  
Архитектурные референсы: паттерны из проекта `node` (DI, orchestration, validation, upload/sign/callback design).

## Структура

- `01-scope-and-constraints.md`
- `02-requirements-traceability.md`
- `03-target-architecture-overview.md`
- `04-module-api-and-contract-layer.md`
- `05-module-story-intake-and-store.md`
- `06-module-story-intelligence-and-cluster-engine.md`
- `07-module-distinct-issue-and-spa-projection.md`
- `08-module-evidence-pack-and-lineage.md`
- `09-module-geo-intelligence.md`
- `10-data-architecture-and-state-model.md`
- `11-cross-cutting-security-config-observability.md`
- `12-integration-adapters-demo-vs-pilot.md`
- `13-testing-and-quality-architecture.md`
- `14-adr-log.md`
- `15-phased-implementation-plan.md`
- `16-automation-orchestration-and-scheduled-jobs.md` (post-demo: cron/queue vs единый use-case слой)
- `17-post-demo-story-tokenization-context.md` (указатель на post-demo токенизацию/уведомления; детали в `requirements/21`)

## Принцип чтения

1. Сначала `01` + `03` (контекст и общая схема).  
2. Затем модульные документы `04-09`.  
3. Потом cross-cutting и delivery `10-15`.  
4. Для post-demo оркестрации — `16` и требования `docs/requirements/20-*.md`.  
5. Для post-demo токенизации/уведомлений — `17` + `docs/requirements/21-*.md`.
