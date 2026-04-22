# Run Reports

Директория хранит агрегированные отчеты запусков pipeline.

## Формат файла

- `run-summary-YYYYMMDD-HHMM.md`

## Когда создавать

- Один файл на один запуск `EPIC_BATCH` / `STORY_BATCH` / `TASK_BATCH`.

## Минимальная структура отчета

1. `Run metadata` (timestamp, mode: explicit/fallback, `ACTIVE_TASK_PATH` при наличии).
2. `Process coverage` (этапы run-task, включая тестовую фазу).
3. `Executed items` (epics/stories/tasks).
4. `Acceptance summary`.
5. `Commit summary`.
6. `Open follow-ups`.

## Синхронизация с индексом

После создания нового `run-summary-*` обязательно добавить запись в:
- `docs/tasks/bullrun-launch-index.md` -> секция `Run Reports Registry`.
