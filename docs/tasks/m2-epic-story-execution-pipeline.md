# M2 Pipeline: Epic -> Story -> Execution

## Назначение
Канонический процесс (SSOT) для запуска и ведения работ в Module 2 в зоне `doge-complaints-gateway/docs/tasks/`.

## Оркестрация batch-run (перед каждым запуском)
Источник истины по **текущей точке работ** — только [`docs/tasks/bullrun-launch-index.md`](./bullrun-launch-index.md), отдельный файл «текущий эпик» не ведётся.

1. Открыть индекс и найти **первый эпик**, в котором есть story не в статусе **Done (Committed)** (по строкам таблицы: ⚪ 🟡 🔵 или иной незакрытый статус в колонке Status).
2. Если **секции эпика нет** в индексе — эпик считается **не декомпозированным**: сначала процесс `bullrun-epic-decompose` (папка `stories/`, task-папки `task-m2-xx-yy-*`), затем исполнение story.
3. Если эпик в индексе есть, но развёрнут только как **одна строка epic | Draft** без строк по story — трактовать как **не декомпозированный** и выполнить декомпозицию (п. 2).
4. Если все stories текущего эпика 🟢 **Done (Committed)** — переходить к **следующему** эпику **сверху вниз** в файле индекса.

## Контракт ролей (обязательный)
- **Process (Epic decomposition):** `@.cursor/commands/bullrun-epic-decompose.md`
- **Thinking (always-on analysis):** `@.cursor/rules/analysis.mdc`  
  (допустимый вход через `@.cursor/commands/run-analysis.md`)
- **Process (Story execution):** `@.cursor/commands/bullrun-start.md`
- **Skill (Python story):** `@.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Git (коммиты по закрытию фаз / task-артефактов):** [`docs/methodology/git-commit.md`](../../../docs/methodology/git-commit.md) — группировка изменений, фильтрация файлов, формат сообщений (англ.). Полный цикл с **планом коммита на согласование с оператором** и ограничениями по push: [`docs/methodology/git-commit-prompt.md`](../../../docs/methodology/git-commit-prompt.md). На фазах 9–10 BULLRUN и при синхронизации `bullrun-launch-index.md` агент обязан следовать этой методике, а не ad-hoc коммитам.

## Уровни процесса

### 1) Epic
1. По правилам раздела **«Оркестрация batch-run»** определить стартовый эпик и необходимость декомпозиции.
2. Выбрать `EPIC-M2-*` со статусом `Draft` или `In Progress` (или не декомпозированный по индексу).
3. Запустить декомпозицию через `bullrun-epic-decompose` с мышлением `analysis.mdc`, если story ещё нет в индексе.
4. Результат декомпозиции:
   - `stories/STORY-M2-XX-YY-*.md`;
   - task-папка на каждую сторис: `docs/tasks/task-m2-xx-yy-*/`;
   - синхронизация строк в `bullrun-launch-index.md` в той же итерации.

### 2) Story
1. Взять конкретную `STORY-M2-*`.
2. Выполнять через `bullrun-start` (пошаговый процесс, фазовый лог, AC-верификация).
3. Для Python story обязательно заявить skill `python-pro` в артефактах.

### 3) Execution
1. Вести `BULLRUN-PHASE-LOG.md` по этапам.
2. На паузах выдавать чекпоинт: сделано / осталось / согласование / жду фидбек.
3. Перед закрытием обязательно заполнить `acceptance-verification-*.md`.
4. **Коммиты:** перед `git commit` / `git push` — [`git-commit.md`](../../../docs/methodology/git-commit.md); при необходимости согласования с оператором — [`git-commit-prompt.md`](../../../docs/methodology/git-commit-prompt.md). Документация по таску (README task, BULLRUN-лог, acceptance, test-qualification) коммитится в том же духе: отдельные логические коммиты, без мусорных путей из раздела «что НЕ коммитить» в `git-commit.md`.

## Минимальный контракт артефактов

### Для Story файла
- `Key`, `Parent Epic`, `Status`, `AC / DoD`, `Task Artifacts`.
- `Task Artifacts` должны ссылаться на:
  - `README.md`,
  - `BULLRUN-PHASE-LOG.md`,
  - `acceptance-verification-*.md`.

### Для task-папки
- Обязательно:
  - `README.md`
  - `task-*.md`
  - `BULLRUN-PHASE-LOG.md`
  - `acceptance-verification-*.md`
- По этапам добавляются:
  - `analysis-*.md`
  - `decision-points-*.md`
  - `solution-architecture-*.md`
  - `implementation-plan-*.md`

## Статусы и синхронизация
- Story: `Todo -> In Progress -> Implemented (Waiting Acceptance/Commits) -> Done (Committed)`.
- Любая смена статуса Story отражается в `docs/tasks/bullrun-launch-index.md` в той же итерации.

## Быстрый runtime-чеклист
1. **Индекс:** открыт `bullrun-launch-index.md`, стартовый эпик/story определены по разделу «Оркестрация batch-run».
2. Epic/Story выбраны и статус корректный.
3. Декомпозиция (если нужна) выполнена через `bullrun-epic-decompose + analysis.mdc`.
4. Task-папка существует и содержит обязательные файлы.
5. Story запущена через `bullrun-start`.
6. Для Python story: отмечено `Skill declared: python-pro`.
7. Фазы и AC-верификация обновляются по ходу процесса; после каждой story — строка в `bullrun-launch-index.md` в той же итерации.
