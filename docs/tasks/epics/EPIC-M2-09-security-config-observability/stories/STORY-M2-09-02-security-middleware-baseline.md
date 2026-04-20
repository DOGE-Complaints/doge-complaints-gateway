# STORY-M2-09-02: Security middleware baseline

## Meta
- Key: `STORY-M2-09-02`
- Parent Epic: [`../../EPIC-M2-09-security-config-observability.md`](../../EPIC-M2-09-security-config-observability.md)
- Type: Technical Story
- Status: Todo
- Stream: M2 Security/Ops
- Skill declared: `python-pro`

## Story Goal
Сервисная граница API: минимальная политика доверия к вызовам (например service token / allowlist) без замены IdP пользователя.

## AC / DoD
- [ ] Контракт «сервисной» аутентификации согласован с `requirements/19` (ссылка в коде/доке).
- [ ] Middleware или dependency guard для защищённых маршрутов.
- [ ] Тесты: отказ без креденшелов / успех с валидным токеном (stub).

## Task Artifacts
- Task workspace: [`../../../task-m2-09-02-security-middleware-baseline/README.md`](../../../task-m2-09-02-security-middleware-baseline/README.md)
- Task specification: [`../../../task-m2-09-02-security-middleware-baseline/task-m2-09-02-security-middleware-baseline.md`](../../../task-m2-09-02-security-middleware-baseline/task-m2-09-02-security-middleware-baseline.md)
- Phase log: [`../../../task-m2-09-02-security-middleware-baseline/BULLRUN-PHASE-LOG.md`](../../../task-m2-09-02-security-middleware-baseline/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-09-02-security-middleware-baseline/acceptance-verification-STORY-M2-09-02.md`](../../../task-m2-09-02-security-middleware-baseline/acceptance-verification-STORY-M2-09-02.md)
