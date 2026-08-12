# Changelog — STORY-M2-02-03

## Added
- `IdempotencyRecord` and `IdempotencyRepository` in domain contracts.
- `InMemoryIdempotencyRepository`.
- `tests/test_story_intake_idempotency.py`.

## Updated
- `StoryIntakeService` поддерживает `idempotency_key`.
- DI providers/factory расширены idempotency dependency.
- Existing service/repository tests адаптированы.
