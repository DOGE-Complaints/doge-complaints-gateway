# EPIC-M2-13: Demo Polishing (Gap Closure for Non Post-demo Scope)

## Epic Meta
- Status: In Progress
- Priority: High
- Owner: TBD
- Target: Sprint 5

## Business Goal
Закрыть выявленные разрывы соответствия (P1/P2) после валидации `requirements/01..19` и epic AC `M2-01..M2-10`, чтобы довести demo-контур до полного и проверяемого соответствия без расширения post-demo scope.

## Problem Statement
По итогам Web2 Node Validation найдено 7 gap-областей (`GAP-001..GAP-007`), которые не блокируют текущую работу, но мешают заявлять полное соответствие в деталях архитектуры, контрактов и критериев приемки.

## Scope
### In Scope
- закрытие `GAP-001..GAP-007` из `docs/analysis/04-gap-backlog-and-revalidation.md`;
- углубление story lifecycle переходов и тестов;
- расширение intake-контракта в части non-post-demo клаузы `requirements/19`;
- усиление privacy/PII-min поведения в runtime и тестах;
- выравнивание config/flags инжекции и geo retry/timeout политики;
- дооформление проверяемых ops-артефактов по метрикам/алертам в рамках активного demo-контекста.

### Out of Scope
- любые post-demo требования `requirements/20`, `requirements/21`;
- эпики `M2-11`, `M2-12`;
- новый функционал вне списка gap-областей.

## Stakeholders
- CTO/Architecture
- Backend team
- QA
- Product owner (для приемки обновлённого compliance статуса)

## Dependencies
- Завершены baseline эпики `M2-01..M2-10`.
- Актуален audit-пакет:
  - `docs/analysis/01-fr-functional-section-matrix-filled.md`
  - `docs/analysis/02-requirements-01-19-coverage-filled.md`
  - `docs/analysis/03-epic-ac-m2-01-m2-10-filled.md`
  - `docs/analysis/04-gap-backlog-and-revalidation.md`
  - `docs/analysis/05-final-compliance-report.md`

## Success Metrics
- 0 открытых `P1` в gap backlog;
- для каждого закрытого gap есть re-validation evidence;
- обновлённый compliance-отчёт без критичных/высоких разрывов по non-post-demo scope.

## Epic Acceptance Criteria
- все gap-строки `GAP-001..GAP-007` имеют статус `fixed` или `accepted risk` с обоснованием;
- для каждого gap выполнен и задокументирован re-test set;
- `requirements/01..19` и AC `M2-01..M2-10` повторно провалидированы по той же verdict-модели (`Confirmed/Partial/Not Found/Doc-only`);
- соблюдается правило мышления `/.cursor/rules/analysis.mdc` без предположений.

## Risks and Mitigation
- Риск: расширение intake-контракта нарушит текущую совместимость.
  Mitigation: additive изменения + контрактные тесты до/после.
- Риск: «косметическое» закрытие gap без измеримого эффекта.
  Mitigation: обязательная re-validation матрица и evidence на уровне тест-кейсов/команд.

## Definition of Done
- stories `M2-13-01..M2-13-07` завершены;
- gap backlog обновлён и не содержит открытых `P1`;
- финальный compliance report переиздан с новым статусом.

## Stories (декомпозиция)

| Key | Документ |
|-----|----------|
| M2-13-01 | [`stories/STORY-M2-13-01-story-lifecycle-readiness-transitions.md`](./EPIC-M2-13-demo-polishing/stories/STORY-M2-13-01-story-lifecycle-readiness-transitions.md) |
| M2-13-02 | [`stories/STORY-M2-13-02-intake-envelope-parity-requirements-19.md`](./EPIC-M2-13-demo-polishing/stories/STORY-M2-13-02-intake-envelope-parity-requirements-19.md) |
| M2-13-03 | [`stories/STORY-M2-13-03-author-lineage-proof-tests.md`](./EPIC-M2-13-demo-polishing/stories/STORY-M2-13-03-author-lineage-proof-tests.md) |
| M2-13-04 | [`stories/STORY-M2-13-04-centralized-config-injection-consistency.md`](./EPIC-M2-13-demo-polishing/stories/STORY-M2-13-04-centralized-config-injection-consistency.md) |
| M2-13-05 | [`stories/STORY-M2-13-05-geo-timeout-retry-policy-hardening.md`](./EPIC-M2-13-demo-polishing/stories/STORY-M2-13-05-geo-timeout-retry-policy-hardening.md) |
| M2-13-06 | [`stories/STORY-M2-13-06-ops-alert-metrics-contract.md`](./EPIC-M2-13-demo-polishing/stories/STORY-M2-13-06-ops-alert-metrics-contract.md) |
| M2-13-07 | [`stories/STORY-M2-13-07-privacy-minimization-runtime-enforcement.md`](./EPIC-M2-13-demo-polishing/stories/STORY-M2-13-07-privacy-minimization-runtime-enforcement.md) |
