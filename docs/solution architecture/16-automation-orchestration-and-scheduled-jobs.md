# 16. Automation Plane: Orchestration, Cron и фоновые задачи

## Назначение

Зафиксировать архитектурный задел, чтобы после завершения демо-эпиков **удобно** добавлять:

- периодические пересчёты cluster views;
- отложенную обработку enrichment / projection;
- операционные «sweep»-задачи (ретеншн, reconcile);
- ручной replay тех же сценариев без дублирования бизнес-логики.

Документ **не** выбирает конкретный продукт (Kubernetes CronJob, Supabase `pg_cron`, внешний scheduler, worker-процесс). Он задаёт **границы слоёв**, чтобы cron не превратился в параллельную систему правил.

## Проблема без этого слоя

Если фоновые задачи напрямую дергают SQL, обходят доменные инварианты или дублируют переходы state machine, то:

- расходится поведение API и фона;
- сложно тестировать и откатывать;
- ручное управление и автоматизация начинают конфликтовать.

## Принцип: один вход в доменные переходы

- **Application / use-case слой** остаётся единственным местом, где выполняются осмысленные переходы (`story` / `cluster` / `issue candidate` / `projection`), с **idempotency keys** там, где уже заложено в модели данных (см. `10-data-architecture-and-state-model.md`).
- **HTTP API** и **scheduler/worker** вызывают **одни и те же** сервисы/команды (через `ServiceFactory` / DI), а не независимые копии логики.
- **Инфраструктура доставки** (cron, queue, HTTP admin endpoint «run job X») — тонкая оболочка: создать контекст, `trace_id`, вызвать use-case, записать результат/метрику.

## Компоненты (логические)

| Компонент | Роль |
|---|---|
| **Job definition** | Имя, расписание или триггер, параметры (например lens version), политика concurrency. |
| **Job runner** | Процесс, который по событию расписания вызывает use-case; не содержит бизнес-правил кластеров/issues. |
| **Manual override** | Те же use-case через API или internal tool — для операторов и отладки. |
| **Dead-letter / retry** | Зарезервировано для pilot (см. `11-cross-cutting-security-config-observability.md`); в demo может быть no-op. |

## Связь с Supabase / Postgres

- **Миграции и схема** остаются в канале migration-first (`10`).
- **Планировщик** может быть:
  - внешним (вызывает HTTP/internal command);
  - или внутри Postgres (`pg_cron`) **только** если триггер — это вызов **идемпотентного** use-case через тот же контракт (не «сырой SQL как источник истины» для доменных переходов).

Конкретная технология — решение деплоя; архитектурное требование: **не размножать семантику переходов**.

## Наблюдаемость

Метрики и логи для job runs (старт/успех/ошибка/длительность, `trace_id`) — расширение EPIC-M2-09; детализация в `docs/requirements/20-post-demo-orchestration-and-scheduled-jobs.md`.

## Связанные артефакты

- Требования: `docs/requirements/20-post-demo-orchestration-and-scheduled-jobs.md`
- Эпик: `docs/tasks/epics/EPIC-M2-11-post-demo-orchestration-and-scheduled-automation.md`
