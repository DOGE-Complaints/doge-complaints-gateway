# Solution Architecture — STORY-M2-01-03

## Централизованный модуль
- `core.config.schema`:
  - `ENV_SCHEMA` (декларация required/optional env);
  - `DeploymentProfile` (`demo`/`pilot`);
  - `FeatureFlags`, `AppConfig`;
  - `load_config_from_env()` + `ConfigError`.

## Правила
- Required env: `API_BASE_URL`.
- Optional env с defaults: `APP_PROFILE`, `REQUEST_TIMEOUT_S`, feature flag overrides.
- Profile defaults:
  - `demo`: все пилотные фичи выключены;
  - `pilot`: пилотные фичи включены.

## Проверка
- `tests/test_config_loading.py`:
  - позитивные сценарии demo/pilot;
  - override флагов;
  - негативные сценарии (missing required env, invalid profile/timeout).
