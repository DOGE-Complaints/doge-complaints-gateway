## Task workspace — `task-m2-16-02-remote-simulation-primary`

- Story: [`../STORY-M2-16-02-remote-api-simulation-runner.md`](../STORY-M2-16-02-remote-api-simulation-runner.md)
- Requirement: [`remote-api-simulation-gap-2026-05-07.md`](../../../../../analysis/remote-api-simulation-gap-2026-05-07.md)
- Decision Ref: [`remote-api-simulation-gap-2026-05-07.md`](../../../../../analysis/remote-api-simulation-gap-2026-05-07.md)
- Skill declared: `python-pro`

### Scope
Оркестрация story-wave: синхронизация task-артефактов, acceptance gates и проверок по GAP-SIM-01..04.

## Task: orchestrate — STORY-M2-16-02 primary gate

### Цель
Обеспечить целостное выполнение и верификацию всей wave без рассинхронизации индекса, story и verification-артефактов.

### Факты из кода
1) `remote-api-simulation-gap-2026-05-07.md` фиксирует GAP-SIM-01..04 и target state.
2) `bullrun-launch-index.md` — канонический источник статусов story/task-wave.
3) `Gateway_builder.plan.md` поддерживает YAML default и safe override run_mode.

### Gap / Проблема
Без story-level orchestration task-wave может закрываться частично и терять traceability по acceptance.

### AC/DoD
- [x] (P0) Все nested task-артефакты созданы и связаны в STORY-M2-16-02.
- [x] (P0) Story acceptance заполняется после task-wave.
- [x] (P1) Индекс и пакет synchronized с новой story-wave.

### Где менять код
- `docs/tasks/epics/EPIC-M2-16-clustering-cron-scheduler/stories/STORY-M2-16-02/*`
- `docs/tasks/bullrun-launch-index.md`
- `.cursor/plans/Gateway_builder.plan.md`

### План выполнения
1. Сформировать story/task-структуру.
2. Обновить builder/index/package files.
3. Закрыть story acceptance и финальный path report.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q --tb=short
```
