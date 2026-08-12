## Task workspace — `task-m2-16-02-t04-geo-location-query-coverage`

- Story: [`../STORY-M2-16-02-remote-api-simulation-runner.md`](../STORY-M2-16-02-remote-api-simulation-runner.md)
- Requirement: [`remote-api-simulation-gap-2026-05-07.md`](../../../../../analysis/remote-api-simulation-gap-2026-05-07.md)
- Decision Ref: [`remote-api-simulation-gap-2026-05-07.md`](../../../../../analysis/remote-api-simulation-gap-2026-05-07.md)
- Skill declared: `python-pro`

### Scope
Закрыть `GAP-SIM-04`: добавить/нормализовать `location_query` для geo-сценариев simulation canvas.

## Task: data — T04 geo location_query coverage in simulation canvas

### Цель
Сделать geo-сигналы в simulation сценариях корректными, чтобы geo-линза не теряла данные из-за отсутствия `location_query`.

### Факты из кода
1) Gap-матрица фиксирует отсутствие `location_query` для geo-сценариев (`GAP-SIM-04`).
2) Анализ указывает риск: geo-линза будет `unknown` без этого поля.
3) Датасет: `tests/sandbox/dogestonia_simulation_canvas_v0_1.json`.

### Gap / Проблема
Geo-часть simulation датасета неполная для линзы гео-кластеризации.

### AC/DoD
- [x] (P0) Для geo-сценариев в canvas присутствует `location_query` (или подтвержденный эквивалент).
- [x] (P1) Изменения отражены в summary/документации датасета.

### Где менять код
- `tests/sandbox/dogestonia_simulation_canvas_v0_1.json`
- `tests/sandbox/dogestonia_simulation_canvas_v0_1_summary.json`

### План выполнения
1. Выбрать geo-сценарии и добавить `location_query` в согласованную структуру.
2. Обновить summary-метаданные датасета.

### Команды проверки
```bash
cd doge-complaints-gateway && rg -n "location_query" tests/sandbox/dogestonia_simulation_canvas_v0_1.json
```
