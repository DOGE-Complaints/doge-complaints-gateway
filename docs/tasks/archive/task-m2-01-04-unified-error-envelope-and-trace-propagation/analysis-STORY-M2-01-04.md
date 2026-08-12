# Анализ — STORY-M2-01-04 (Unified Error Envelope and Trace Propagation)

## Проверенные факты

1. В текущем `core.api` отсутствовал единый контракт response envelope для ошибок.
2. Trace-id не был стандартизирован на boundary-слое.
3. Предсказуемый mapping типов ошибок не был зафиксирован отдельным контрактом.
4. Story требует:
   - единый `ErrorEnvelope`;
   - `trace_id` в ответах и логах;
   - contract tests на shape и propagation.

## Gap

- Добавить в `core.api` единый envelope + mapper + handler boundary-функцию.
- Покрыть mapping и trace propagation pytest-контрактами.
