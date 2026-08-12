## Task workspace — `task-m2-09-05-t06-gap-trace-04-05-06-cluster-geo-issue-trace`

- Story: [`../STORY-M2-09-05-trace-debug-observability-hardening.md`](../STORY-M2-09-05-trace-debug-observability-hardening.md)
- Requirement: [`req-trace-debug-observability.md`](../../../../../requirements/req-trace-debug-observability.md)
- Decision Ref: [`req-trace-debug-observability.md`](../../../../../requirements/req-trace-debug-observability.md)
- Skill declared: `python-pro`

### Scope
GAP-TRACE-04/05/06: tracing in cluster, geo and issue create flows.

## Task: implement — task-m2-09-05-t06-gap-trace-04-05-06-cluster-geo-issue-trace

### Цель
Реализовать целевое поведение по trace/debug observability согласно GAP-матрице requirement-документа.

### Факты из кода
1) GAP-матрица и приоритеты фиксированы в `req-trace-debug-observability.md`.
2) Целевые файлы/слои перечислены в секциях 2.2-2.5 и 8 requirement.
3) Acceptance criteria определены в секции 5 requirement.

### Gap / Проблема
Текущая observability-трассировка неполная и не даёт сквозной диагностики story pipeline в DEBUG.

### AC/DoD
- [ ] (P0) Реализован scope таска по requirement.
- [ ] (P1) Верификация командами подтверждает ожидаемое поведение.

### Где менять код
- `src/core/api/asgi_app.py`
- `src/core/logging_setup.py`
- `src/core/application/services.py`
- `src/core/infrastructure/db_supabase.py`
- `src/core/application/cluster_orchestrator.py`
- `src/core/application/issue_create.py`
- `src/core/geo/service.py`
- `src/core/config/schema.py`

### План выполнения
1. Имплементировать изменения в целевых слоях.
2. Проверить лог-сигналы в DEBUG/INFO.
3. Обновить acceptance артефакт.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q --tb=short
```
