## Task workspace — `task-m2-18-04-t19-gap41-04-config-env-only`

- Story: [`../STORY-M2-18-04-offline-production-paths-req41.md`](../STORY-M2-18-04-offline-production-paths-req41.md)
- Decision Ref: [`../../../../../../requirements/41-testing-production-coverage-target-state.md`](../../../../../../requirements/41-testing-production-coverage-target-state.md) §3 GAP-41-04; PS-18

---
**Приоритет:** P3  
**Сложность:** S  
**Оценка времени:** ~1–2 ч  
**Статус:** Done  
**Wave:** `pkg-000021`  
---

## Task: tests — env-only config loading (Railway injection)

### Цель
`tests/test_config_env_only_contract.py` — CE-01..03: `load_app_config()` / `provide_app_config()` in subprocess without `.env` file.

### Почему это важно (риск)
[`tests/conftest.py`](../../../../../../../tests/conftest.py) `_block_dotenv_leakage` forces in_memory — does not prove Railway env-only bootstrap.

### Факты из кода
1. [`tests/conftest.py`](../../../../../../../tests/conftest.py) — session autouse `DB_BACKEND=in_memory`.
2. [`tests/test_config_loading.py`](../../../../../../../tests/test_config_loading.py) — existing config tests under pytest env (not isolated subprocess).
3. REQ-41 CE-01..03 — subprocess, env dict only.

### Gap / Проблема
**GAP-41-04:** no isolated env-only contract.

### AC/DoD
- [x] (P0) CE-01: full env dict → valid `AppConfig` without `.env`.
- [x] (P0) CE-02: missing required field → `ConfigError`.
- [x] (P0) CE-03: `CLUSTER_CRON_ENABLED=false` read correctly from env.

### Где менять код
- `tests/test_config_env_only_contract.py` (new)

### Out of scope
- Changing [`core/config/schema.py`](../../../../../../../src/core/config/schema.py) defaults without test need.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_config_env_only_contract.py
```
