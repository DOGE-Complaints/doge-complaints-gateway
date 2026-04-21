# Architecture Deep Dive (RU)

## 1. Почему текущая архитектура организована через factory + providers

Текущий runtime показывает четкую ставку на composable service graph:

- `build_api_dependencies()` получает готовый `ServiceFactory` через `provide_service_factory()`.
- `DefaultServiceFactory` инкапсулирует wiring application services с инфраструктурными реализациями.

Практический эффект:

1. Доменные сервисы изолированы от transport и внешних деталей.
2. Замена инфраструктуры (например, in-memory на SQL) ограничивается provider/factory зоной.

Источники:

- `src/core/api/dependencies.py`
- `src/core/infrastructure/providers.py`
- `src/core/infrastructure/service_factory.py`

## 2. Контрактная стабильность как базовый архитектурный актив

В нескольких подсистемах контракты заданы явно и проверяются тестами:

- API envelopes: `src/core/api/envelope.py`, `tests/test_error_envelope_contract.py`
- Intake schema versions: `src/core/intake/contracts.py`, `tests/test_story_intake_contract.py`
- Projection contract: `src/core/projection/*`, `tests/test_spa_projection.py`
- Domain records/statuses: `src/core/domain/contracts.py`, `tests/test_story_repository_lifecycle.py`

Это снижает риск «тихого» дрейфа интерфейсов между модулями.

## 3. Реальная цепочка бизнес-обработки и ее ограничения

В runtime присутствуют самостоятельные сервисы для ключевых этапов:

- intake (`StoryIntakeService`)
- profile (`SignalProfileService`)
- clustering (`ClusteringEngine`)
- promotion (`IssuePromotionService`)
- projection (`IssueProjectionService`)
- evidence (`EvidencePackService`)
- geo (`GeoService`)

Однако текущая реализация не содержит единого orchestration use-case, который бы склеивал все этапы в один синхронный pipeline.  
Следовательно, архитектура готова по модульным surface-ам, но не как единый runtime workflow.

Источники:

- `src/core/application/services.py`
- `src/core/cluster/engine.py`
- `src/core/promotion/service.py`
- `src/core/projection/service.py`
- `src/core/evidence/service.py`
- `src/core/geo/service.py`

## 4. Architectural guardrails: что реально защищено тестами

### Защищено

- Domain не должен импортировать application/api/infrastructure.
- Application не должен импортировать api/infrastructure.
- Infrastructure repositories не должны импортировать api/application.

Источник:

- `tests/test_layer_guardrails.py`

### Частично защищено

- Есть smoke на bootstrap и DI resolution (`tests/test_bootstrap_smoke.py`, `tests/test_di_service_factory.py`).
- Нет e2e проверки transport integration, так как transport layer не выделен.

## 5. Точки расширения без ломки контрактов

Наименее рискованные точки эволюции:

1. `src/core/infrastructure/providers.py` — переключение concrete repositories/adapters.
2. `src/core/infrastructure/service_factory.py` — расширение wiring новыми сервисами.
3. `src/core/adapters/registry.py` — замена stub adapters на реальные.
4. `src/core/config/schema.py` — добавление новых env contracts.

## 6. Architectural debt (as-is)

- Нет transport adapter слоя как отдельного runtime entrypoint.
- Нет unified orchestration service, связывающего модули в end-to-end flow.
- Нет persistence-backed infrastructure для production durability.

## 7. Roadmap ориентиры

- Ввести transport boundary модуль (HTTP router + dependency injection adapter).
- Ввести orchestration слой для сквозных use-cases.
- Перенести persistence на SQL-backed adapters с сохранением существующих protocol contracts.
