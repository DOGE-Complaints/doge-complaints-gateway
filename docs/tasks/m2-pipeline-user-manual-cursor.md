# User Manual: M2 Pipeline в Cursor

## Для чего это
Этот гайд показывает, как в Cursor запускать M2-пайп:
`Epic -> Story -> Execution` с правильной связкой процесса, мышления и skill.

## 1) Быстрый старт (практически)
0. Откройте [`docs/tasks/bullrun-launch-index.md`](./bullrun-launch-index.md) и по правилам **«Оркестрация batch-run»** в [`m2-epic-story-execution-pipeline.md`](./m2-epic-story-execution-pipeline.md) определите стартовый эпик/story (не ведите отдельный «текущий эпик»-файл).
1. Откройте Epic в `docs/tasks/epics/`.
2. Если сторис еще не созданы — запустите декомпозицию:
   - процесс: `@.cursor/commands/bullrun-epic-decompose.md`
   - мышление: `@.cursor/rules/analysis.mdc`
3. Выберите нужную Story и ее task-папку.
4. Запустите выполнение Story:
   - процесс: `@.cursor/commands/bullrun-start.md`
5. Для Python story явно попросите агент заявить и применять:
   - `@.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
6. После каждого этапа принимайте чекпоинт (сделано / осталось / согласование / жду фидбек).
7. Следите за обновлением `docs/tasks/bullrun-launch-index.md`.
8. **Коммиты (обязательно):** методика репозитория — [`docs/methodology/git-commit.md`](../../../docs/methodology/git-commit.md); план на согласование и push — [`docs/methodology/git-commit-prompt.md`](../../../docs/methodology/git-commit-prompt.md). Указывайте агенту явно при закрытии стори / фаз 9–10.

## 2) Что писать агенту (готовые формулы)

### A. Декомпозиция эпика
```text
Выполни декомпозицию эпика процессом @.cursor/commands/bullrun-epic-decompose.md
с мышлением @.cursor/rules/analysis.mdc.
Эпик: @docs/tasks/epics/EPIC-M2-XX-....md
```

### B. Выполнение стори
```text
Выполни стори процессом @.cursor/commands/bullrun-start.md
с мышлением @.cursor/rules/analysis.mdc.
Story: @docs/tasks/epics/.../stories/STORY-M2-XX-YY-....md
Для Python-реализации обязательно заяви skill
@.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md
```

### C. Коммиты после реализации (фазы 9–10 BULLRUN)
```text
Коммиты выполняй по методике @docs/methodology/git-commit.md
(при необходимости план на согласование — @docs/methodology/git-commit-prompt.md).
Task-доки и код группируй отдельными логическими коммитами, без служебного мусора из списка исключений git-commit.md.
```

## 3) Как использовать режимы Cursor

### Plan mode (когда включать)
- Когда нужно согласовать структуру пайпа, решение по архитектуре или список изменений.
- Хорош для этапов: анализ, decision points, архитектура, implementation plan.

### Agent mode (когда включать)
- Когда решения уже приняты и нужно создавать/обновлять файлы, вносить правки, синхронизировать статусы.
- Хорош для этапов: реализация, документация, верификация артефактов.

## 4) Минимальный контроль качества
Перед тем как сказать "идем дальше", проверьте:
1. `BULLRUN-PHASE-LOG.md` обновлен на текущем этапе.
2. Есть артефакт этапа (analysis / decisions / architecture / plan).
3. Для Python story есть явная фиксация `Skill declared: python-pro`.
4. Статус в `bullrun-launch-index.md` синхронизирован.

## 5) Частые ошибки
- Пропускать мышление `analysis.mdc` во время декомпозиции или анализа.
- Запускать Story без `bullrun-start`.
- Не фиксировать skill для Python story.
- Менять статус в story/task и забывать обновить индекс.

## 6) Канонические документы
- Pipeline SSOT: `docs/tasks/m2-epic-story-execution-pipeline.md`
- Этот user manual: `docs/tasks/m2-pipeline-user-manual-cursor.md`
