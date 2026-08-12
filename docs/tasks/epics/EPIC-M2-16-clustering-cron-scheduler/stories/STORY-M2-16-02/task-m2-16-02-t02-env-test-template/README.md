## Task workspace — `task-m2-16-02-t02-env-test-template`

- Story: [`../STORY-M2-16-02-remote-api-simulation-runner.md`](../STORY-M2-16-02-remote-api-simulation-runner.md)
- Requirement: [`remote-api-simulation-gap-2026-05-07.md`](../../../../../analysis/remote-api-simulation-gap-2026-05-07.md)
- Decision Ref: [`remote-api-simulation-gap-2026-05-07.md`](../../../../../analysis/remote-api-simulation-gap-2026-05-07.md)
- Skill declared: `python-pro`

### Scope
Закрыть `GAP-SIM-02`: добавить `.env.test.example` и правила безопасного использования test env.

## Task: add — T02 .env.test.example for simulation wave

### Цель
Разделить production `.env` и simulation test-настройки, чтобы исключить случайное смешение runtime/тест-контуров.

### Факты из кода
1) Анализ требует `.env.test.example` и explicit поля `GATEWAY_URL/GATEWAY_API_TOKEN/SIMULATION_CANVAS_PATH`.
2) В анализе явно указано: использовать `.env.test`, а не `.env` для simulation.
3) В gap-матрице `GAP-SIM-02` отмечен как open.

### Gap / Проблема
Нет каноничного тестового env-шаблона для remote simulation запуска.

### AC/DoD
- [x] (P0) `.env.test.example` создан и содержит mandatory simulation vars.
- [x] (P1) В комментариях файла указан workflow copy->.env.test и запрет коммита `.env.test`.

### Где менять код
- `.env.test.example`

### План выполнения
1. Добавить шаблон с переменными и комментариями использования.
2. Проверить, что runner читает этот контракт переменных.

### Команды проверки
```bash
cd doge-complaints-gateway && rg -n "GATEWAY_URL|GATEWAY_API_TOKEN|SIMULATION_CANVAS_PATH" .env.test.example
```
