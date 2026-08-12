# Solution Architecture — STORY-M2-02-02

## Design

- Domain:
  - `StoryLifecycleStatus` (`accepted`, `partial_ready`, `ready_for_profile`);
  - `StoryRecord` dataclass;
  - `StoryRepository` protocol.
- Infrastructure:
  - `InMemoryStoryRepository` with dictionary storage.
- Application:
  - `StoryIntakeService.create_story(request)`:
    - генерирует `story_id`;
    - сохраняет immutable narrative;
    - переносит authorship linkage;
    - устанавливает lifecycle status `accepted`.

## DI Wiring

- `DefaultServiceFactory` расширен `story_repository`.
- Добавлен `get_story_intake_service`.
- Providers расширены `provide_story_repository`.
