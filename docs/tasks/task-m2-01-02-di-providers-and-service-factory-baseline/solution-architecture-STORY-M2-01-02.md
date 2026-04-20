# Solution Architecture — STORY-M2-01-02

## Цель
Сделать единый путь получения сервисов: `API -> providers -> service factory -> application services`.

## Контур
- `core.application.factory.ServiceFactory` (Protocol):
  - контракт factory-резолва сервисов.
- `core.infrastructure.service_factory.DefaultServiceFactory`:
  - дефолтная реализация контракта.
- `core.infrastructure.providers`:
  - `provide_health_repository()`;
  - `provide_service_factory()`.
- `core.api.dependencies.build_api_dependencies()`:
  - использует только `provide_service_factory()`;
  - не инстанцирует сервисы напрямую.

## Проверка
- unit: `tests/test_di_service_factory.py`;
- guardrails: `tests/test_layer_guardrails.py`.
