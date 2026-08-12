# STORY-GW-DRAFT-07 — Hosted schema blocks browser submit

## Meta
- **Key:** `STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit`
- **Пакет:** [`story-draft-handoff/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) — gate PASS 2026-08-07T07:04:17Z pkg-000056
- **Приоритет:** 🔴 P0 — demo / value-loop blocker (browser publish)
- **Тип:** fix / ops (hosted schema readiness)
- **Основание:** SPA UAT FE-HANDOFF-03 · pin [`pin-STORY-SPA-BUG-01-root-cause-2026-08-06.md`](../../../../../spa-app/docs/analysis/pin-STORY-SPA-BUG-01-root-cause-2026-08-06.md) · evidence [`evidence-STORY-SPA-BUG-01-submit-http-2026-08-06T201810Z.md`](../../../../../spa-app/docs/analysis/evidence-STORY-SPA-BUG-01-submit-http-2026-08-06T201810Z.md)
- **Связано с:** [STORY-SPA-BUG-01](../../../../../spa-app/docs/tasks/backlog-stories/bugs/STORY-SPA-BUG-01-story-submission-unavailable.md); [GW-DRAFT-02](./STORY-GW-DRAFT-02-browser-submit-verification-gate.md); [GW-TAX-01](../taxonomy-fidelity/STORY-GW-TAX-01-taxonomy-persistence-fidelity.md) (D-TAX-2 · таблица `story_labels`)
- **Зависит от:** [GW-DRAFT-01](./STORY-GW-DRAFT-01-story-draft-stash.md)/[02](./STORY-GW-DRAFT-02-browser-submit-verification-gate.md) Done (роуты стеша/сабмита); TAX-01 **код** Done; **hosted DDL для `story_labels` applied** (DRAFT-07 T02, text FK)
- **Разблокирует:** FE-HANDOFF-03 / [SPA-BUG-01](../../../../../spa-app/docs/tasks/backlog-stories/bugs/STORY-SPA-BUG-01-story-submission-unavailable.md) retest → 202 (без FE-only hotfix)

## Зачем простыми словами

Verified-пользователь открывает черновик в SPA — preview полный. Нажимает **Submit** → «сервис недоступен»; Retry то же. История не публикуется. Ломается последний шаг handoff (GPT → SPA → publish), хотя draft и auth живы. Root cause — не SPA: на Public Node нет таблицы `story_labels`, gateway считает БД не готовой и режет intake 503.

## Что наблюдаю сейчас — pre-fix UAT 2026-08-06 (historical)

> **Historical.** Снимок до T02–T04. Не текущее hosted-состояние.

## Текущее состояние (post-Done, after T02–T05)

| Элемент | As-is | Ref |
|---------|-------|-----|
| Live `/ready` | `status=ready`, `db.ready=true`, `checks.schema=true` | T04; evidence 2026-08-07 |
| Live submit | `POST …/submit` → **202** + `story_id` | T05 evidence |
| Retry same draft | idempotent **202** + same `story_id` (`_story_intake_replay_from_idempotency`); GET draft → **404** | [`handlers.py:656-713`](../../../../src/core/api/handlers.py) |
| Hosted `story_labels` | text FK → `stories(story_id)`; RLS + `service_role` policy | T02 DDL `draft_07_story_labels_text_fk` |

## Pre-fix snapshot (UAT 2026-08-06)

| Элемент | As-is | Ref |
|---------|-------|-----|
| Live preview | `GET /story-drafts/{id}` → **200** (draft filled) | [evidence T01](../../../../../spa-app/docs/analysis/evidence-STORY-SPA-BUG-01-submit-http-2026-08-06T201810Z.md) |
| Live submit | `POST /story-drafts/{id}/submit` → **503** `SERVICE_UNAVAILABLE` · message «Persistence backend is not ready…» · `checks.schema: false` (connectivity / columns / columns_geo_admin / columns_v2 / policy_probe **true**) | evidence body |
| Live `/ready` | `status=degraded`, `db.ready=false`, `checks.schema=false` | pin T02 |
| Intake gate | `db_backend==supabase` и `not db_ready` → envelope + log `story_intake_rejected_db_not_ready` → **503** | [`handlers.py:159-182`](../../../../src/core/api/handlers.py) |
| Readiness build | `db_checks.schema` = `required_tables_ready()`; `db_ready = all(db_checks.values())` | [`dependencies.py:75-83`](../../../../src/core/api/dependencies.py) |
| Required tables | `REQUIRED_READINESS_TABLES` включает **`story_labels`** (+ stories, drafts, embeddings, …) | [`db_supabase.py:29-43`](../../../../src/core/infrastructure/db_supabase.py) |
| Table probe | `GET /rest/v1/{table}?select=*&limit=1` для каждой required; любая ошибка → `schema=false` | [`db_supabase.py:293-303`](../../../../src/core/infrastructure/db_supabase.py) |
| Deps cache | `get_api_dependencies` → `_cached_dependencies` **`@lru_cache(maxsize=1)`** — `db_ready` заморожен до рестарта процесса | [`asgi_app.py:228-238`](../../../../src/core/api/asgi_app.py) |
| Public Node inventory | все readiness-таблицы на месте **кроме `story_labels`** | pin §Mechanism |
| Repo UUID migration | `story_id UUID REFERENCES stories(story_id)` — **несовместимо** с hosted `stories.story_id` = **text** | [`20260714_1200_gw_tax_01_story_labels.sql`](../../../../supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql) |
| Bootstrap DDL (канон для host) | `story_id text … REFERENCES public.stories(story_id)` + RLS | [`bootstrap/000_full_init.sql:86-94`](../../../../supabase/bootstrap/000_full_init.sql), policies `:325-331` |
| SPA symptom | `mapDraftErrorPhase`: 503 → `SERVICE_DOWN` / `story-handoff-service-down` — UI-маппинг, не root cause | [SPA-BUG-01](../../../../../spa-app/docs/tasks/backlog-stories/bugs/STORY-SPA-BUG-01-story-submission-unavailable.md) |

```mermaid
flowchart TB
  subgraph asis [As-is hosted fail]
    Submit["POST /story-drafts/id/submit"] --> Intake["handle_story_intake"]
    Intake --> Gate{"supabase and not db_ready?"}
    Gate -->|yes| Reject503["503 SERVICE_UNAVAILABLE\nstory_intake_rejected_db_not_ready"]
    Gate -->|no| Create["parse + create_story"]
    Build["build_api_dependencies"] --> Schema["required_tables_ready"]
    Schema --> Missing["story_labels missing on Public Node"]
    Missing --> ReadyFalse["db_ready=false"]
    ReadyFalse --> Gate
    Cache["lru_cache deps at process start"] --> ReadyFalse
  end

  subgraph target [DRAFT-07 target]
    DDL["Apply text-FK story_labels + RLS"] --> Redeploy["Redeploy gateway\nclear lru_cache"]
    Redeploy --> ReadyOk["GET /ready schema=true db.ready=true"]
    ReadyOk --> SubmitOk["POST submit → 202 + story_id"]
  end
```

## Требование / целевое состояние

1. Hosted Supabase (Public Node, таргет Railway gateway) имеет таблицу `story_labels` в форме, совместимой с hosted `stories.story_id` (**text** FK), плюс RLS/policy `service_role` и GRANT по канону bootstrap.
2. **Не** применять as-is UUID DDL из [`20260714_1200_gw_tax_01_story_labels.sql`](../../../../supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql) на этот host — FK на text `story_id` упадёт.
3. После DDL — **redeploy/restart** gateway: [`asgi_app.py:228-230`](../../../../src/core/api/asgi_app.py) кэширует `ApiDependencies` (`db_ready`) на старте; flip схемы без рестарта не обновляет readiness.
4. `GET /ready` → `db.ready=true`, `checks.schema=true`.
5. Verified browser `POST /story-drafts/{id}/submit` на валидном draft → **202** + `story_id`; draft consumed; история на заявленной MVP-поверхности.
6. SPA FE-HANDOFF-03 / BUG-01 разблокированы без FE-only hotfix (симптом UI — маппинг 503, не root cause).

## Подзадачи (ops / verify — не src-wave)

- **T01** — Inventory Public Node vs [`REQUIRED_READINESS_TABLES`](../../../../src/core/infrastructure/db_supabase.py): подтвердить, что отсутствует **только** `story_labels` (остальные probe OK).
- **T02** — Apply proposed SQL (text FK + indexes + RLS + GRANT): [`proposed-migration-DRAFT-07-story-labels-text-fk.sql`](./proposed-migration-DRAFT-07-story-labels-text-fk.sql) на Public Node (оператор / gateway session).
- **T03** — Redeploy/restart Railway `doge-complaints-gateway` — сброс `_cached_dependencies` ([`asgi_app.py:228-234`](../../../../src/core/api/asgi_app.py)).
- **T04** — Verify `GET https://dogestonia-tallinn.up.railway.app/ready` → `db.ready: true`, `checks.schema: true`.
- **T05** — Browser submit smoke (verified user + filled draft) → **202** + `story_id`; повторный submit того же draft → idempotent **202** + same `story_id`; GET draft → **404**; зафиксировать evidence в `docs/analysis/`; story acceptance gate.

## Acceptance Criteria

- [x] `GET https://dogestonia-tallinn.up.railway.app/ready` → `db.ready: true`, `checks.schema: true`.
- [x] Verified user + filled draft: Submit → **202** (не 503 `service_down` на happy path).
- [x] Повторный Submit того же consumed draft — idempotent **202** + same `story_id` (без ложной второй публикации); GET draft → **404**.
- [x] Evidence artifact в `doge-complaints-gateway/docs/analysis/` (sanitized ready JSON + submit 202 trace_id) после Done.
- [x] FE-HANDOFF-03 / [SPA-BUG-01](../../../../../spa-app/docs/tasks/backlog-stories/bugs/STORY-SPA-BUG-01-story-submission-unavailable.md) могут закрыть regression на новом draft после этого Done.

## Швы

| Шов | Где |
|-----|-----|
| Submit → intake | [`handlers.py`](../../../../src/core/api/handlers.py) `handle_story_draft_submit` → `handle_story_intake` |
| db_ready gate | [`handlers.py:159-182`](../../../../src/core/api/handlers.py) |
| Readiness assembly | [`dependencies.py:51-83`](../../../../src/core/api/dependencies.py) |
| Table set / probe | [`db_supabase.py:29-43`](../../../../src/core/infrastructure/db_supabase.py), [`:293-303`](../../../../src/core/infrastructure/db_supabase.py) |
| Process cache | [`asgi_app.py:228-238`](../../../../src/core/api/asgi_app.py) `_cached_dependencies` |
| DDL канон | [`bootstrap/000_full_init.sql`](../../../../supabase/bootstrap/000_full_init.sql) · proposed SQL в appendix |
| SPA symptom only | `mapDraftErrorPhase` 503 → `SERVICE_DOWN` (не чинить в этой стори) |

## Граница и контракт

- **In scope:** hosted schema для readiness (`story_labels` + RLS/grants по канону bootstrap); проверка `/ready`; redeploy/restart gateway; verify browser submit; evidence artifact.
- **Вне scope:** правки SPA UI; GPT OpenAPI; identity; переписывание UUID-миграций на других host; полный rewrite TAX/clustering; изменение `REQUIRED_READINESS_TABLES` в коде (таблица должна появиться, не исключаться).

## Открытые вопросы

- Follow-up: починить repo UUID migration [`20260714_…story_labels.sql`](../../../../supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql) для text hosts (отдельная TAX/ops story) vs оставить только bootstrap/proposed path на Public Node?
- Кто владеет apply DDL на Public Node (`lvfrdtglpksmaywqlohj`) в операционном runbook — gateway operator vs Supabase admin?

## Appendix — предложение миграции (не apply в docs-волне)

Оператор применяет в **gateway** / ops сессии. Файл:

[`proposed-migration-DRAFT-07-story-labels-text-fk.sql`](./proposed-migration-DRAFT-07-story-labels-text-fk.sql)

**Обоснование:** создать `public.story_labels` с **text** FK на `stories(story_id)`, индексы, RLS + policy `service_role`, GRANT — как [`bootstrap/000_full_init.sql`](../../../../supabase/bootstrap/000_full_init.sql). Не копировать as-is UUID DDL из `supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql` на этот host. После DDL — redeploy gateway (`lru_cache` readiness).
