## Task workspace — `task-m2-09-06-t03-gap-log-03-supabase-request-failed`

- Story: [`../STORY-M2-09-06-runtime-failure-observability-hardening.md`](../STORY-M2-09-06-runtime-failure-observability-hardening.md)
- Requirement: [`req-trace-debug-observability.md`](../../../../../requirements/req-trace-debug-observability.md)
- Decision Ref: [`trace-observability-log-gap-analysis-20260508.md`](../../../../../analysis/trace-observability-log-gap-analysis-20260508.md)
- Skill declared: `python-pro`

### Scope
GAP-LOG-03: unify Supabase persistence error telemetry.

## Task: implement — task-m2-09-06-t03-gap-log-03-supabase-request-failed

### Цель
Добавить унифицированное error-событие `supabase.request_failed` с HTTP-диагностикой для точной локализации инфраструктурных сбоев.

### Факты из кода
1) Сейчас есть request/response debug-события, но нет единого error-контракта.
2) Gap требует поля `path/method/status_code/error_body_preview`.
3) Supabase transport расположен в `db_supabase.py`.

### Gap / Проблема
При сбоях persistence нельзя быстро определить первичную причину на уровне HTTP обращения.

### AC/DoD
- [ ] (P0) Все ошибки Supabase запроса логируются единым событием `supabase.request_failed`.
- [ ] (P1) Событие содержит безопасный preview ответа и контекст `trace_id/story_id`.

### Где менять код
- `src/core/infrastructure/db_supabase.py`
- `src/core/logging_setup.py`

### План выполнения
1. Добавить перехват исключений в transport request.
2. Нормализовать error payload в единый log contract.
3. Проверить negative сценарии транспорта.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q --tb=short
```
