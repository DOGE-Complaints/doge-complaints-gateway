# STORY-GW-SEED-01 — Загрузчик историй + готовность hosted-таргета

## Meta
- **Key:** `STORY-GW-SEED-01`
- **Parent Epic:** [`../../../EPIC-M2-19-demo-data-seeding.md`](../../../EPIC-M2-19-demo-data-seeding.md)
- **Type:** Technical Story
- **Status:** 🔵 Done (Awaiting Commits) — gate PASS 2026-06-21; pkg-000036 T01–T05
- **Закрывает:** D-SEED-1 (hosted-таргет), D-SEED-3 (загрузка через cron-путь)
- **source:** [`../../../../backlog-stories/demo-data-seeding/STORY-GW-SEED-01-loader-and-hosted-readiness.md`](../../../../backlog-stories/demo-data-seeding/STORY-GW-SEED-01-loader-and-hosted-readiness.md)
- **Стартовый документ:** [`simulation-runner-manual.md`](../../../../../runtime-docs/testing/simulation-runner-manual.md); [интервью](../../../../../analysis/interview-seed-demo-data-2026-06-20.md)
- **Зависит от:** RC-04 (columnar-миграции применены на hosted)
- **Decision Ref:** backlog file above; [`interview-seed-demo-data-2026-06-20.md`](../../../../../analysis/interview-seed-demo-data-2026-06-20.md) — D-SEED-1, D-SEED-3, D-SEED-4; [`demo-data-seeding/INDEX.md`](../../../../backlog-stories/demo-data-seeding/INDEX.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000036-20260621-gw-seed-01-loader-and-hosted-readiness.yaml`](../../../../gateway-active-packages/pkg-000036-20260621-gw-seed-01-loader-and-hosted-readiness.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **5** тасков T01–T05; audit follow-up **T06** (`run_mode=gw_seed_01_audit_followup`, superseded by T07 CF-A path); **T07** (`run_mode=gw_seed_02_audit_cf_a_followup`)

## Зачем простыми словами
Прежде чем грузить истории в живой демо (Railway+Supabase), надо убедиться, что (а) загрузчик реально кладёт данные в эту БД, и (б) таргет готов: применены новые колонки проекций (RC-04) и включена кластеризация. Иначе истории либо не запишутся, либо никогда не станут карточками.

## Что наблюдаю сейчас (verified)
- Загрузчик [`tests/simulation_runner.py`](../../../../../../tests/simulation_runner.py) совместим с canvas v0_1 (читает `normalized_issue_payload.canonical_payload`); шлёт `POST /intake/stories`; конфиг через `.env.test` (`GATEWAY_URL`, `GATEWAY_API_TOKEN`).
- Запись в Supabase идёт только если **сервер** (на который указывает `GATEWAY_URL`) в режиме `DB_BACKEND=supabase`; иначе данные не в hosted (см. [simulation-runner-manual §FAQ](../../../../../runtime-docs/testing/simulation-runner-manual.md)).
- Пост-RC-04: read/write проекций требует columnar-колонок; `/ready` теперь их проверяет ([audit-gw-rc-04](../../../../../analysis/audit-gw-rc-04-columnar-model-migration-2026-06-20.md)). На hosted они могут быть НЕ применены (integration-тест skip'ается).
- `CLUSTER_CRON_ENABLED` default=`true`, интервал 60s.

## Требование / целевое состояние
- Подтвердить готовность hosted перед загрузкой: `GET /ready` → `db_ready=true` (значит columnar-колонки и схема на месте).
- Применить columnar-миграции RC-04 (`20260619_1200/1210/1220`) на hosted Supabase, если `/ready` красный.
- Убедиться `CLUSTER_CRON_ENABLED=true` на таргете (иначе кластеризация не пойдёт).
- Прогнать smoke-загрузку (`--max 10`) → 202/200, истории видны в `stories` (submitter `sim:*`).

## Out of scope
- Расширение датасета (SEED-02)
- Финальный e2e runbook (SEED-03)
- Новый ручной триггер кластеризации
- Понижение `CLUSTER_MIN_SIZE`
- Правки application code (`src/core/`)

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-seed-01-t01-hosted-readiness-checklist-and-columnar-migrations`](./task-gw-seed-01-t01-hosted-readiness-checklist-and-columnar-migrations/README.md) | pkg-000036 |
| 2 | [`task-gw-seed-01-t02-smoke-simulation-runner-max-10`](./task-gw-seed-01-t02-smoke-simulation-runner-max-10/README.md) | pkg-000036 |
| 3 | [`task-gw-seed-01-t03-full-simulation-run-130-stories-summary`](./task-gw-seed-01-t03-full-simulation-run-130-stories-summary/README.md) | pkg-000036 |
| 4 | [`task-gw-seed-01-t04-verify-stories-sim-prefix-sql`](./task-gw-seed-01-t04-verify-stories-sim-prefix-sql/README.md) | pkg-000036 |
| 5 | [`task-gw-seed-01-t05-story-acceptance-gate`](./task-gw-seed-01-t05-story-acceptance-gate/README.md) | pkg-000036 |
| 6 | [`task-gw-seed-01-t06-verify-hosted-cluster-cron-enabled-railway-env`](./task-gw-seed-01-t06-verify-hosted-cluster-cron-enabled-railway-env/README.md) | audit override (`run_mode=gw_seed_01_audit_followup`; superseded by T07 CF-A) |
| 7 | [`task-gw-seed-01-t07-close-r1-empirical-cron-evidence-cf-a`](./task-gw-seed-01-t07-close-r1-empirical-cron-evidence-cf-a/README.md) | audit override (`run_mode=gw_seed_02_audit_cf_a_followup`) |

## Acceptance Criteria
- [x] `GET /ready` на hosted = `db_ready: true` до загрузки.
- [x] `CLUSTER_CRON_ENABLED=true` подтверждён на таргете — **R1 → T07 CF-A** (empirical cron proof); T06 railway env optional/superseded.
- [x] Smoke `--max 10` → все приняты; полный прогон → сводка зафиксирована.
- [x] В `stories` появились строки `sim:*` (count 141).

## Открытые вопросы
- Доступ к hosted Railway/Supabase (URL, токен) и право применять миграции — у кого?
