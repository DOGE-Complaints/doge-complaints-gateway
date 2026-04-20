# Module 2 Requirements Pack (Product + CTO)

Этот каталог содержит детализированную декомпозицию PDF `DOGEstonia — Module 2 Canvas: Web2 Core / Story Intelligence Layer`.

Дополнительно добавлены контрактные спецификации, выходящие за рамки нумерации PDF (например inbound API для GPT).

Каждый файл, привязанный к PDF, соответствует отдельному пункту исходного документа (разделы 1-18) и включает:
- продуктовую цель и ценность;
- операционную и техническую модель реализации;
- NFR/риски/метрики;
- решения и открытые вопросы.

## Файлы

- `01-module-mission.md`
- `02-business-problem-and-target-outcome.md`
- `03-scope-and-boundaries.md`
- `04-business-entities-model.md`
- `05-module-philosophy-and-principles.md`
- `06-lifecycle-business-logic.md`
- `07-dynamic-clusters-product-model.md`
- `08-distinct-issue-product-logic.md`
- `09-spa-issue-projection.md`
- `10-functional-requirements-system-spec.md`
- `11-working-content-model.md`
- `12-delivery-specs-package.md`
- `13-anti-patterns-and-prevention.md`
- `14-quality-criteria-framework.md`
- `15-acceptance-criteria-operationalization.md`
- `16-working-assumptions-v1.md`
- `17-open-decisions-and-decision-log.md`
- `18-module-formula-and-strategy.md`

### Контракты интеграции (GPT / API)

- `19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md` — inbound JSON для Story Intake, препроцессинг GPT, «живая» история, черновик SPA-issue (i18n), задел gov-interop.

### Post-demo (вне обязательного MVP, сроки не зафиксированы)

- `20-post-demo-orchestration-and-scheduled-jobs.md` — оркестрация, cron/queue, единый use-case слой.
- `21-post-demo-story-tokenization-and-contributor-notifications.md` — токенизация на уровне историй и уведомления авторам; **дисклеймер post-demo**.
