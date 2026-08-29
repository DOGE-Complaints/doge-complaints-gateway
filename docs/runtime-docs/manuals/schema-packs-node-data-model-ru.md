# Schema packs: модель данных ноды (операторский мануал)

**Дата:** 2026-08-29T09:20:52Z  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc) — claims только из `src/core` / tests / SQL.  
**Пакет:** [`backlog-stories/semantic-schema-runtime/INDEX.md`](../../tasks/backlog-stories/semantic-schema-runtime/INDEX.md) (T-wave SSR-01…05 Done).  
**Loader keys SSOT:** [`schema-packs/README.md`](../../../schema-packs/README.md) (не универсальный YAML-диалект).  
**Wire:** [`API_REFERENCE.md`](../api-reference/API_REFERENCE.md) §`schema_binding`.

Вопрос: **как после T-wave настраивать модель ноды, что менять в БД, и чего ещё нет.**

---

## Current state (implemented now)

### Два мира на одном intake

Один HTTP-контракт: envelope `schema_version` = `m2.story_intake_envelope.v2` ([`contracts.py`](../../../src/core/intake/contracts.py) `INTAKE_SCHEMA_VERSION`). Кластеризация **не** синхронна на submit — cron зовёт `StoryClusterOrchestrator.process_all_pending` ([`cluster_cron.py:64`](../../../src/core/scheduler/cluster_cron.py)).

| Если в теле | Что происходит |
|-------------|----------------|
| Нет ключа `schema_binding` или `{}` | Civic: ярлыки + `ClusterLens` (10 членов, [`types.py:10–22`](../../../src/core/cluster/types.py)). Binding-поля `StoryRecord` остаются `None`. |
| Объект `schema_binding` | Pack: `LocalSchemaRuntime.validate` **до** `save_story` ([`services.py`](../../../src/core/application/services.py)). Потом pack exact-lens. Civic engine эту story **не** берёт (`is_schema_bound` = оба `schema_id` и `bound_schema_version` truthy, [`pack_engine.py:16–18`](../../../src/core/schema/pack_engine.py)). |

Ветка orchestrator: schema-bound → `_process_pack_bound_story`; иначе civic pool `_civic_ready` ([`cluster_orchestrator.py:236–241`](../../../src/core/application/cluster_orchestrator.py)).

Линза = правило «в какую кучу». Membership ≠ Issue. Civic promote: типы `complaint`/`system_bug` + default `PromotionGatePolicy` ([`gates.py:7–14`](../../../src/core/promotion/gates.py)). Pack promote: `readiness_policy` из файла пака, mapper [`pack_policy.py`](../../../src/core/schema/pack_policy.py); civic default/factory **не** меняются.

Pack engine читает **только** `structured_payload` по dotted path. `narrative_*`, `canonical_labels`, geo civic **не** source_fields ([`pack_engine.py:103–105`](../../../src/core/schema/pack_engine.py)).

### Код и файлы пака

```text
src/core/schema/          # LocalSchemaRuntime, resolver, validator, pack_engine, pack_policy
schema-packs/
  <schema_id>/<schema_version>/
    pack.json
    payload.schema.json
```

Сейчас на диске: `legal_process/v1`, `mobility_observation/v1`, `tallinn_civic/v1` (civic-оси как payload map; `ClusterLens` не копируется).

Корень: env **`SCHEMA_PACKS_ROOT`** или default `<gateway-root>/schema-packs/` ([`resolver.py:19–30`](../../../src/core/schema/resolver.py)). Поля в [`AppConfig`](../../../src/core/config/schema.py) **нет** — читается `os.environ` в resolver.

`build_index` / `project` бросают `NotImplementedError` ([`runtime.py:62–72`](../../../src/core/schema/runtime.py)). Это не IDX и не processor.

### Wire `schema_binding`

Разрешённые inner keys: `schema_id`, `schema_version` (semantic pack, **не** envelope), optional `profile_id` / `profile_version`, `structured_payload`. `payload_hash` на проводе запрещён (сервер считает). Inner `schema_version` ≠ `m2.story_intake_envelope.v2`.

Пример (pack `legal_process` / `v1` — поля из [`payload.schema.json`](../../../schema-packs/legal_process/v1/payload.schema.json)):

```json
{
  "schema_version": "m2.story_intake_envelope.v2",
  "submitter": {
    "external_user_id": "telegram:123456789",
    "identity_issuer": "telegram"
  },
  "narrative": {
    "original_text": "Filed at office 12.",
    "language": "en",
    "title": { "en": "Office filing" },
    "description": { "en": "Process at office 12." }
  },
  "schema_binding": {
    "schema_id": "legal_process",
    "schema_version": "v1",
    "profile_id": "legal_access",
    "structured_payload": {
      "institution": { "office_id": "office-12", "name": "Station" },
      "process": { "stage": "filed" }
    }
  }
}
```

Нарратив (title/description) по-прежнему обязателен. Pack-поля живут в payload, не вместо civic envelope.

Пример (pack `tallinn_civic` / `v1` — civic-оси в `structured_payload`, не labels; gateway fixture [`tests/fixtures/gw_ssr_08_tallinn_civic_envelope.json`](../../../tests/fixtures/gw_ssr_08_tallinn_civic_envelope.json); не GPT UI):

```json
{
  "schema_version": "m2.story_intake_envelope.v2",
  "submitter": {
    "external_user_id": "telegram:123456789",
    "identity_issuer": "telegram"
  },
  "narrative": {
    "original_text": "Pothole on the tram line.",
    "language": "en",
    "title": { "en": "Tram pothole" },
    "description": { "en": "Recurring pothole on the tram line." },
    "canonical_type": "complaint"
  },
  "schema_binding": {
    "schema_id": "tallinn_civic",
    "schema_version": "v1",
    "structured_payload": {
      "signals": {
        "civic_domain": "transport",
        "failure_pattern": "broken_infrastructure",
        "civic_weight": "recurring_issue",
        "desired_outcome": "better_maintenance",
        "affected_group": "residents",
        "service_object": "tram_line",
        "need": "unknown",
        "ecosystem_signal": "unknown",
        "canonical_type": "complaint"
      },
      "geo": { "district": "kesklinn" }
    }
  }
}
```

### Как добавить ноду (данные, не колонки)

1. Каталог `schema-packs/<schema_id>/<schema_version>/`.
2. `pack.json` — ключи loader ([`schema-packs/README.md`](../../../schema-packs/README.md)): `field_policy`, ≥1 `exact_lenses`, `readiness_policy` с **тремя** knobs.
3. `payload.schema.json` — JSON Schema для `structured_payload`.
4. Числа порогов — **в файле пака**, не копировать civic `70`/`2` из `gates.py`.
5. Intake с `schema_binding`. Cron тот же — второго cron нет.

Не делать: новый член `ClusterLens`; domain-колонки `stories`; новый HTTP filter path.

---

## БД: ALTER `stories`, не пересоздавать контур

Нужны **шесть nullable** колонок на существующей `public.stories`. Civic строки остаются `NULL`. Таблицы `cluster_memberships`, `doge_issues`, `issue_candidates` **не** меняли DDL под pack: pack пишет `cluster_memberships.lens` строкой (`police_station`), не enum.

| Колонка | Смысл |
|---------|--------|
| `schema_id` | id пака |
| `bound_schema_version` | версия пака (**не** envelope `schema_version`) |
| `profile_id` / `profile_version` | optional |
| `structured_payload` | JSONB |
| `payload_hash` | SHA-256 канонического JSON, считает сервер |

Где смотреть:

- Hosted: [`supabase/migrations/20260828_1400_gw_ssr_02_stories_schema_binding.sql`](../../../supabase/migrations/20260828_1400_gw_ssr_02_stories_schema_binding.sql)
- Bootstrap: [`000_full_init.sql`](../../../supabase/bootstrap/000_full_init.sql) (тот же `ADD COLUMN IF NOT EXISTS`)
- SQLite: `_ensure_sqlite_schema_migrations` в [`db_sqlite.py`](../../../src/core/infrastructure/db_sqlite.py) при `ensure_schema()`
- Domain: [`StoryRecord`](../../../src/core/domain/contracts.py) `:68–74`

### Что сделать, чтобы заработало

| Backend | Действие |
|---------|---------|
| `in_memory` | Ничего. Dataclass хранит поля целиком. |
| `sqlite` | Ничего руками. Старт сам `ALTER`. |
| Hosted Supabase | Применить миграцию `20260828_1400_*`. Пока колонок нет, omit-probe в [`db_supabase.py`](../../../src/core/infrastructure/db_supabase.py) **вырезает** binding из SELECT/save — civic живёт, pack persist на host **нет**. После apply — **рестарт** процесса (probe кэшируется). **G9:** live hosted apply + restart = **operator/deploy**, не overnight proof (как `live_integration` в T-wave). |

**Не** класть binding-колонки в `required_columns_ready` (иначе `/ready` 503 до apply).

Pack-файлы должны быть в дереве gateway (`schema-packs/`) или `SCHEMA_PACKS_ROOT` на volume/образе (поле **нет** в `AppConfig` — только `os.environ` в [`resolver.py:19–30`](../../../src/core/schema/resolver.py)). CWD ≠ корень gateway → выставить env. **Dockerfile в gateway не найден** (Glob 0) — не invent; фактический build (Railway/Nixpacks root) копирует исходники. Live image = operator, не overnight proof. Нет каталога → intake с binding → unknown schema.

Карточка `GET /node/issues`: `DOGEIssue.to_public_dict` **без** `structured_payload` ([`dto.py`](../../../src/core/projection/dto.py)). Overlay SPA — sibling spa-16, не этот runtime.

---

## Planned target

- Civic Tallinn как **pack-данные** (`schema-packs/tallinn_civic/v1`) для *новых* bound stories — [`STORY-GW-SSR-08`](../../tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-08-tallinn-civic-schema-pack.md). Не удаляет `ClusterLens`. Pack не видит labels — значения в payload.
- IDX `story_dimensions` / generic filter HTTP — [`STORY-GW-SSR-06`](../../tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-06-analytical-index-later.md) Draft. `build_index` не реализация IDX.
- Processors — [`STORY-GW-SSR-07`](../../tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-07-processor-delivery-later.md). Validate ≠ Generic Processor.
- GPT MAY emit `schema_binding` (sibling REQ-45). Без этого pack-intake только ручной JSON.

---

## Gaps / risks

| Gap | Факт |
|-----|------|
| Env не в AppConfig | `SCHEMA_PACKS_ROOT` только `os.environ` в resolver; нет fail-fast в `load_config_from_env`. |
| Hosted без миграции | Omit-probe: civic OK, binding не пишется. |
| Civic ≠ pack 1:1 | `infer_signals_from_canonical` ([`enrichment.py:39–84`](../../../src/core/profile/enrichment.py)) ≠ dotted payload. Нельзя «скопировать enum в pack.json». |
| GPT | Парсер готов; instruction pack emit — не этот репозиторий-слой. |
| IDX / PROC | Stubs. T-wave закрыт без них (AC-018). |
| Аудит T-wave vs код | Product AC SSR-01…05 закрыты (gates pkg-000061…065). Этот мануал закрывает операторский разрыв docs. |

### Аудит T-wave (сводка)

| Стори | Код | Совпадает с AC |
|-------|-----|----------------|
| SSR-01 | `src/core/schema/` + `jsonschema` + example packs | Да |
| SSR-02 | шесть колонок + sqlite ALTER + bootstrap | Да |
| SSR-03 | sidecar parse + validate до persist | Да |
| SSR-04 | `SchemaPackClusterEngine`; civic enum 10 | Да |
| SSR-05 | pack promote без civic types; factory civic default True | Да |
