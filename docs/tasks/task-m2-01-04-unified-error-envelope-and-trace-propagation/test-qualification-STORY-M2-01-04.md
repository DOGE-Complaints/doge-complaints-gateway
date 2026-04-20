# Test Qualification — STORY-M2-01-04

## Набор тестов
- `tests/test_error_envelope_contract.py`
- `tests/test_trace_propagation.py`
- регрессия: весь pytest набор

## Покрытие
- P0: contract shape для success/error payload.
- P1: предсказуемый mapping validation/domain/infrastructure/internal.
- P1: trace propagation в payload и log records.

## Результат
- `python3 -m pytest -q` -> все тесты проходят.
