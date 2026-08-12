## Task workspace — `task-m2-09-06-t05-gap-log-05-shutdown-reason`

- Story: [`../STORY-M2-09-06-runtime-failure-observability-hardening.md`](../STORY-M2-09-06-runtime-failure-observability-hardening.md)
- Requirement: [`req-trace-debug-observability.md`](../../../../../requirements/req-trace-debug-observability.md)
- Decision Ref: [`trace-observability-log-gap-analysis-20260508.md`](../../../../../analysis/trace-observability-log-gap-analysis-20260508.md)
- Skill declared: `python-pro`

### Scope
GAP-LOG-05: explicit process shutdown reason telemetry.

## Task: implement — task-m2-09-06-t05-gap-log-05-shutdown-reason

### Цель
Добавить явное событие причины остановки процесса для разделения manual stop и аварийного завершения.

### Факты из кода
1) В логах виден `^C`, но нет структурного события источника shutdown.
2) Gap требует фиксации `SIGINT/SIGTERM/other`.
3) Lifespan boundary находится в `asgi_app`.

### Gap / Проблема
После остановки процесса отсутствует машинно-читаемый shutdown reason для инцидент-разбора.

### AC/DoD
- [ ] (P0) На shutdown публикуется событие с `shutdown_reason`.
- [ ] (P1) Сценарии ручной и системной остановки различимы по логам.

### Где менять код
- `src/core/api/asgi_app.py`
- `src/core/logging_setup.py`

### План выполнения
1. Добавить обработку сигналов с reason mapping.
2. Логировать shutdown reason в lifecycle finalize.
3. Проверить graceful shutdown и signal сценарии.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q --tb=short
```
