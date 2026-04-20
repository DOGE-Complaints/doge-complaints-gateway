# STORY-M2-09-04: Health checks and metrics

## Meta
- Key: `STORY-M2-09-04`
- Parent Epic: [`../../EPIC-M2-09-security-config-observability.md`](../../EPIC-M2-09-security-config-observability.md)
- Type: Technical Story
- Status: Todo
- Stream: M2 Security/Ops
- Skill declared: `python-pro`

## Story Goal
Liveness/readiness (или расширение существующего health) и минимальные метрики для ключевых потоков (счётчики/экспозиция под Prometheus-совместимый scrape при необходимости).

## AC / DoD
- [ ] Договорённый контракт `/health` / `/ready` (или эквивалент в текущем ASGI).
- [ ] Базовые метрики (например запросы, ошибки) — in-process или текстовый endpoint.
- [ ] Тесты на доступность health.

## Task Artifacts
- Task workspace: [`../../../task-m2-09-04-health-checks-and-metrics/README.md`](../../../task-m2-09-04-health-checks-and-metrics/README.md)
- Task specification: [`../../../task-m2-09-04-health-checks-and-metrics/task-m2-09-04-health-checks-and-metrics.md`](../../../task-m2-09-04-health-checks-and-metrics/task-m2-09-04-health-checks-and-metrics.md)
- Phase log: [`../../../task-m2-09-04-health-checks-and-metrics/BULLRUN-PHASE-LOG.md`](../../../task-m2-09-04-health-checks-and-metrics/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-09-04-health-checks-and-metrics/acceptance-verification-STORY-M2-09-04.md`](../../../task-m2-09-04-health-checks-and-metrics/acceptance-verification-STORY-M2-09-04.md)
