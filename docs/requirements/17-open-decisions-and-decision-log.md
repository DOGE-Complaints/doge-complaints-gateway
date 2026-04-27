# 17. Открытые решения и decision log

## Критичные открытые решения
1. Какие cluster views обязательны в MVP, а какие позже.
2. Institution: mandatory или suggested.
3. Порог между analytics cluster и issue-ready cluster.
4. Нужна ли отдельная витрина cluster cards до official issue board.
5. Какие intake-поля обязательны для evidence pack.
6. Входит ли city-wide clustering в MVP.
7. Нужен ли новый projection type для `improvement_case`.

## Формат принятия решений (ADR-lite)
- **Context**
- **Decision**
- **Alternatives**
- **Trade-offs**
- **Impact on SPA/Operations**
- **Rollback path**

## Приоритизация решений
- **P0 до начала полной реализации:** #1, #3, #5.
- **P1 до выхода MVP:** #2, #6.
- **P2 post-MVP:** #4, #7.

## Governance cadence
- еженедельный architecture/product review;
- decision freeze перед каждым релиз-кандидатом;
- пересмотр спорных решений по данным метрик и обратной связи.

## Post-demo decision backlog (не блокирует demo)

- **Оркестрация и cron:** зафиксировать выбор паттерна job runner и инфраструктуры планировщика после стабилизации use-case — см. `20-post-demo-orchestration-and-scheduled-jobs.md`, архитектура `solution architecture/16-automation-orchestration-and-scheduled-jobs.md`, эпик EPIC-M2-11.
- **Токенизация на уровне story и уведомления авторам:** продуктовые и юридические границы, сроки — **не зафиксированы**; см. `21-post-demo-story-tokenization-and-contributor-notifications.md`, эпик EPIC-M2-12.

## Зафиксированные решения (ADR-lite, после интервью)

| Дата | Тема | Документ |
|------|------|----------|
| 2026-04-26 | Demo M2: story intake контракт, обязательность `language`/`title_hint`, deprecated `POST /issues`, async extraction, расширение полей под GPT canonical type/labels | `22-m2-demo-story-intake-interview-ssot-v1.md` (источник: `docs/tasks/task-domain-story-contract-interview-01/interview-report-domain-story-contract-01.md`) |
| 2026-04-26 | Demo M2: критерии кластеризации (MIN_CLUSTER_SIZE, env-driven линзы/пороги), primary GPT type/labels vs keyword-derivation, N:M story–issue, title из доминантного `title_hint`, контракт cluster output | `23-m2-demo-story-clustering-interview-ssot-v1.md` (источник: `docs/tasks/task-cluster-criteria-interview-01/interview-report-cluster-criteria-01.md`) |
