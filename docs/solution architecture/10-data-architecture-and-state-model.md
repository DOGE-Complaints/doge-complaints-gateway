# 10. Data Architecture & State Model

## Logical bounded contexts
- Story Context
- Intelligence Context
- Cluster Context
- Issue Projection Context
- Evidence Context
- Geo Context

## Core state machines

### Story lifecycle
`accepted -> profiled -> cluster_eligible -> issue_linked -> archived`

### Cluster lifecycle
`analytics -> candidate -> promoted | reframed | split | merged`

### Issue lifecycle (internal)
`projected_new -> reviewed -> published_ready`

## Persistence principles
- migration-first schema governance;
- immutable core + mutable derived layers;
- explicit version columns for profile/lens/projection policies;
- idempotency keys for command handlers;
- **авторство:** при приёме intake сохранять связь story с внешним субъектом (`submitter.external_user_id`, `identity_issuer`) из OAuth-потока GPT/IdP — opaque string, без обязательной нормализации формата; поле не теряется на пути к evidence (см. `requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md` §5).

**Операционная схема таблиц (bootstrap + runtime ports):** группы `story_drafts`/`draft_owner`, story core, clustering, published board — см. [`docs/runtime-docs/story-persistence-model.md`](../runtime-docs/story-persistence-model.md). Этот SA-документ остаётся логическим state model; детали колонок и ER не дублируются здесь.

## Read models
- board read model (SPA fields only);
- issue details read model (enriched but contract-safe);
- evidence drill-down read model (internal).

## Ключевые изменения схемы (решения интервью 2026-05-13)

### `stories` таблица — новые колонки (v2 контракт)

| Колонка | Тип | Изменение |
|---------|-----|-----------|
| `narrative_title` | JSONB `{et,ru,en}` | ✅ Новая |
| `narrative_description` | JSONB `{et,ru,en}` | ✅ Новая |
| `narrative_summary` | JSONB `{et,ru,en}` | ✅ Новая |
| `narrative_session_language` | TEXT | ✅ Новая |
| `narrative_title_hint` | — | ❌ Удалить (заменено на `narrative_title`) |
| `narrative_title_hint_et/ru/en` | — | ❌ Удалить |
| `submitter_identity_issuer` | TEXT NOT NULL | ♻️ NOT NULL constraint |

### `issue_story_links` таблица — N:M связь (G-11)

```sql
CREATE TABLE IF NOT EXISTS issue_story_links (
    issue_id TEXT NOT NULL,
    story_id TEXT NOT NULL,
    cluster_id TEXT NOT NULL,
    linked_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (issue_id, story_id)
);
```

Обеспечивает множественную принадлежность story к кластерам/Issues (Protocol `ClusterMembershipStore` уже допускает N кластеров на story, но таблицы не было в Supabase bootstrap SQL).

### `StoryGeoSnapshot` — новые admin-уровни (G-02)
`admin_district`, `admin_settlement`, `admin_region`, `admin_country` — см. SA-09.

### Idempotency keys (G-08)
При отсутствии `Idempotency-Key` header — SHA-256 от raw body используется как ключ; предотвращает дубли при GPT retry.

## Automation / scheduled execution (MVP cron + post-demo plane)

Фоновые и cron-задачи **не** являются отдельным источником доменной истины: они должны вызывать те же application use-case, что и API. Инвариант **уже соблюдается** MVP-инстансом `ClusterCronJob` (`CLUSTER_CRON_ENABLED`, default ON → `process_all_pending`); post-demo — расширение (job runner / queue / replay), не замена минимального цикла. Детали — `16-automation-orchestration-and-scheduled-jobs.md` и требования `requirements/20-post-demo-orchestration-and-scheduled-jobs.md`.
