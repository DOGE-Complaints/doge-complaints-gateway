## Task workspace — `task-m2-09-06-t04-gap-log-04-story-pipeline-outcome`

- Story: [`../STORY-M2-09-06-runtime-failure-observability-hardening.md`](../STORY-M2-09-06-runtime-failure-observability-hardening.md)
- Requirement: [`req-trace-debug-observability.md`](../../../../../requirements/req-trace-debug-observability.md)
- Decision Ref: [`trace-observability-log-gap-analysis-20260508.md`](../../../../../analysis/trace-observability-log-gap-analysis-20260508.md)
- Skill declared: `python-pro`

### Scope
GAP-LOG-04: final per-story pipeline outcome event.

## Task: implement — task-m2-09-06-t04-gap-log-04-story-pipeline-outcome

### Цель
Ввести единое outcome-событие по каждой story для диагностики финального состояния pipeline.

### Факты из кода
1) В логах есть `story_intake_created`, но нет финального сводного состояния pipeline.
2) Gap требует поля `story_id/trace_id/lifecycle_status/cluster_outcome/error_code`.
3) Intake/cluster переходы проходят через API handler и orchestrator.

### Gap / Проблема
По текущим логам нельзя быстро ответить, чем закончился полный pipeline конкретной story.

### AC/DoD
- [ ] (P0) Добавлено событие `story.pipeline_outcome` для success/deferred/error.
- [ ] (P1) Событие стабильно содержит жизненный статус и код ошибки (если есть).

### Где менять код
- `src/core/api/handlers.py`
- `src/core/application/cluster_orchestrator.py`

### План выполнения
1. Добавить final outcome точку в intake/pipeline path.
2. Нормализовать outcome enum и error mapping.
3. Проверить сценарии success/deferred/error.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q --tb=short
```
