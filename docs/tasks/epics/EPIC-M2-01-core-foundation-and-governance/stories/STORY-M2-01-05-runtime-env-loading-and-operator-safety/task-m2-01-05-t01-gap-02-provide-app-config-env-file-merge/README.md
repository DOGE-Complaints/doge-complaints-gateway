## Task workspace — `task-m2-01-05-t01-gap-02-provide-app-config-env-file-merge`

- Story: [`../STORY-M2-01-05-runtime-env-loading-and-operator-safety.md`](../STORY-M2-01-05-runtime-env-loading-and-operator-safety.md)
- Decision Ref: [`../../../../../../docs/analysis/gap-analysis-env-loading-target-state-2026-05-12.md`](../../../../../../docs/analysis/gap-analysis-env-loading-target-state-2026-05-12.md) — **§4 GAP-02**, приоритет `os.environ` > `.env`

## Task: implement — merge `.env` при `provide_app_config(env=None)`

### Цель
При запуске `uvicorn` без предварительного `source .env` процесс получает только `os.environ`; `DB_BACKEND` остаётся дефолтом `in_memory`. Подмешивание `.env` из рабочей директории при `env is None` устраняет класс ошибок H1 при сохранении приоритета переменных уже экспортированных в shell.

### Факты из кода
1. [`src/core/infrastructure/providers.py`](../../../../../../src/core/infrastructure/providers.py) — `provide_app_config(env: Mapping[str, str] | None = None)` читает конфиг через `load_config_from_env` из переданного `env` или из `os.environ` без чтения файла.
2. [`tests/simulation_runner.py`](../../../../../../tests/simulation_runner.py) — `_load_env_file` / парсинг строк `KEY=value` (референс для inline-парсера без `python-dotenv`).

### Gap / Проблема
GAP-02 из Decision Ref: нет автозагрузки `.env` на стороне приложения; оператор обязан помнить про `make serve` / ручной `source`.

### AC/DoD
- [ ] (P0) При `provide_app_config(env=None)` и существующем `.env` в cwd: значения из файла попадают в источник для `load_config_from_env`, **если** ключ ещё не задан в `os.environ` (приоритет shell/OS выше).
- [ ] (P0) При явном `provide_app_config(env={...})` (в т.ч. тесты) файл `.env` **не** читается.
- [ ] (P1) Тест(ы) в [`tests/test_config_loading.py`](../../../../../../tests/test_config_loading.py): tmp `.env` с `DB_BACKEND=supabase` + минимально валидный набор; без экспорта в `os.environ` — конфиг подхватывает значение из файла; с `monkeypatch.delenv`/`setenv` — приоритет `os.environ` подтверждён.
- [ ] (P1) Нет циклических импортов `tests` → `core`; при дублировании парсера — общий util в `src/` (например `core.config.env_file`).

### Где менять код
- [`src/core/infrastructure/providers.py`](../../../../../../src/core/infrastructure/providers.py)
- [`tests/test_config_loading.py`](../../../../../../tests/test_config_loading.py)
- при необходимости новый модуль рядом с `schema`/`providers`

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_config_loading.py -q --tb=short
```
