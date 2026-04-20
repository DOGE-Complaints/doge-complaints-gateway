# Solution Architecture — STORY-M2-01-04

## Компоненты
- `core.api.envelope`:
  - `ErrorBody`, `ErrorEnvelope`, `SuccessEnvelope`
  - `ensure_trace_id()`
  - `build_error_envelope()`, `build_success_envelope()`
- `core.api.logging`:
  - `log_error()` с записью `trace_id` в лог.
- `core.api.handlers`:
  - `handle_health()` как boundary-обработчик с unified envelope.

## Контракт
- Success: `{ "data": {...}, "trace_id": "<id>" }`
- Error: `{ "error": { "code": "...", "type": "...", "message": "...", "details": {...} }, "trace_id": "<id>" }`

## Верификация
- `tests/test_error_envelope_contract.py` — shape и error mapping.
- `tests/test_trace_propagation.py` — trace id в success/error и в логах.
