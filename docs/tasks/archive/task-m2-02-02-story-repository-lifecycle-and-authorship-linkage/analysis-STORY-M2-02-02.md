# Анализ — STORY-M2-02-02 (Story Repository Lifecycle and Authorship Linkage)

## Проверенные факты

1. В домене отсутствовала модель story lifecycle.
2. Story intake contract уже доступен из STORY-M2-02-01.
3. ServiceFactory не умел собирать story intake use-case.

## Gap

- Нужны:
  - domain contracts (`StoryRecord`, `StoryLifecycleStatus`, `StoryRepository`);
  - in-memory repository;
  - application service для сохранения story с авторством;
  - DI wiring и тесты на lifecycle/authorship linkage.
