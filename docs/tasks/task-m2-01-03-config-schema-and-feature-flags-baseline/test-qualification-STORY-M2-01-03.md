# Test Qualification — STORY-M2-01-03

## Набор тестов
- `tests/test_config_loading.py`
- регрессия baseline: весь `pytest` набор

## Покрытие
- P0: валидный config loading для `demo/pilot`.
- P1: корректная обработка invalid profile/timeout и missing required env.
- P1: override feature flags.

## Результат
- `python3 -m pytest -q` -> `13 passed`.
