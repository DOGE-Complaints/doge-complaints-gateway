# Decision Points — STORY-M2-01-04

## DP-01: Формат envelope
- Решение: `ErrorEnvelope = { error: { code, type, message, details }, trace_id }`.
- Причина: читаемый контракт и явная разделённость error-body и trace.

## DP-02: Базовый mapping ошибок
- `ConfigError` -> `VALIDATION_ERROR` (`validation`)
- `ValueError` -> `DOMAIN_ERROR` (`domain`)
- `ConnectionError` / `TimeoutError` / `OSError` -> `INFRASTRUCTURE_ERROR` (`infrastructure`)
- Остальные -> `INTERNAL_ERROR` (`internal`)

## DP-03: Что считать trace propagation
- Решение: `trace_id` обязателен в success/error payload и в log record (`extra={"trace_id": ...}`).
