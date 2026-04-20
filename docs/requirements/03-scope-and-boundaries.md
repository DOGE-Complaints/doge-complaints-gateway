# 03. Scope и границы

## In Scope (обязательно в MVP)
- приём narrative package из GPT-контура;
- хранение истории как первичной сущности;
- поддержка Story Profile / Signal Profile;
- динамические cluster views;
- перевод зрелого кластера в distinct issue;
- SPA-совместимая issue-проекция;
- evidence pack и lineage.

## Out of Scope (явно исключено)
- интервью с пользователем;
- policy/gate как источник норм;
- on-chain токенизация/голосование;
- финальный гос-статус и внешняя Smart City интеграция.

## Post-demo backlog (документировано отдельно, без расширения MVP)

Исследования и требования после demo (оркестрация/cron, сценарии токенизации/уведомлений на уровне story) ведутся в `20-post-demo-orchestration-and-scheduled-jobs.md` и `21-post-demo-story-tokenization-and-contributor-notifications.md` и **не меняют** границы текущего MVP до отдельного решения.

## Границы ответственности
- **Upstream:** GPT поставляет narrative + (опц.) структурные сигналы.
- **Current module:** operational truth и подготовка производных объектов.
- **Downstream:** Web3/external принимают уже нормализованные артефакты.

## Управление пограничными зонами
- контрактные DTO между слоями;
- явные статусы “interpreted vs asserted by user”;
- версия projection-правил (чтобы реконструировать прошлые решения).

## NFR для границ
- расширяемость без ломки SPA;
- наблюдаемость lineage на каждом переходе;
- обратимость решений кластеризации.
