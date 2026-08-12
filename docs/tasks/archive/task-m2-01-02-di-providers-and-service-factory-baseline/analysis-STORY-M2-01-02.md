# Анализ — STORY-M2-01-02 (DI Providers and Service Factory Baseline)

## Проверенные факты

1. В `core.api.dependencies` зависимости создавались ad-hoc.
   - Было: прямой `InMemoryHealthRepository()` и `HealthService(...)` в `build_api_dependencies`.
2. Контракт `ServiceFactory` отсутствовал.
3. DI providers как отдельный слой не были выделены.
4. Story требует:
   - контракт factory;
   - providers baseline;
   - wiring в API dependencies;
   - тесты резолва.

## Gap

- Нужен explicit DI bridge:
  - контракт `ServiceFactory` в application;
  - дефолтная factory + providers в infrastructure;
  - API dependencies только через `provide_service_factory()`.
