# CHANGELOG — STORY-M2-01-03

## Added
- `src/core/config/schema.py`:
  - `ENV_SCHEMA`
  - `DeploymentProfile`
  - `FeatureFlags`
  - `AppConfig`
  - `load_config_from_env()`
  - `ConfigError`
- `src/core/config/__init__.py`
- `tests/test_config_loading.py`

## Validation
- `python3 -m pytest -q` -> `13 passed`.
