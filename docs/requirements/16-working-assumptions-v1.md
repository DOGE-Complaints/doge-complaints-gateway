# 16. Рабочие допущения v1

## Допущения
1. Web2-модуль — центральный story-intelligence слой.
2. Stories в Supabase — долгоживущий продуктовый актив.
3. Distinct issue — производный объект от story corpus.
4. Zero-change SPA — ограничение MVP.
5. Расширенный intake допустим без обязательного PII.
6. Evidence/tokenization prep входит в scope Web2 как подготовка.

## Последствия для планирования
- архитектура должна поддерживать эволюцию без смены core-контракта;
- внутренняя data model богаче публичной витрины;
- roadmap строится вокруг сохранения lineage и explainability.

## Риск-реестр допущений
- если zero-change станет невозможен, нужен controlled contract migration plan;
- если PII станет обязательным для части кейсов, нужен privacy tiering;
- если city-wide clusters войдут в MVP, нужна ранняя оптимизация pipeline.
