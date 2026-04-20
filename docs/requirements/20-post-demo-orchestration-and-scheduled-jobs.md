# 20. Post-demo: оркестрация, scheduled jobs и автоматизация

## Статус

**Post-demo / pilot-ops.** Не входит в обязательный объём demo delivery Module 2 до отдельного решения о сроках. Служит **требованиями-направлением** для архитектуры (`solution architecture/16-automation-orchestration-and-scheduled-jobs.md`).

## Цель

После стабилизации доменных модулей (story → profile → cluster → promotion → projection) обеспечить:

1. **Повторное использование** одних и тех же use-case для синхронного API и фоновых запусков.
2. **Предсказуемость**: ручные операции и cron не расходятся по семантике.
3. **Операбельность**: метрики, алерты, идемпотентность, trace по job execution.

## Функциональные ожидания (high level)

- Определение **именованных задач** (например «recalculate cluster views for lens set X», «rebuild projection batch») как вызовов application-сервисов, а не ad-hoc скриптов.
- Возможность **запуска по расписанию** и **ручного запуска** тем же кодом.
- Явная политика **concurrency** (не два полных пересчёта одного scope без блокировки/lease).
- **Audit / log** результата job (успех, частичный успех, ошибка) с `trace_id`.

## Нефункциональные требования

- Секреты и service-role доступ к БД — только из доверенного runtime (не в браузере).
- Ошибки фона не должны молча портить доменные инварианты: fail-closed или компенсирующая запись в ops log.

## Границы

- Не дублировать **issue promotion** и **operator review** как полностью автоматические без политики продукта — см. отдельные решения в `17-open-decisions-and-decision-log.md`.
- Детализация конкретных cron-выражений и инфраструктуры — в эпике **EPIC-M2-11**.

## Traceability

- Архитектура: `docs/solution architecture/16-automation-orchestration-and-scheduled-jobs.md`
- Эпик: `docs/tasks/epics/EPIC-M2-11-post-demo-orchestration-and-scheduled-automation.md`
