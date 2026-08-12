# STORY-M2-01-05: Runtime env loading and operator safety

## Meta
- Key: `STORY-M2-01-05`
- Parent Epic: [`../../../EPIC-M2-01-core-foundation-and-governance.md`](../../../EPIC-M2-01-core-foundation-and-governance.md)
- Type: Technical Story
- Status: Draft / Todo
- Stream: M2 Foundation / config governance
- Decision Ref: [`../../../../../docs/analysis/gap-analysis-env-loading-target-state-2026-05-12.md`](../../../../../docs/analysis/gap-analysis-env-loading-target-state-2026-05-12.md) — GAP-02, GAP-03, контекст H1/H4/H2; см. также [`../../../../../docs/analysis/simulation-runner-local-run-validation-2026-05-11.md`](../../../../../docs/analysis/simulation-runner-local-run-validation-2026-05-11.md)
- Gateway override (без смены YAML SSOT): `run_mode=story01_05_env_loading_gaps` — см. [`.cursor/plans/Gateway_builder.plan.md`](../../../../../../.cursor/plans/Gateway_builder.plan.md)
- Skill declared: `python-pro` (runtime)

## Story Goal
Устранить класс операторских ошибок: запуск `uvicorn` без экспорта `.env` в процесс ОС → молчаливый `DB_BACKEND=in_memory`; несогласованность `CLUSTER_PRIMARY_LENS` с `CLUSTER_ACTIVE_LENSES` → неочевидный `ConfigError` на старте; неинформативный `ConfigError` при частично заданном Supabase-env при `in_memory` (GAP-03 / H2).

## Scope
- Реализация и тесты по вложенным таскам T01–T03.
- **Не входит:** смена `pkg-000011`, правка `gateway-active-package.current.yaml`, хранение секретов в репозитории, обязательная зависимость `python-dotenv` (первая итерация T01 — inline merge по Decision Ref §4).

## Out of scope
- GAP-01 (startup warning `in_memory`) — уже реализован в `asgi_app.py` по аудиту; не дублировать работу в этой story кроме регрессионной проверки при необходимости.

## Nested tasks

| Order | Task folder |
|-------|-------------|
| 1 | [`task-m2-01-05-t01-gap-02-provide-app-config-env-file-merge`](./task-m2-01-05-t01-gap-02-provide-app-config-env-file-merge/README.md) |
| 2 | [`task-m2-01-05-t02-gap-cluster-primary-active-lenses-alignment`](./task-m2-01-05-t02-gap-cluster-primary-active-lenses-alignment/README.md) |
| 3 | [`task-m2-01-05-t03-gap-03-in-memory-supabase-env-configerror-clarity`](./task-m2-01-05-t03-gap-03-in-memory-supabase-env-configerror-clarity/README.md) |

## AC / DoD (story level)
- [ ] Закрыты GAP-02 и GAP-03 из Decision Ref (код + тесты по таскам).
- [ ] H4 отражён в `example.env` / `server-env-quickstart.md` и покрыт тестом или явной проверкой в T02.
- [ ] Нет регрессии изоляции pytest: при явном `env` в `provide_app_config` / фикстурах не подхватывается посторонний `.env` из cwd (см. AC T01).
- [ ] `bullrun-launch-index.md` и `Gateway_builder.plan.md` синхронизированы с этой story (override перечислен).

---

## Таблица: gap / гипотеза → task → файлы → статус

| Gap / гипотеза | Task | Целевые файлы / артефакты | Статус |
|----------------|------|---------------------------|--------|
| GAP-01 startup warning `in_memory` | — (вне scope) | `src/core/api/asgi_app.py` | Done (по аудиту) |
| GAP-02 / H1 | T01 | `providers.py`, `test_config_loading.py`, при необходимости util | Todo |
| H4 | T02 | `schema.py`, `example.env`, `server-env-quickstart.md`, тесты | Todo |
| GAP-03 / H2 | T03 | `schema.py`, тесты | Todo |
