# Retrospective — STORY-M2-01-01

## Что сделано
- Сформирован минимальный Python bootstrap каркас в `src/core` по слоям API/Application/Domain/Infrastructure.
- Добавлены smoke и guardrails-тесты для проверки bootstrapping и базовых архитектурных ограничений.
- Оформлены все task-артефакты (analysis, decisions, architecture, plan, qualification, acceptance, changelog).

## Что сработало
- `src/` layout упрощает модульные импорты и тестовую настройку.
- Guardrails-тесты быстро выявляют архитектурный дрейф.

## Что улучшить в следующих stories
- Добавить более формализованный архитектурный линтер слоев (например import-lint) после стабилизации baseline.
- Раньше фиксировать нейминг пакета, чтобы избегать промежуточного переименования.
