# Solution Architecture — STORY-M2-01-01

## Цель
Сформировать минимальный исполняемый каркас слоев Module 2, чтобы следующий функционал добавлялся без нарушения архитектурных границ.

## Слои и ответственность
- `core.api`
  - сборка API-зависимостей через `build_api_dependencies()`.
- `core.application`
  - use-case сервис `HealthService`.
- `core.domain`
  - контракты (`HealthRepository`) и доменные DTO (`HealthReport`).
- `core.infrastructure`
  - реализация контракта (`InMemoryHealthRepository`).
- `core.bootstrap`
  - единая точка bootstrap `bootstrap_app()`.

## Правила зависимостей
- `domain` не импортирует `application/api/infrastructure`;
- `application` импортирует только `domain`;
- `infrastructure` импортирует `domain`, но не `application/api`;
- `api` собирает зависимости и может импортировать `application`/`infrastructure`.

## Проверка архитектуры
- smoke: `tests/test_bootstrap_smoke.py`;
- guardrails: `tests/test_layer_guardrails.py`.
