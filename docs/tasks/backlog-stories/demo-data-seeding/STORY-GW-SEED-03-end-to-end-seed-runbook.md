# STORY-GW-SEED-03 — E2E seed-runbook + проверка наполнения доски

## Meta
- **Key:** `STORY-GW-SEED-03`
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** P3 — hosted leg после RC-07
- **Тип:** docs + ops verify + runner (stash+submit)
- **Закрывает:** D-SEED-4 (e2e-мануал + проверка)
- **Стартовый документ:** [интервью](../../../analysis/interview-seed-demo-data-2026-06-20.md)
- **Зависит от:** [SEED-01](./STORY-GW-SEED-01-loader-and-hosted-readiness.md), [SEED-02](./STORY-GW-SEED-02-dataset-expansion-for-clustering.md), [GW-DRAFT-06](../story-draft-handoff/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md) (runner на `/story-drafts`), [GW-SEED-04](./STORY-GW-SEED-04-runner-auth-bootstrap-email-password.md) (runner auth email+password)
- **Разблокировано:** [GW-RC-07](../issues-read-contract/STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md) **Done** 2026-07-10 (hosted read-path)
- **Артефакт:** [`seed-demo-data-runbook-ru.md`](../../../runtime-docs/manuals/seed-demo-data-runbook-ru.md)

## Зачем простыми словами
Свести всё в один воспроизводимый мануал: «как с нуля наполнить демо-доску» — от проверки готовности таргета до загрузки, ожидания кластеризации и проверки, что карточки появились. Чтобы любой оператор повторил без догадок.

## Что наблюдаю сейчас (verified)

- Runbook + runner-manual синхронизированы с GW-DRAFT-06 двухфазным flow (T06).
- Локальный e2e: v0_2 → `GET /tallinn/issues` = 2 карточки ([`verify-gw-seed-03-end-to-end-2026-06-22.md`](../../../analysis/verify-gw-seed-03-end-to-end-2026-06-22.md) §2) через `post_intake_via_story_drafts` (TestClient).
- Hosted read-path: [GW-RC-07](../issues-read-contract/STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md) **Done** — `/tallinn/issues` HTTP 200, **9** карточек (2026-07-11, verify §5).
- Загрузчик: [`simulation_runner.py`](../../../../tests/simulation_runner.py) — **T05 Done:** `POST /story-drafts` (service) → `POST /story-drafts/{id}/submit` (user Bearer); live HTTP — [`simulation_intake_http.py`](../../../../tests/simulation_intake_http.py), smoke — [`post_intake_via_story_drafts_http`](../../../../tests/smoke/conftest.py).
- Env: `GATEWAY_API_TOKEN` + `GATEWAY_USER_EMAIL`/`GATEWAY_USER_PASSWORD` + `SUPABASE_URL`/`SUPABASE_ANON_KEY` (GW-SEED-04 password grant → Supabase access_token); см. [`.env.test.example`](../../../../.env.test.example).
- **Ops:** полный hosted re-seed через runner требует email+password в `.env.test` (verify §5).

## Требование / целевое состояние

- Локально: runbook + verify + runner materialize stories — **Done** (T05/T06).
- Hosted: read-path + board fill — **Done**; runner re-seed на prod — ops (email+password в `.env.test`, GW-SEED-04).

## Подзадачи

| ID | Задача | Status |
|----|--------|--------|
| **T01** | Финализировать runbook (команды, env, ожидаемый вывод) | Done |
| **T02** | Раздел диагностики «пустая доска» | Done |
| **T03** | Hosted: preflight + board ≥2; runner re-seed — ops email+password | Done (preflight) |
| **T04** | Кросс-ссылки simulation-runner-manual ↔ e2e-runbook | Done |
| **T05** | Runner: stash + browser submit (live HTTP) | Done |
| **T06** | Sync runtime SSOT: runbook + runner-manual + `.env.test.example` | Done |

## Acceptance Criteria

- [x] Мануал `seed-demo-data-runbook-ru.md` финализирован (T01/T02/T06).
- [x] Runner материализует stories: stash **201** + submit **202** (не silent stash-only) — T05 + `test_gw_seed_03_simulation_runner_submit.py`.
- [x] Runtime SSOT синхронизирован с GW-DRAFT-06 (T06).
- [x] Hosted: доска наполнена (9 карточек, ≥2); `/ready` green (T03 preflight, verify §5).

## Открытые вопросы

- ~~Интервал cron на время seed~~ — **решено:** `CLUSTER_CRON_INTERVAL_S=20` на время seed, затем 60s (runbook §Шаг4).

## Швы

- Runbook: [`seed-demo-data-runbook-ru.md`](../../../runtime-docs/manuals/seed-demo-data-runbook-ru.md)
- Runner SSOT: [`simulation-runner-manual.md`](../../../runtime-docs/testing/simulation-runner-manual.md)
- Verify: [`verify-gw-seed-03-end-to-end-2026-06-22.md`](../../../analysis/verify-gw-seed-03-end-to-end-2026-06-22.md)
- HTTP helper: [`story_draft_intake_helpers.py`](../../../../tests/story_draft_intake_helpers.py), [`simulation_intake_http.py`](../../../../tests/simulation_intake_http.py), [`smoke/conftest.py`](../../../../tests/smoke/conftest.py)
- Config template: [`.env.test.example`](../../../../.env.test.example)
