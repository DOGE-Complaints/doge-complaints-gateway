# Retrospective — STORY-M2-01-03

## Что сделано
- Введён централизованный `core.config` модуль.
- Зафиксированы profile defaults (`demo/pilot`) и feature flag overrides.
- Добавлены позитивные и негативные тесты загрузки конфигурации.

## Что сработало
- Enum + dataclass подход дал прозрачную схему config governance.
- Негативные тесты покрыли критичные fail-fast сценарии.

## Что улучшить в следующих stories
- Добавить интеграцию `AppConfig` в bootstrap/DI как отдельный provider.
- Ввести `.env.example` нового формата при переходе к runtime endpoint-слоям.
