# Acceptance Verification — STORY-M2-01-04

## Критерии приемки
- [x] Все API-ошибки возвращаются в едином `ErrorEnvelope`.  
  Доказательство: `src/core/api/envelope.py`, `tests/test_error_envelope_contract.py`.
- [x] `trace_id` присутствует в каждом ответе и логах.  
  Доказательство: `src/core/api/envelope.py`, `src/core/api/logging.py`, `tests/test_trace_propagation.py`.
- [x] Ошибки валидации/доменные/инфраструктурные маппятся предсказуемо.  
  Доказательство: `build_error_envelope()` в `src/core/api/envelope.py`, тесты mapping в `tests/test_error_envelope_contract.py`.
- [x] Contract tests для error shape и trace propagation проходят.  
  Доказательство: `tests/test_error_envelope_contract.py`, `tests/test_trace_propagation.py`, прогон `python3 -m pytest -q` (21 passed).
- [x] Документация API-ошибок актуализирована.  
  Доказательство: `api-error-envelope-reference-STORY-M2-01-04.md`.

## Проверки
- [x] Прогон тестов/проверок выполнен и зафиксирован.
- [x] Результаты сверены с AC story.
- [x] Отклонения (если есть) описаны и согласованы. (Отклонений нет.)
