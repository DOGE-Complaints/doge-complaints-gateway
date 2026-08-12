## Task workspace — `task-m2-01-05-t02-gap-cluster-primary-active-lenses-alignment`

- Story: [`../STORY-M2-01-05-runtime-env-loading-and-operator-safety.md`](../STORY-M2-01-05-runtime-env-loading-and-operator-safety.md)
- Decision Ref: [`../../../../../../docs/analysis/gap-analysis-env-loading-target-state-2026-05-12.md`](../../../../../../docs/analysis/gap-analysis-env-loading-target-state-2026-05-12.md) — **§7**, контекст H4 (`CLUSTER_PRIMARY_LENS` ∉ `CLUSTER_ACTIVE_LENSES` → `ConfigError`)

## Task: fix — согласованность primary/active lenses в шаблонах и тестах

### Цель
Старт сервера с `.env`, где первичная линза не входит в активный набор, даёт `ConfigError` (см. `schema.py`). Шаблоны и quickstart должны исключить эту ловушку; добавить узкий тест на сообщение/условие ошибки.

### Факты из кода
1. [`src/core/config/schema.py`](../../../../../../src/core/config/schema.py) — валидация `CLUSTER_PRIMARY_LENS` ∈ `CLUSTER_ACTIVE_LENSES` (сообщения около проверки active/primary).
2. [`example.env`](../../../../../../example.env), [`docs/runtime-docs/server-env-quickstart.md`](../../../../../../docs/runtime-docs/server-env-quickstart.md) — операторские шаблоны.

### Gap / Проблема
H4: после загрузки `.env` сервер падает на старте, если primary не включён в active; без синхронизации шаблонов повторяемость высокая.

### AC/DoD
- [ ] (P0) В `example.env` и `server-env-quickstart.md`: явное правило «`CLUSTER_PRIMARY_LENS` должен быть одним из значений в `CLUSTER_ACTIVE_LENSES`»; примеры согласованы.
- [ ] (P1) Тест в [`tests/test_config_loading.py`](../../../../../../tests/test_config_loading.py): `load_config_from_env` / `provide_app_config` с primary ∉ active → `ConfigError` (или ожидаемый тип), при желании assert на фрагмент текста.
- [ ] (P2) При необходимости — подсказка в `Makefile` цели `check-env` / help-текст (если уже есть точка расширения).

### Где менять код / доки
- [`example.env`](../../../../../../example.env)
- [`docs/runtime-docs/server-env-quickstart.md`](../../../../../../docs/runtime-docs/server-env-quickstart.md)
- [`tests/test_config_loading.py`](../../../../../../tests/test_config_loading.py)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_config_loading.py -q --tb=short
```
