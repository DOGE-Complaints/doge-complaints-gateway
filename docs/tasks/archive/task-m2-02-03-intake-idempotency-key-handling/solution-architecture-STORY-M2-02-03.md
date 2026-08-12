# Solution Architecture — STORY-M2-02-03

## Design

- Domain:
  - `IdempotencyRecord`;
  - `IdempotencyRepository` protocol.
- Infrastructure:
  - `InMemoryIdempotencyRepository`.
- Application:
  - `StoryIntakeService.create_story(..., idempotency_key=...)`:
    - ищет ключ в idempotency repository;
    - при совпадении возвращает существующий story;
    - при отсутствии создает story и сохраняет key->story mapping.

## Integrity Rules

- Одинаковый `Idempotency-Key` -> один и тот же `story_id`.
- Разные ключи -> независимые story.
