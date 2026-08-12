## Task workspace — `task-m2-09-06-t02-gap-log-02-cron-run-correlation`

- Story: [`../STORY-M2-09-06-runtime-failure-observability-hardening.md`](../STORY-M2-09-06-runtime-failure-observability-hardening.md)
- Requirement: [`req-trace-debug-observability.md`](../../../../../requirements/req-trace-debug-observability.md)
- Decision Ref: [`trace-observability-log-gap-analysis-20260508.md`](../../../../../analysis/trace-observability-log-gap-analysis-20260508.md)
- Skill declared: `python-pro`

### Scope
GAP-LOG-02: cron start/end correlation events with run-level metrics.

## Task: implement — task-m2-09-06-t02-gap-log-02-cron-run-correlation

### Цель
Сделать каждый cron-цикл диагностируемым через пары событий start/end с агрегированными счётчиками и длительностью.

### Факты из кода
1) В логах есть `cluster.cron_run`, но нет агрегированного результата цикла.
2) Gap требует `ready_count/processed_count/created_issue_count/failed_count/duration_ms`.
3) Cron lifecycle управляется через scheduler слой.

### Gap / Проблема
Нельзя точно определить на каком этапе и после какого story остановился batch run.

### AC/DoD
- [ ] (P0) Добавлены `cluster.cron_run_start` и `cluster.cron_run_end` с run-level метриками.
- [ ] (P1) По одному `trace_id`/run id можно восстановить весь cron-цикл.

### Где менять код
- `src/core/scheduler/cluster_cron.py`
- `src/core/application/cluster_orchestrator.py`

### План выполнения
1. Ввести run-идентификатор и метрики цикла.
2. Логировать start/end и итоговые счётчики.
3. Проверить сценарии success/partial/failure.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q --tb=short
```
