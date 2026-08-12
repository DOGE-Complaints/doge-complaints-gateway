## Task workspace — `task-m2-09-06-t01-gap-log-01-global-exception-trace`

- Story: [`../STORY-M2-09-06-runtime-failure-observability-hardening.md`](../STORY-M2-09-06-runtime-failure-observability-hardening.md)
- Requirement: [`req-trace-debug-observability.md`](../../../../../requirements/req-trace-debug-observability.md)
- Decision Ref: [`trace-observability-log-gap-analysis-20260508.md`](../../../../../analysis/trace-observability-log-gap-analysis-20260508.md)
- Skill declared: `python-pro`

### Scope
GAP-LOG-01: structured global exception telemetry for runtime failures.

## Task: implement — task-m2-09-06-t01-gap-log-01-global-exception-trace

### Цель
Добавить централизованное логирование исключений верхнего уровня с обязательной корреляцией `trace_id/story_id/stage`.

### Факты из кода
1) GAP-LOG-01 требует `exception` событие с `stack` и корреляцией.
2) Текущие логи содержат успешные INFO события, но не дают унифицированный stack trace.
3) Runtime boundary проходит через `asgi_app`/handlers.

### Gap / Проблема
При runtime сбое невозможно однозначно локализовать место падения по одному событию.

### AC/DoD
- [ ] (P0) Добавлено глобальное exception-событие с `exc_info` и обязательными полями контекста.
- [ ] (P1) Ошибки API/cron/infra коррелируются по `trace_id`.

### Где менять код
- `src/core/api/asgi_app.py`
- `src/core/api/handlers.py`
- `src/core/logging_setup.py`

### План выполнения
1. Ввести централизованный логгер исключений.
2. Добавить обязательные поля `stage/exception_type/message/stack`.
3. Проверить на unit/runtime сценариях.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q --tb=short
```
