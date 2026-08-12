# EPIC-M2-09: Security, Config, Observability

## Epic Meta
- Status: In Progress
- Priority: Critical
- Owner: TBD
- Target: Cross-sprint (starts Sprint 1)

## Business Goal
Обеспечить production-grade операционную дисциплину с первого дня demo реализации.

## Problem Statement
Без базовой security/ops дисциплины demo быстро станет неуправляемым и небезопасным.

## Scope
### In Scope
- boundary auth/authz policies (**сервисная** аутентификация вызова API + политика доверия к `submitter` из тела запроса; OAuth пользователя остаётся на стороне GPT/IdP — см. `requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md` §5);
- secret-safe logging;
- centralized config schema;
- health endpoints and telemetry;
- failure mode strategy (fail-soft/fail-closed).

### Out of Scope
- full SIEM/SOC integration;
- enterprise IAM integration.

## Stakeholders
- CTO/Security
- Backend/DevOps
- QA

## Dependencies
- EPIC-M2-01 baseline

## Success Metrics
- 0 critical security regressions;
- 100% сервисов используют centralized config;
- observability dashboards покрывают ключевые потоки.

## Epic Acceptance Criteria
- security baseline policy документирована и внедрена;
- structured logs с trace_id включены;
- health and readiness endpoints работают;
- ключевые алерты и метрики определены.

## Risks and Mitigation
- Риск: команда откладывает ops “на потом”.  
  Mitigation: quality gate запрещает merge без минимального ops coverage.

## Definition of Done
- baseline security/ops practices enforced across all active modules.
- trace/debug observability wave delivered for intake -> cluster -> issue path.

## Связанная post-demo доработка (не часть обязательного scope эпика)

- Метрики и алерты для **scheduled / automation** job runs закладываются в **EPIC-M2-11** и архитектуру `docs/solution architecture/16-automation-orchestration-and-scheduled-jobs.md` (расширение раздела metrics в этом эпике при внедрении M2-11).

## Source Requirement (trace wave)
- [`req-trace-debug-observability.md`](../../requirements/req-trace-debug-observability.md)

## Stories (decomposed)

| Key | Story | Status |
|---|---|---|
| STORY-M2-09-01 | [Centralized config and env validation](./EPIC-M2-09-security-config-observability/stories/STORY-M2-09-01-centralized-config-and-env-validation.md) | Done (Committed) |
| STORY-M2-09-02 | [Security middleware baseline](./EPIC-M2-09-security-config-observability/stories/STORY-M2-09-02-security-middleware-baseline.md) | Done (Committed) |
| STORY-M2-09-03 | [Structured logging and tracing](./EPIC-M2-09-security-config-observability/stories/STORY-M2-09-03-structured-logging-and-tracing.md) | Done (Committed) |
| STORY-M2-09-04 | [Health checks and metrics](./EPIC-M2-09-security-config-observability/stories/STORY-M2-09-04-health-checks-and-metrics.md) | Done (Committed) |

| STORY-M2-09-05 | [Trace/debug observability hardening](./EPIC-M2-09-security-config-observability/stories/STORY-M2-09-05/STORY-M2-09-05-trace-debug-observability-hardening.md) | Todo |
| STORY-M2-09-06 | [Runtime failure observability and log diagnostics hardening](./EPIC-M2-09-security-config-observability/stories/STORY-M2-09-06/STORY-M2-09-06-runtime-failure-observability-hardening.md) | Todo |
| STORY-M2-09-08 | [Production logging noise reduction (REQ-45)](./EPIC-M2-09-security-config-observability/stories/STORY-M2-09-08-production-logging-noise-reduction-req45/STORY-M2-09-08-production-logging-noise-reduction-req45.md) | Done (Awaiting Commits) |
