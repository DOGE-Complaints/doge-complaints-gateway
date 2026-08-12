## Task workspace — `task-m2-16-02-t01-simulation-runner`

- Story: [`../STORY-M2-16-02-remote-api-simulation-runner.md`](../STORY-M2-16-02-remote-api-simulation-runner.md)
- Requirement: [`remote-api-simulation-gap-2026-05-07.md`](../../../../../analysis/remote-api-simulation-gap-2026-05-07.md)
- Decision Ref: [`remote-api-simulation-gap-2026-05-07.md`](../../../../../analysis/remote-api-simulation-gap-2026-05-07.md)
- Skill declared: `python-pro`

### Scope
Закрыть `GAP-SIM-01`: добавить `tests/simulation_runner.py` по спецификации из gap-документа.

## Task: implement — T01 simulation runner for remote API intake

### Цель
Сделать воспроизводимый remote smoke/regression запуск simulation canvas через реальный `POST /intake/stories` против `GATEWAY_URL`.

### Факты из кода
1) В анализе указан отсутствующий файл `tests/simulation_runner.py` (`GAP-SIM-01`).
2) Там же зафиксирован required mapping canvas -> intake payload.
3) Документ определяет mandatory output: per-scenario result + summary + exit-code policy.

### Gap / Проблема
Нет инструмента массового remote intake-прогона по готовому canvas.

### AC/DoD
- [x] (P0) `tests/simulation_runner.py` существует и читает `.env.test`.
- [x] (P0) Скрипт отправляет `POST /intake/stories` на `GATEWAY_URL` с `x-api-token`.
- [x] (P1) Поддержаны `--max` и `--groups`.
- [x] (P1) Summary + exit code policy соответствуют spec.

### Где менять код
- `tests/simulation_runner.py`

### План выполнения
1. Реализовать env/config loading и JSON loading для canvas.
2. Реализовать mapping + http dispatch + report.
3. Добавить fail/success exit codes и базовую валидацию аргументов.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 tests/simulation_runner.py --max 1
```
