# CHANGELOG — STORY-M2-01-04

## Added
- `src/core/api/envelope.py` (success/error envelope contract + mapper + trace helper)
- `src/core/api/logging.py` (`log_error` with trace propagation)
- `src/core/api/handlers.py` (boundary handler with unified envelope)
- `tests/test_error_envelope_contract.py`
- `tests/test_trace_propagation.py`

## Changed
- `src/core/api/__init__.py` exports envelope/handler API.

## Validation
- `python3 -m pytest -q` passes.
