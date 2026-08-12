# Acceptance Verification — TASK-ISSUE-CREATE-HTTP-01

- [x] Добавлен рабочий HTTP endpoint create issue.
- [x] Endpoint использует application orchestration вместо inline бизнес-логики в роуте.
- [x] Возвращается стабильный contract envelope.
- [x] Ошибки валидации/контракта возвращаются в `ErrorEnvelope`.
- [x] Добавлены и проходят HTTP contract tests.
- [x] PM gate: сценарий создания issue понятен и демонстрируем.
- [x] CTO gate: архитектура сохраняет четкие границы API/application/domain без временных костылей.
