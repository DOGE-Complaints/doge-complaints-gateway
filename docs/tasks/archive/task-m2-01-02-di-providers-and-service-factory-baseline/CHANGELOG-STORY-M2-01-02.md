# CHANGELOG — STORY-M2-01-02

## Added
- `src/core/application/factory.py` (`ServiceFactory` contract).
- `src/core/infrastructure/service_factory.py` (`DefaultServiceFactory` implementation).
- `src/core/infrastructure/providers.py` (DI providers).
- `tests/test_di_service_factory.py` (factory resolution test).

## Changed
- `src/core/api/dependencies.py`: wiring через `provide_service_factory()` вместо ad-hoc инстанцирования.
- `src/core/application/__init__.py` и `src/core/infrastructure/__init__.py`: экспорт factory/providers.
- `tests/test_layer_guardrails.py`: проверка, что API dependencies не создаёт сервисы напрямую.

## Validation
- `python3 -m pytest -q` -> `6 passed`.
