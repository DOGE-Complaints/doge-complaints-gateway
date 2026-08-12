# Gateway Story Builder

Проект: `doge-complaints-gateway`  
Рабочая зона: `/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/tasks/`  
Источник процесса: `docs/tasks/m2-epic-story-execution-pipeline.md` (этот файл)

## Назначение
Канонический SSOT-процесс для запуска и ведения работ Module 2 в проекте `doge-complaints-gateway`.

## Backlog SSOT layers

| Слой | Путь |
|------|------|
| Backlog stories | `docs/tasks/backlog-stories/STORY-GW-*.md` + [`backlog-stories/INDEX.md`](./backlog-stories/INDEX.md) |
| Очередь исполнения | immutable `gateway-active-packages/pkg-*.yaml` |
| Launch index | [`bullrun-launch-index.md`](./bullrun-launch-index.md) |
| Progress snapshot | [`gateway-backlog-dashboard.md`](./gateway-backlog-dashboard.md) |

### Sync after story close

В той же итерации, что и story gate / P6 audit:

1. Story file `Status` / AC
2. Package [`backlog-stories/*/INDEX.md`](./backlog-stories/)
3. Root [`backlog-stories/INDEX.md`](./backlog-stories/INDEX.md)
4. [`bullrun-launch-index.md`](./bullrun-launch-index.md) registry + §Актуальная точка при смене волны
5. [`gateway-backlog-dashboard.md`](./gateway-backlog-dashboard.md) — recount from package indexes ([maintenance guide](../../../docs/methodology/Zeya888-builder-queue/workflow/backlog-dashboard-maintenance.md))

**SSOT order при конфликтах:** pipeline gate → package INDEX → root INDEX → bullrun → dashboard (derived).

## Input Source
Этот блок обязателен перед любым запуском и определяет входной источник выполнения.

Пример:
`ACTIVE_TASK_PATH=doge-complaints-gateway/docs/tasks/task-implement-full-bearer-api-enforcement/task-implement-full-bearer-api-enforcement.md`

### Поле запуска
- `ACTIVE_TASK_PATH` — абсолютный или workspace-путь до активного task/story/epic артефакта.

### Режим A: explicit input
Если `ACTIVE_TASK_PATH` задан:
1. Проверить, что путь существует.
2. Проверить, что путь относится к проекту `doge-complaints-gateway` и лежит в зоне `.../doge-complaints-gateway/docs/tasks/`.
3. Запускать выполнение строго от этого пути.

### Режим B: fallback от индекса
Если `ACTIVE_TASK_PATH` не задан:
1. Взять индекс: [`bullrun-launch-index.md`](./bullrun-launch-index.md).
2. Найти следующую сущность со статусом `⚪`.
3. Приоритет выбора:
   - сначала `Story` в активном эпике `In Progress`/`Draft`;
   - затем `Cross-Epic Task Backlog`;
   - затем первый следующий `EPIC` в статусе `Draft`.
4. Выполнять найденную сущность по этому же универсальному процессу.

### Однозначный алгоритм резолва
1. `input path -> validate exists -> execute`
2. иначе `index scan -> first ⚪ -> execute`

## Оркестрация batch-run (перед каждым запуском)
Источник истины по текущей точке работ — только [`docs/tasks/bullrun-launch-index.md`](./bullrun-launch-index.md), отдельный файл «текущий эпик» не ведётся.

Контракт gateway (process-reminder todos): [`gateway-operator-contract.md`](../../../docs/methodology/Zeya888-builder-queue/contracts/gateway-operator-contract.md) — `resolve-start-epic-from-index`, `treat-missing-epic-as-not-decomposed`, `sync-index-after-each-story`.

1. Если эпик не присутствует в индексе — считать его не декомпозированным → `bullrun-epic-decompose`, не P3 Execute.
2. Если эпик присутствует, но в нем есть story не в `Done (Committed)` — продолжать с этого эпика.
3. Если текущий эпик полностью `Done (Committed)` — переходить к следующему.
4. После каждого закрытого task/story — обновить индекс в **той же** итерации (§«Актуальная точка» при смене волны).

## Контракт ролей (обязательный)
- **Epic decomposition:** `@.cursor/commands/bullrun-epic-decompose.md`
- **Thinking (always-on analysis):** `@.cursor/rules/analysis.mdc`
  - допустимый вход через `@.cursor/commands/run-analysis.md`
- **Process (Story or Task execution):** `@.cursor/commands/bullrun-start.md`
- **Skill (Python-only):** `@.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Git:** [`docs/methodology/git-commit.md`](../../../docs/methodology/git-commit.md), [`docs/methodology/git-commit-prompt.md`](../../../docs/methodology/git-commit-prompt.md)

## Уровни процесса

### 1) Epic
1. Определить стартовый эпик по `bullrun-launch-index.md`.
2. Выбрать `EPIC-M2-*` со статусом `Draft` или `In Progress`.
3. Запустить декомпозицию через `bullrun-epic-decompose` с мышлением `analysis.mdc`.
4. Результат декомпозиции:
   - `stories/STORY-M2-XX-YY-*.md`
   - task-папка на каждую сторис: `docs/tasks/task-m2-xx-yy-*/`

### 2) Story или Task
1. Выбрать конкретную `STORY-M2-*` или `task-*`:
   - либо через `ACTIVE_TASK_PATH`;
   - либо через fallback-приоритизацию из индекса.
2. Выполнять через `@.cursor/commands/bullrun-start.md` (пошаговый процесс, фазовый лог, AC-верификация).
3. Для Python-историй явно фиксировать `Skill declared: python-pro` в task-артефактах.

### 3) Execution
1. Вести `BULLRUN-PHASE-LOG.md` по этапам.
2. На паузах выдавать чекпоинт: сделано / осталось / согласование / жду фидбек.
3. Перед закрытием обязательно выполнить и заполнить `acceptance-verification-*.md`.
4. После каждой story синхронизировать `bullrun-launch-index.md`.

## Run-task hard gates (обязательные)
Источник: `@.cursor/commands/run-task.md`.

1. Выполнение только фазами (не одним проходом).
2. Проверка покрытия фаз: перед закрытием сверить, что все фазы из `implementation-plan-*` выполнены, включая фазу с тестами.
3. На каждом stop-point обязателен checkpoint-блок:
   - что сделано;
   - что осталось;
   - что требует согласования;
   - жду фидбек.
4. Decision points и коммит-план согласуются с оператором до перехода дальше.
5. Процесс завершен только после:
   - этапа коммитов;
   - итоговой ретроспективы.

## Gate: Phase Coverage
Перед переводом story/task в финальный статус:
1. Сопоставить фактически выполненные фазы с `implementation-plan-*`.
2. Убедиться, что фаза тестов не пропущена.
3. Зафиксировать результат сверки в `acceptance-verification-*.md`.

## Минимальный контракт артефактов

### Для Story файла
- Обязательные поля: `Key`, `Parent Epic`, `Status`, `AC / DoD`, `Task Artifacts`.
- `Task Artifacts` должны ссылаться на:
  - `README.md`
  - `BULLRUN-PHASE-LOG.md`
  - `acceptance-verification-*.md`

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
- Для `task-*` из `Cross-Epic Task Backlog` применяется та же дисциплина синхронизации статуса в индексе.

## Artifact dates (pkg / gate / run-summary)

SSOT методологии: [`builder-artifact-dates.md`](../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md).

- Перед записью дат: `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now`
- Gate `Date:` и `acceptance-verification-*.md` — только после live pytest + `--verify` в той же сессии
- Перед story Done: `--verify --check-dates` (см. gateway-operator-contract §5)

## Run Summary Report (timestamped)
Для каждого запуска (`epic/story/task batch`) обязателен единый агрегированный отчет:
- Формат имени: `run-summary-YYYYMMDD-HHMM.md` (prefix из `--print-utc-now`, см. artifact dates guide)
- Локация: `docs/tasks/run-reports/`
- Частота: один отчет на один запуск

### Минимальные секции отчета
1. `Run metadata`:
   - timestamp;
   - режим источника (`explicit`/`fallback`);
   - `ACTIVE_TASK_PATH` (если был задан).
2. `Process coverage`:
   - какие шаги `run-task` реально пройдены.
3. `Executed items`:
   - epics/stories/tasks, выполненные в рамках запуска.
4. `Acceptance summary`:
   - что принято;
   - что заблокировано.
5. `Commit summary`:
   - hash/message/scope.
6. `Open follow-ups`:
   - остаточные действия и риски.

### Реестр отчетов
После создания `run-summary-*` в той же итерации обновляется реестр в:
- [`bullrun-launch-index.md`](./bullrun-launch-index.md), секция `Run Reports Registry`.

## Режимы запуска (универсальный процесс)
- `EPIC_BATCH` — запуск на нескольких эпиках.
- `STORY_BATCH` — запуск на нескольких story.
- `TASK_BATCH` — запуск на нескольких точечных task.

Для всех режимов одинаково обязательны:
1. резолв источника (`ACTIVE_TASK_PATH` или fallback от индекса);
2. phase-gates и checkpoint дисциплина;
3. единый итоговый `run-summary-*` отчет и регистрация в индексе.

## Аудит консистентности и полноты (quality audit)

### Current
1. План project-specific для `doge-complaints-gateway` (имя, зона, ссылки и индексы).
2. Источник запуска однозначен: `ACTIVE_TASK_PATH` или fallback от `⚪` в bullrun.
3. Критичные run-task шаги зафиксированы как hard-gates.
4. Отчетность запуска стандартизирована (`run-summary-*` + registry).

### Контрольные anti-drift правила
1. Любая новая операция в процессе должна иметь явный home section в этом файле.
2. Если меняется порядок фаз, обязательна актуализация `Gate: Phase Coverage`.
3. Если добавляется новый тип batch, он обязан быть описан в разделе `Режимы запуска`.

## Быстрый runtime-чеклист
1. Проверить Input Source:
   - если `ACTIVE_TASK_PATH` задан — запустить от него;
   - если нет — выбрать первую `⚪` сущность из индекса по правилу приоритета.
2. Epic/Story/Task выбраны и статус корректный.
3. Декомпозиция (если нужна) выполнена через `bullrun-epic-decompose + analysis.mdc`.
4. Task-папка существует и содержит обязательные файлы.
5. Выполнение идет фазами через `bullrun-start`, без пропуска тестовой фазы.
6. Для Python story: отмечено `Skill declared: python-pro`.
7. На каждом стопе выдан checkpoint-блок (сделано/осталось/согласование/жду фидбек).
8. Перед завершением выполнен `Gate: Phase Coverage`.
9. Сформирован `run-summary-YYYYMMDD-HHMM.md` в `docs/tasks/run-reports/`.
10. Реестр `Run Reports Registry` в индексе обновлен в той же итерации.
11. Изменения процесса не выходят за пределы project-zone `doge-complaints-gateway/docs/tasks/`.
