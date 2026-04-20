# Solution Architecture — STORY-M2-02-04

## Design

- `core.intake.observability`:
  - `IntakeErrorType` enum;
  - `IntakeErrorInfo` dataclass;
  - `classify_intake_error(error)`;
  - `build_intake_error_payload(error, trace_id)`;
  - `log_intake_error(...)`;
  - `IntakeTelemetry` counters.

## Error Mapping Baseline

- `ValueError` -> `INTAKE_VALIDATION_ERROR`
- `ConnectionError/TimeoutError/OSError` -> `INTAKE_INFRASTRUCTURE_ERROR`
- fallback -> `INTAKE_INTERNAL_ERROR`

## Operational Contract

- Любая intake ошибка должна быть представима payload с `trace_id`.
- Лог должен нести поля для фильтрации и агрегации.
