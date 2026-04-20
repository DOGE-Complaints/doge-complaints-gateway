## Task: implement — intake idempotency key handling

### Source Story
- `docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-03-intake-idempotency-key-handling.md`

### Цель
Добавить dedup-механику intake-команд по `Idempotency-Key` для безопасных повторов.

### AC/DoD
- [ ] Повторные intake-команды с одним ключом не создают новый story.
- [ ] Ответ повторного вызова предсказуем и стабилен.
- [ ] Конфликтные сценарии задокументированы и покрыты тестами.
