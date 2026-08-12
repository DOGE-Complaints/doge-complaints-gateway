# Анализ — STORY-M2-02-01 (Story Intake Request/Response Contract)

## Проверенные факты

1. В `core` отсутствовал отдельный intake request/response контракт.
2. Требования epic ожидают versioned intake payload и authorship через `submitter`.
3. В API уже есть единый envelope (`SuccessEnvelope` / `ErrorEnvelope`), который можно переиспользовать для response contract.

## Gap

- Нужен отдельный модуль `core.intake`:
  - строгий parsing/validation request;
  - фиксированные версии contract;
  - helper для response shape с `trace_id`.
