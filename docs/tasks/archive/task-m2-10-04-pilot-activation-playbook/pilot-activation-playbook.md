# Pilot activation playbook — adapter layer (EPIC-M2-10)

Операционный чеклист для перехода окружения на **pilot** с сохранением тех же интерфейсов, что и в demo. Реальный blockchain broadcast и production wallet transport **вне scope** этого документа до готовности отдельных интеграций.

## 1. Предусловия

- Завершены эпики **M2-01** (конфиг/DI), **M2-07** (evidence/lineage по продуктовому контуру), **M2-09** (безопасность, health, метрики).
- Есть согласованный план секретов (tokens, keys) вне репозитория.

## 2. Конфигурация профиля

1. Установить `APP_PROFILE=pilot` (или эквивалент в вашем deployment manifest).
2. Задать валидный `API_BASE_URL` с схемой `http` или `https` (см. `load_config_from_env` / `ENV_SCHEMA`).
3. При необходимости переопределить feature flags через env: `FF_WALLET_ADAPTER`, `FF_BLOCKCHAIN_ADAPTER`, `FF_TOKENIZATION_PIPELINE` (см. `core.config.schema`). Если переменные не заданы, **профиль pilot** использует значения по умолчанию: `wallet_adapter=true`, `blockchain_adapter=true`, `tokenization_pipeline=true`.

## 3. Наблюдаемость режима

- Вызвать `adapter_runtime_flags(config)` (или залогировать его результат при старте) и убедиться, что `deployment_profile` — `pilot`, а флаги соответствуют ожиданию ops.

## 4. Замена stub-адаптеров на реальные реализации

Текущая сборка: `build_adapter_bundle` в `src/core/adapters/registry.py` подставляет `Demo*` классы и для demo, и для pilot. Для настоящего pilot:

1. Реализовать классы, удовлетворяющие `WalletPushAdapter`, `SignRequestAdapter`, `TxBroadcastAdapter` в `src/core/adapters/` (или в инфраструктурном слое с thin wrapper).
2. В `build_adapter_bundle` ветвить по `config.profile` и/или feature flags и возвращать production-адаптеры вместо `Demo*`.
3. Не менять сигнатуры протоколов без ADR и версионирования API.

## 5. Проверки перед выкладкой

- Прогнать тесты: `python3 -m pytest` (включая `tests/test_adapters_demo_pilot.py`).
- Smoke: health/readiness (M2-09), защищённые маршруты с `SERVICE_API_TOKEN` при необходимости.
- Убедиться, что логи содержат `trace_id` для цепочки запросов.

## 6. Откат

- Вернуть `APP_PROFILE=demo` и прежние значения feature flags.
- Откатить deployment до сборки с stub-адаптерами, если реальные адаптеры вызывают инцидент.

## 7. Связанные артефакты

- Код: `src/core/adapters/` (`protocols.py`, `types.py`, `demo.py`, `registry.py`, `__init__.py`).
- Продуктовая токенизация story и уведомления авторов — **EPIC-M2-12**, не блокирует выполнение этого чеклиста.
