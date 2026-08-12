# STORY-GW-SEED-01 — Загрузчик историй + готовность hosted-таргета

## Meta
- **Key:** `STORY-GW-SEED-01`
- **Status:** 🔵 Done (Awaiting Commits)
- **Закрывает:** D-SEED-1 (hosted-таргет), D-SEED-3 (загрузка через cron-путь)
- **Стартовый документ:** [`simulation-runner-manual.md`](../../../runtime-docs/testing/simulation-runner-manual.md); [интервью](../../../analysis/interview-seed-demo-data-2026-06-20.md)
- **Зависит от:** RC-04 (columnar-миграции применены на hosted)

## Зачем простыми словами
Прежде чем грузить истории в живой демо (Railway+Supabase), надо убедиться, что (а) загрузчик реально кладёт данные в эту БД, и (б) таргет готов: применены новые колонки проекций (RC-04) и включена кластеризация. Иначе истории либо не запишутся, либо никогда не станут карточками.

## Что наблюдаю сейчас (verified)
- Загрузчик [`tests/simulation_runner.py`](../../../../tests/simulation_runner.py) совместим с canvas v0_1 (читает `normalized_issue_payload.canonical_payload`); **техдолг:** шлёт `POST /intake/stories` ([`simulation_runner.py:207`](../../../../tests/simulation_runner.py)) — legacy route, к удалению в [GW-DRAFT-06](../story-draft-handoff/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md); **продуктовый путь** — `POST /story-drafts` → `POST /story-drafts/{id}/submit`.
- Конфиг через `.env.test` (`GATEWAY_URL`, `GATEWAY_API_TOKEN`).
- Запись в Supabase идёт только если **сервер** (на который указывает `GATEWAY_URL`) в режиме `DB_BACKEND=supabase`; иначе данные не в hosted (см. [simulation-runner-manual §FAQ](../../../runtime-docs/testing/simulation-runner-manual.md)).
- Пост-RC-04: read/write проекций требует columnar-колонок; `/ready` теперь их проверяет ([audit-gw-rc-04](../../../analysis/audit-gw-rc-04-columnar-model-migration-2026-06-20.md)). На hosted они могут быть НЕ применены (integration-тест skip'ается).
- `CLUSTER_CRON_ENABLED` default=`true`, интервал 60s.

## Требование / целевое состояние
- Подтвердить готовность hosted перед загрузкой: `GET /ready` → `db_ready=true` (значит columnar-колонки и схема на месте).
- Применить columnar-миграции RC-04 (`20260619_1200/1210/1220`) на hosted Supabase, если `/ready` красный.
- Убедиться `CLUSTER_CRON_ENABLED=true` на таргете (иначе кластеризация не пойдёт).
- Прогнать smoke-загрузку (`--max 10`) → 202/200, истории видны в `stories` (submitter `sim:*`).

## Подзадачи (черновик)
- **T01** — Чек-лист готовности hosted: `/ready` зелёный; `DB_BACKEND=supabase`; columnar-миграции применены; `CLUSTER_CRON_ENABLED=true`.
- **T02** — Smoke-прогон загрузчика `--max 10` против hosted; зафиксировать результат.
- **T03** — Полный прогон 130 историй; сводка success/failed.
- **T04** — Зафиксировать факт записи (SQL по `stories` где `submitter_external_user_id LIKE 'sim:%'`).

## Acceptance Criteria
- [x] `GET /ready` на hosted = `db_ready: true` до загрузки.
- [~] `CLUSTER_CRON_ENABLED=true` подтверждён на таргете. — ⚠️ **R1 (MEDIUM):** доказано лишь schema-default `true`; фактический Railway env НЕ запрошен, а локальный `.env`=`false` (значение переопределяемо). См. [`audit-gw-seed-01 §R1`](../../../analysis/audit-gw-seed-01-loader-and-hosted-readiness-2026-06-22.md).
- [x] Smoke `--max 10` → все приняты; полный прогон → сводка зафиксирована.
- [x] В `stories` появились строки `sim:*`.

## Открытые вопросы
- Доступ к hosted Railway/Supabase (URL, токен) и право применять миграции — у кого?
