# Retrospective — STORY-M2-01-02

## Что сделано
- Введён контракт `ServiceFactory` и дефолтная реализация в infrastructure.
- Добавлены DI providers и переведён API wiring на DI bridge.
- Добавлены/обновлены тесты для factory resolution и запрета ad-hoc инициализации в API dependencies.
- Оформлены process-артефакты (analysis → acceptance + changelog).

## Что сработало
- Чёткое разделение contracts/factory/providers помогло сохранить границы слоев.
- Guardrail на ad-hoc в API dependencies предотвращает регрессии DI дисциплины.

## Что улучшить в следующих stories
- Добавить стандарт именования providers/factories в отдельный архитектурный guideline.
- В story про config заранее предусмотреть провайдеры конфигурации для factory.
