# Анализ — STORY-M2-02-03 (Intake Idempotency Key Handling)

## Проверенные факты

1. Story creation уже реализована через `StoryIntakeService`.
2. Повторные intake вызовы с одинаковым payload пока создавали новый `story_id`.
3. Для безопасной интеграции GPT/API нужна предсказуемая dedup стратегия.

## Gap

- Нужен idempotency storage + использование `Idempotency-Key` в use-case.
