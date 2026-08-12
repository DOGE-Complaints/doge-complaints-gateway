## Task workspace — `task-m2-09-06-log-observability-primary`

- Story: [`../STORY-M2-09-06-runtime-failure-observability-hardening.md`](../STORY-M2-09-06-runtime-failure-observability-hardening.md)
- Requirement: [`req-trace-debug-observability.md`](../../../../../requirements/req-trace-debug-observability.md)
- Decision Ref: [`trace-observability-log-gap-analysis-20260508.md`](../../../../../analysis/trace-observability-log-gap-analysis-20260508.md)
- Skill declared: `python-pro`

### Scope
story-level orchestration and acceptance gates for GAP-LOG wave.

## Task: orchestrate — task-m2-09-06-log-observability-primary

### Цель
Реализовать целевое поведение по диагностике runtime падений через структурное логирование на всех критических этапах pipeline.

### Факты из кода
1) Gap-матрица зафиксирована в `trace-observability-log-gap-analysis-20260508.md` (`GAP-LOG-01..05`).
2) EPIC-M2-09 уже используется как активный observability контур в `bullrun-launch-index.md`.
3) Текущий active package (`pkg-000009`) покрывает STORY-M2-09-05, новая wave требует отдельного story-пакета.

### Gap / Проблема
Текущие логи не дают однозначно определить точку падения по одному запуску без воспроизведения.

### AC/DoD
- [x] (P0) Реализован scope таска по requirement.
- [x] (P1) Верификация командами подтверждает ожидаемое поведение.

### Где менять код
- `src/core/api/asgi_app.py`
- `src/core/logging_setup.py`
- `src/core/scheduler/cluster_cron.py`
- `src/core/infrastructure/db_supabase.py`
- `src/core/api/handlers.py`

### План выполнения
1. Имплементировать GAP-LOG-01..05 в целевых слоях.
2. Проверить корреляцию событий по trace_id/story_id.
3. Обновить acceptance артефакты.

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_cluster_cron_job.py tests/test_asgi_lifespan_cron.py tests/test_http_intake_endpoint.py tests/test_supabase_observability.py
```
