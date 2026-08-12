# Acceptance Verification — STORY-M2-01-02

## Критерии приемки
- [x] Описан контракт `ServiceFactory`.  
  Доказательство: `src/core/application/factory.py`.
- [x] Реализованы DI providers для baseline-сервисов.  
  Доказательство: `src/core/infrastructure/providers.py`, `src/core/infrastructure/service_factory.py`.
- [x] API-слой использует DI-bridge вместо ad-hoc инициализации.  
  Доказательство: `src/core/api/dependencies.py` использует `provide_service_factory()`.
- [x] Добавлены unit/integration тесты DI graph.  
  Доказательство: `tests/test_di_service_factory.py`, `tests/test_layer_guardrails.py`.

## Проверки
- [x] Прогон тестов/проверок выполнен и зафиксирован.
- [x] Результаты сверены с AC story.
- [x] Отклонения (если есть) описаны и согласованы. (Отклонений нет.)
