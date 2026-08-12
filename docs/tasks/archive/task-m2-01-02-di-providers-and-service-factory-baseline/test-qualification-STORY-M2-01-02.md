# Test Qualification — STORY-M2-01-02

## Тесты
- `tests/test_di_service_factory.py`
- `tests/test_layer_guardrails.py`
- `tests/test_bootstrap_smoke.py` (регрессия bootstrap после DI refactor)

## Покрытие критериев
- P0: factory возвращает рабочий `HealthService`.
- P1: API dependencies не содержит ad-hoc инстанцирования сервисов.
- P1: общий bootstrap не деградировал.

## Результат
- `python3 -m pytest -q` -> `6 passed`.
