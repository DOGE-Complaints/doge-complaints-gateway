# Acceptance Verification — STORY-M2-01-03

## Критерии приемки
- [x] Конфигурация централизована в одном модуле.  
  Доказательство: `src/core/config/schema.py`, `src/core/config/__init__.py`.
- [x] Введена схема валидации env-переменных.  
  Доказательство: `ENV_SCHEMA`, `ConfigError`, `load_config_from_env()` в `src/core/config/schema.py`.
- [x] Зафиксированы профили `demo` и `pilot`.  
  Доказательство: `DeploymentProfile` в `src/core/config/schema.py`.
- [x] Feature flags подключены и документированы.  
  Доказательство: `FeatureFlags` + profile defaults + overrides в `src/core/config/schema.py`; `solution-architecture-STORY-M2-01-03.md`.
- [x] Тесты config loading проходят.  
  Доказательство: `tests/test_config_loading.py`; прогон `python3 -m pytest -q` (13 passed).

## Проверки
- [x] Прогон тестов/проверок выполнен и зафиксирован.
- [x] Результаты сверены с AC story.
- [x] Отклонения (если есть) описаны и согласованы. (Отклонений нет.)
