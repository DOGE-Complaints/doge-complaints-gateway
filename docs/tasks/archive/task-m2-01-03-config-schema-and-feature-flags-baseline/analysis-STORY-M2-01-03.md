# Анализ — STORY-M2-01-03 (Config schema and feature flags baseline)

## Проверенные факты

1. В `src/core` отсутствовал отдельный модуль конфигурации.
2. Профили `demo/pilot` и feature flags не были формализованы в runtime-коде.
3. Тестов на валидацию env-конфигурации не было.
4. Story требует централизованный config, schema validation, профили и flags с тестами.

## Gap

- Нужен единый конфигурационный слой:
  - декларация env schema;
  - строгий парсинг и валидация;
  - profile-based defaults для feature flags;
  - позитивные/негативные тесты загрузки.
