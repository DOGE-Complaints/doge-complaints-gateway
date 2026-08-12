## Task workspace — `task-m2-16-02-t03-single-command-launch`

- Story: [`../STORY-M2-16-02-remote-api-simulation-runner.md`](../STORY-M2-16-02-remote-api-simulation-runner.md)
- Requirement: [`remote-api-simulation-gap-2026-05-07.md`](../../../../../analysis/remote-api-simulation-gap-2026-05-07.md)
- Decision Ref: [`remote-api-simulation-gap-2026-05-07.md`](../../../../../analysis/remote-api-simulation-gap-2026-05-07.md)
- Skill declared: `python-pro`

### Scope
Закрыть `GAP-SIM-03`: добавить одношаговый запуск simulation (`make simulate` или эквивалентный shell target).

## Task: implement — T03 one-command simulation launch

### Цель
Снизить операционные ошибки ручного запуска и ускорить smoke/regression прогон.

### Факты из кода
1) Gap-матрица фиксирует отсутствие one-command target (`GAP-SIM-03`).
2) Manual section в анализе описывает `make simulate` как ожидаемый маршрут.
3) Runner CLI уже предполагает фильтры `--max/--groups`, которые target должен прокидывать.

### Gap / Проблема
Нет каноничной одной команды запуска для команды/оператора.

### AC/DoD
- [x] (P0) Добавлен target `simulate` в Makefile (или документированный shell alias).
- [x] (P1) Target запускает `tests/simulation_runner.py` и поддерживает env-driven конфиг.

### Где менять код
- `Makefile` (или equivalent launcher file)

### План выполнения
1. Добавить target `simulate`.
2. Проверить запуск на минимальном сценарии.

### Команды проверки
```bash
cd doge-complaints-gateway && make simulate
```
