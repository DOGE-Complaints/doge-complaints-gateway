# Test Qualification — STORY-M2-01-01

## Набор тестов
- `tests/test_bootstrap_smoke.py`
- `tests/test_layer_guardrails.py`

## Квалификация
- P0 (bootstrap viability): покрыт smoke-тестом.
- P1 (layer dependency rules): покрыт guardrail-тестами.
- P2 (расширенные интеграции): вне scope этой story.

## Результат
- `python3 -m pytest -q` -> `4 passed`.
