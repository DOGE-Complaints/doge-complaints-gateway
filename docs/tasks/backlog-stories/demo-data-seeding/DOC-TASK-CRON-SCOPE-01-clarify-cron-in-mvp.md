# DOC-TASK-CRON-SCOPE-01 — Развести MVP-cron и post-demo automation plane в документации

- **Тип:** Documentation task (не product story — правки только в доках, код не трогаем).
- **Пакет:** demo-data-seeding (cron — часть seed→board pipeline).
- **Статус:** ✅ Done (2026-07-23)
- **Источник:** [audit-mvp-scope-hard-2026-07-21.md](../../../analysis/audit-mvp-scope-hard-2026-07-21.md) §F3.
- **Приоритет:** P2 (scope-drift, риск неверной эксплуатации на демо).

## Проблема (verified)

Документация противоречит коду по вопросу «есть ли фоновая обработка в MVP»:

- [high-level-description.md:258](../../../high-level-description.md) в разделе **Out of Scope (MVP)** пишет: *«Scheduled/background orchestration (post-demo)»*.
- Факт кода: авто-промоция историй в issues держится на **in-process cron-цикле** `ClusterCronJob` ([`src/core/scheduler/cluster_cron.py:23`](../../../../src/core/scheduler/cluster_cron.py#L23)), который стартует в lifespan ([`src/core/api/asgi_app.py:157`](../../../../src/core/api/asgi_app.py#L157)) и **включён по умолчанию**: `CLUSTER_CRON_ENABLED` имеет `required=False, default="true"` ([`src/core/config/schema.py:246`](../../../../src/core/config/schema.py#L246)).
- Intake **не** кластеризует синхронно — помечает историю как отложенную (`cluster_outcome="deferred", reason="cron_deferred"`, [`handlers.py:267`](../../../../src/core/api/handlers.py#L267)). Значит доска `GET /tallinn/issues` наполняется **только** через cron (или через ручной `POST /tallinn/issues`).

**Корень путаницы:** термин «scheduled/background orchestration» в high-level читается как «любой фон», хотя на деле речь о **другом, более общем механизме** — post-demo automation plane из [EPIC-M2-11](../../epics/EPIC-M2-11-post-demo-orchestration-and-scheduled-automation.md) (job runner / named tasks / queue / ручной replay). А MVP-демо использует **минимальный in-process cron-loop** как триггер promotion. Это две разные вещи, и документация их не разделяет.

## Целевое состояние (одна правда)

Явно зафиксировать во всех уместных местах разделение:

| Механизм | Что это | Скоуп |
|----------|---------|-------|
| **`ClusterCronJob`** (in-process cron-loop, `CLUSTER_CRON_ENABLED`) | Минимальный триггер: раз в `CLUSTER_CRON_INTERVAL_S` берёт готовые истории → `process_all_pending()` → промоция кластеров → проекция issue | **В MVP** (по умолчанию ON; демо-доска зависит от него) |
| **Automation plane** (job runner / named tasks / queue / replay) | Обобщённый эксплуатационный слой поверх application services | **Post-demo** (EPIC-M2-11, Draft) |

## Где и как править (scope of edits)

1. **[high-level-description.md](../../../high-level-description.md) §Scope MVP vs Post-Demo** — уточнить формулировку Out-of-Scope:
   - Было: `Scheduled/background orchestration (post-demo)`.
   - Стать: `Обобщённый automation plane (job runner / queue / ручной replay) — post-demo (EPIC-M2-11). NB: минимальный in-process cron-loop промоции кластеров (ClusterCronJob, CLUSTER_CRON_ENABLED, default ON) входит в MVP как триггер доски.`
   - Дополнительно: в §«Жизненный цикл истории» / §«Динамическая кластеризация» добавить строку, что переход `accepted → clustered → projected` выполняет cron-loop, а не синхронный intake.

2. **[demo-data-seeding/INDEX.md](./INDEX.md)** — уже описывает цепочку и «cron `CLUSTER_CRON_ENABLED` default=`true`, интервал 60s» (это **корректно**). Добавить одну ссылку-сноску на разделение MVP-cron vs post-demo automation plane (на этот doc-task), чтобы не читалось как противоречие high-level.

3. **[EPIC-M2-11](../../epics/EPIC-M2-11-post-demo-orchestration-and-scheduled-automation.md)** — в Problem Statement / Scope добавить явную оговорку: *«MVP уже содержит минимальный in-process `ClusterCronJob`; этот эпик — про обобщённый automation plane поверх него, не про его замену»*.

4. **Конфиг-документация ([example.env](../../../../example.env) блок `Story-first cluster runtime knobs`)** — добавить комментарий к `CLUSTER_CRON_*`: назначение (триггер promotion), default ON, и что выключение (`false`) останавливает автонаполнение доски (останется только ручной `POST /tallinn/issues`).

5. **Sync-артефакты** — [gateway-backlog-dashboard.md](../../gateway-backlog-dashboard.md) §Docs backlog: строка DOC-TASK-CRON-SCOPE-01; при закрытии обновить статус на Done.

## Явно НЕ входит

- Любые изменения кода/поведения cron (значения, гейты) — только документация.
- Решение «выключать ли cron на проде» — оно **не требуется**: целевое состояние = cron остаётся в MVP, документация приводится в соответствие с кодом.

## Definition of Done

- [x] high-level §Scope больше не читается как «фон вне MVP» без оговорки про `ClusterCronJob`.
- [x] high-level §lifecycle/кластеризация называет cron как исполнителя перехода в `clustered/projected`.
- [x] EPIC-M2-11 явно отделяет себя от MVP-cron.
- [x] example.env комментирует `CLUSTER_CRON_*` (назначение + эффект выключения).
- [x] Ни в одном из тронутых доков не осталось утверждения, противоречащего `default="true"` и in-process cron.
- [x] Dashboard F3 → закрыт.
