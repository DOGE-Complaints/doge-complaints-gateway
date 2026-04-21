# STORY-M2-13-05: Geo timeout/retry policy hardening

## Meta
- Key: `STORY-M2-13-05`
- Parent Epic: [`../../EPIC-M2-13-demo-polishing.md`](../../EPIC-M2-13-demo-polishing.md)
- Type: Technical Story
- Status: Implemented (Waiting Acceptance/Commits)
- Stream: M2 Polishing
- Gap reference: `GAP-005`
- Skill declared: `python-pro`

## Story Goal
Уточнить и зафиксировать timeout/retry поведение geo resolver chain как проверяемый контракт, а не только fallback-эффект.

## AC / DoD
- [x] Timeout/retry/backoff политика явно отражена в коде или конфигурации.
- [x] Добавлены unit-тесты на retry-path и отказоустойчивость провайдеров.
- [x] `GAP-005` закрыт с воспроизводимой re-validation.

## Task Artifacts
- Task workspace: [`../../../task-m2-13-05-geo-timeout-retry-policy-hardening/README.md`](../../../task-m2-13-05-geo-timeout-retry-policy-hardening/README.md)
- Task specification: [`../../../task-m2-13-05-geo-timeout-retry-policy-hardening/task-m2-13-05-geo-timeout-retry-policy-hardening.md`](../../../task-m2-13-05-geo-timeout-retry-policy-hardening/task-m2-13-05-geo-timeout-retry-policy-hardening.md)
- Phase log: [`../../../task-m2-13-05-geo-timeout-retry-policy-hardening/BULLRUN-PHASE-LOG.md`](../../../task-m2-13-05-geo-timeout-retry-policy-hardening/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-13-05-geo-timeout-retry-policy-hardening/acceptance-verification-STORY-M2-13-05.md`](../../../task-m2-13-05-geo-timeout-retry-policy-hardening/acceptance-verification-STORY-M2-13-05.md)
