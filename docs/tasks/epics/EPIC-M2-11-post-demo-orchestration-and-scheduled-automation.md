# EPIC-M2-11: Post-demo — Orchestration and Scheduled Automation

## Epic Meta
- Status: Draft
- Priority: Medium
- Owner: TBD
- Target: Post-demo (после EPIC-M2-01..M2-10 по продуктовому решению)

## Business Goal
Сделать **удобной** эксплуатационную автоматизацию (cron/queue/ручной replay) **поверх** уже реализованных доменных use-case, без дублирования логики и без обхода state machines.

## Problem Statement
Без явного «automation plane» фоновые задачи неизбежно превращаются в отдельные скрипты и расходятся с API-поведением.

## Scope
### In Scope
- контракт **job runner** / **named tasks**, вызывающих существующие application services через DI;
- политики idempotency/concurrency для длительных пересчётов (cluster/projection batches);
- метрики и structured logs для job execution (расширение observability baseline);
- документация operational runbook (какие задачи существуют, как запускать вручную).

### Out of Scope
- выбор конкретного cloud scheduler как обязательный deliverable (Kubernetes CronJob vs managed cron vs `pg_cron`) — остаётся решением инфраструктуры;
- изменение семантики EPIC-M2-05 (promotion/review) без отдельного product decision.

## Stakeholders
- CTO/Architecture
- Backend/DevOps
- Operations

## Dependencies
- EPIC-M2-01 (DI/config baseline)
- EPIC-M2-09 (observability baseline — метрики для jobs)
- Завершение доменных эпиков M2-02..M2-08 по минимуму стабильных use-case

## Success Metrics
- 0 критичных расхождений «API vs cron» на интеграционных сценариях;
- все фоновые сценарии покрыты trace + метриками latency/success rate.

## Epic Acceptance Criteria
- named tasks вызывают **только** application layer, не «сырой» SQL для доменных переходов;
- ручной запуск и расписание используют **один код path**;
- документированы ограничения concurrency и идемпотентности.

## Risks and Mitigation
- Риск: команда сочтёт cron «инфраструктурой» и обойдёт домен. Mitigation: quality gate и review по ADR/архитектуре `16`.

## Definition of Done
- automation plane внедрён согласно `docs/solution architecture/16-automation-orchestration-and-scheduled-jobs.md` и `docs/requirements/20-post-demo-orchestration-and-scheduled-jobs.md`.

## Initial Story Decomposition (Draft)
- STORY-M2-11-01: job/task registry and runner contract (calls ServiceFactory/use-cases)
- STORY-M2-11-02: idempotency + lease/concurrency policy for long-running recalculations
- STORY-M2-11-03: observability hooks for scheduled jobs (metrics + trace)
- STORY-M2-11-04: operator runbook for manual vs scheduled execution
