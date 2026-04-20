# Implementation Plan — STORY-M2-02-03

1. Добавить domain contracts для idempotency.
2. Реализовать in-memory idempotency repository.
3. Интегрировать idempotency в `StoryIntakeService`.
4. Обновить DI factory/providers.
5. Добавить unit tests на dedup и non-dedup сценарии.
6. Прогнать полный `pytest`.
