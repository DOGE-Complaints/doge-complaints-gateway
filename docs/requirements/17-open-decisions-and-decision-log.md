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
