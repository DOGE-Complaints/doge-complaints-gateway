# Implementation Plan — STORY-M2-01-02

## Phase 1 — Контракт и реализации factory
- Добавить `ServiceFactory` Protocol.
- Добавить `DefaultServiceFactory`.

## Phase 2 — Providers и wiring
- Добавить `infrastructure/providers.py`.
- Перевести `api/dependencies.py` на `provide_service_factory()`.

## Phase 3 — Тесты и verification
- Добавить unit тест factory.
- Расширить guardrails-тест для проверки отсутствия ad-hoc в API dependencies.
- Прогнать `pytest`.
