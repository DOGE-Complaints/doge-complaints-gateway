# Schema packs: как устроена модель данных ноды

**Дата:** 2026-09-07T08:49:49Z (D-SSR-12 federation consume SSR-35; local warehouse + Railway Volume — SSR-34; D-SSR-11 node-taxonomy — SSR-33; taxonomy dual contour + operator copy-paste — SSR-29; три уровня geo — SSR-27; два контура clustering — SSR-21)  
Факты из кода gateway (`src/core`, `schema-packs/`, тесты). Ключи `pack.json` — в [`schema-packs/README.md`](../../../schema-packs/README.md). HTTP envelope: [`API_REFERENCE.md`](../api-reference/API_REFERENCE.md). Живой smoke: [test-matrix](../testing/test-matrix-by-type-layer-mocks.md) § Local real-HTTP smoke. Env playbooks: [`server-env-quickstart.md`](./server-env-quickstart.md) §Node active schema + warehouse ops.

Этот текст для человека, который поднимает ноду: что лежит на диске (склад), какая пара **рабочая** (`NODE_SCHEMA_*`), куда ходит публичный API.

---

## Коротко

Модель ноды — это **файлы pack**, не новые колонки на каждое поле и не город в URL.

`schema-packs/` на диске — **склад** (библиотека каталогов). Рабочая модель ноды — пара из env: **`NODE_SCHEMA_ID`** + **`NODE_SCHEMA_VERSION`** (оба required в `AppConfig`, fail-fast при старте). Клиент не выбирает произвольный pack телом intake.

Новый intake: `schema_binding.schema_id` + `schema_binding.schema_version` должны **ровно** совпасть с `NODE_SCHEMA_*`. Нет ключа, `{}`, `null` или чужая пара → **4xx**, story не пишется. Кластеризация pack-веткой только если persist binding == той же env-паре; чужой bound (legacy) — skip (лог), не membership чужим `pack.json`. Unbound legacy READY_FOR_PROFILE — civic engine as-is (десять `ClusterLens`).

Публичное чтение одно на всех: `GET /node/issues`, не `/tallinn/issues`. Geo вроде `settlement:tallinn` — это данные локации, не адрес API.

---

## Три пака на диске — нормально

Сейчас:

| Каталог | Зачем |
|---------|--------|
| `legal_process/v1` | пример T-wave (офис / стадия процесса) |
| `mobility_observation/v1` | второй example pack |
| `tallinn_civic/v1` | civic-оси как поля payload (не копия enum `ClusterLens`) |

Корень: переменная **`SCHEMA_PACKS_ROOT`**, иначе каталог `schema-packs/` рядом с корнем gateway ([`resolver.py`](../../../src/core/schema/resolver.py)). В `AppConfig` этого поля нет — только `os.environ`. Если процесс стартовал не из корня gateway, без env resolver не найдёт паки.

### Warehouse model (D-SSR-12 / SSR-34)

| Среда | Корень склада | Active | Git |
|-------|---------------|--------|-----|
| Local | default `doge-complaints-gateway/schema-packs/` (`SCHEMA_PACKS_ROOT` unset) | `NODE_SCHEMA_*` | demo/seed tracked; **node packs (uus…) ignored / not committed** |
| Railway | Volume mount = **`SCHEMA_PACKS_ROOT`** (напр. `/data/schema-packs`) | те же `NODE_SCHEMA_*` | N/A (Volume, не git) |
| Federation remote | fetch → тот же cache root (`SCHEMA_PACKS_ROOT` или default) | без смены identity | **SSR-35** (`SCHEMA_ROOT_URL` + optional `SCHEMA_PACK_REFRESH`) |

**Glossary:** `SCHEMA_PACKS_ROOT` = диск / Volume mount. **`SCHEMA_ROOT_URL` ≠ mount** — http(s) URL удалённого federation registry root (**shipped** SSR-35). Не подставлять путь Volume в `SCHEMA_ROOT_URL`. Fresh cache skips fetch unless `SCHEMA_PACK_REFRESH=true`. Stub manifest: `GET {SCHEMA_ROOT_URL}/{id}/{ver}/manifest.json` → `files` map — см. [`remote_fetch.py`](../../../src/core/schema/remote_fetch.py) / server-env federation playbook.

**Git policy:** ignore node trees (напр. `schema-packs/uus_veerenni_civic/` в gateway `.gitignore`). **Не** ignore весь `schema-packs/` — иначе сломается CI (tallinn/legal/mobility fixtures).

**Fail-fast:** missing/invalid active pack → boot `ConfigError`; **не** silent tallinn. Pack content repair / geo enum expand — **вне** SSR-34 (precondition operator).

**GPT lockstep:** Instructions `schema_binding` == env `NODE_SCHEMA_*` (SSR-17). Смена active pair без обновления GPT → intake 4xx. Gateway docs only — GPT files правятся sibling wave.

Каждый pack — папка `<schema_id>/<schema_version>/`:

```text
schema-packs/<schema_id>/<schema_version>/
  pack.json
  payload.schema.json
  taxonomy.json     ← when pack.json sets taxonomy_schema (tallinn_civic/v1 post SSR-28)
```

`taxonomy.json` обязателен **только** если в `pack.json` есть `taxonomy_schema`. Без ключа файл на диске loader **не** подхватывает (SSR-26). legal/mobility — без taxonomy (tallinn first). Код рантайма: `src/core/schema/`. Форма блоков `taxonomy.json` — [`schema-packs/README.md`](../../../schema-packs/README.md) (не дублировать таблицы здесь).

`build_index` и `project` в [`runtime.py`](../../../src/core/schema/runtime.py) бросают `NotImplementedError`. Это не «сломалось»: индекс и процессоры ещё не в этом контуре.

---

## Склад vs рабочая env

Старт приложения ([`asgi_app.py`](../../../src/core/api/asgi_app.py) `_lifespan`) резолвит **рабочий** pack (`NODE_SCHEMA_ID` / `NODE_SCHEMA_VERSION`) и пишет пару в лог рядом с `startup.config`. Каталоги в `schema-packs/`, которых нет в env, остаются на складе — для отладки, не как «на выбор клиента».

Цепочка на **каждой** story:

1. Intake envelope `schema_version` = `m2.story_intake_envelope.v2`. Кластеризация не в том же HTTP-ответе: cron зовёт `process_all_pending` ([`cluster_cron.py`](../../../src/core/scheduler/cluster_cron.py)).
2. Нет `schema_binding`, `{}` или `null` → **4xx** (`IntakeValidationError`). Новый civic-вход закрыт.
3. Есть объект `schema_binding` — пара должна совпасть с `NODE_SCHEMA_*`. Совпадение → `resolve`/`validate` **активного** pack ([`services.py`](../../../src/core/application/services.py)). Чужой id/version → **4xx**, не silent coerce на активный.
4. Cron: persist pair == env → pack exact-lenses **этого** (активного) pack; dual только если флаг **активного** `pack.json` (`dual_civic_lenses`). Persist pair ≠ env (legacy rows) → skip + лог `cluster.skipped_schema_mismatch`, не membership. Unbound READY_FOR_PROFILE → civic as-is.

Pack-движок смотрит `structured_payload` по dotted path. Заголовок, ярлыки и civic geo в exact-lens не подставляются.

Чтобы нода кластеризовала pack-веткой, клиент шлёт binding **ровно** на `NODE_SCHEMA_*` этой ноды (например `"schema_id": "tallinn_civic"`, `"schema_version": "v1"`). Другой pack из склада сервер не примет на intake и не кластеризует.

### Dual (ярлыки и payload на одной story)

В `pack.json` можно поставить `"dual_civic_lenses": true`. Тогда bound story получает и pack exact-lens, и civic memberships с labels. Нет ключа или `false` — только exact, как у `legal_process` и `tallinn_civic` сейчас. Enum `ClusterLens` при этом не расширяют.

### Два контура: `exact_lenses` vs `node_clustering.civic`

На одной ноде два независимых контура кластеризации. Оба читаются из **активного** pack (`NODE_SCHEMA_*`), не из семантических `CLUSTER_*` в `.env`.

| Контур | Ключ в `pack.json` | Кто крутит | Что режет |
|--------|--------------------|------------|-----------|
| Pack exact | `exact_lenses[]` | `SchemaPackClusterEngine` | dotted path в `structured_payload` |
| Civic | `node_clustering.civic` | `ClusteringEngine` + civic `PromotionGatePolicy` + orchestrator min | `ClusterLens` (десять членов). Dual + unbound legacy |

Civic knobs (`min_size`, `readiness_threshold`, `active_lenses`, `primary_lens`, `geo_filter`, `geo_scope`, …) живут в `node_clustering.civic`. Factory и handlers берут их оттуда ([`service_factory.py`](../../../src/core/infrastructure/service_factory.py), [`handlers.py`](../../../src/core/api/handlers.py)). Семантические `CLUSTER_MIN_SIZE` / `CLUSTER_ACTIVE_LENSES` / `CLUSTER_GEO_SCOPE` в env **игнорируются** (нет полей в `AppConfig`). Dual-source «env wins» нет.

`geo_scope` вроде `settlement:tallinn` на `tallinn_civic` — данные зоны civic-gate, не URL `/tallinn`. Публичный API остаётся `/node/issues`.

Нет публичного `GET /schema-active`. Клиент не выбирает pack: intake `schema_binding` должен совпасть с `NODE_SCHEMA_*`.

### `geo_detail`, `geo_intake` и два пути кластеризации

Envelope sidecar `geo_detail` (рядом с `narrative` / `schema_binding`) несёт адресную глубину: street / house / house_range / houses плюс admin leaves. Это не второй binding и не HTTP geo-filter.

Блок pack `geo_intake` (SCHEMA-005) задаёт три режима:

| `mode` | Поведение на intake |
|--------|---------------------|
| `optional` | omit / пустой sidecar → 202, как раньше |
| `require_location_or_detail` | нужен `location_query` **или** непустой `geo_detail` |
| `require_detail` | нужен непустой `geo_detail` |

`merge=true` — клиентский `geo_detail` перекрывает miss провайдера / накладывает admin leaves. Address-only + miss провайдера **не** изобретает координаты.

`mirror_to_payload=true` пишет `structured_payload.geo.*` (district / settlement / region / country / street / house / house_range / houses) **до** pack validate. `tallinn_civic` зеркалит; `legal_process` / `mobility_observation` — нет.

Два независимых пути после persist:

| Путь | Что читает | Что **не** читает |
|------|------------|-------------------|
| Civic (`ClusteringEngine` + `geo_filter`) | только `admin_*` через `geo_filter_bucket` | street / house / houses / `structured_payload.geo.*` |
| Pack exact (`SchemaPackClusterEngine`) | dotted path в `structured_payload` (`geo.district`, опционально `geo.street`, …) | civic snapshot street как ключ; `ClusterLens` не расширяют |

Civic unlabeled / без admin остаётся `geo:unknown` / `geo:agnostic`. Pack missing path при `missing_value_policy=skip` не даёт membership. Enum `ClusterLens` = 10 членов. Публичного HTTP geo-filter нет.

### Три уровня geo (node / instance / precision)

Не смешивать:

| Уровень | Ключ | Кто enforce |
|---------|------|-------------|
| Node acceptance | `node_clustering.civic.geo_scope` | Gateway 422 (SSR-22) |
| Instance acceptance | `gpt_instance_territory` | GPT STOP (GPT-SSR-08); gateway **parse only** |
| Place precision | `geo_model` + `geo_detail.detail_level` | GPT emit; gateway persist → `Issue.geo.detail_level` |

Instance может быть **уже** node scope (район ⊂ Tallinn). Node gate **не** заменяет instance gate. `detail_level` ∈ `region` \| `settlement` \| `district` \| `street` \| `house` \| `house_range` \| `coordinates`. UC-G03: Issue.`geo` может нести `detail_level` / admin **без** lat/lon (без ложного pin). Street/house **не** на Issue projection.

Sibling GPT: [GPT-SSR-08](../../../../GPT%20UI/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GPT-SSR-08-geo-precision-instance-territory.md) · [GPT-SSR-06](../../../../GPT%20UI/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GPT-SSR-06-inbound-validation-post-ssr-delta.md) §6.

### Taxonomy dual contour (wire vs pack) — D-SSR-11

Два **разных** контура ярлыков. Документы **не** говорят, что wire envelope или GW-TAX-01 «переехали» в payload. Arch: [`architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md`](../../analysis/architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md).

| Concern | SSOT | Consumer |
|---------|------|----------|
| Per-axis labels on wire (**Contour1**) | OpenAPI `narrative.taxonomy` | Gateway intake → `story_labels` (GW-TAX-01). **SSR-32:** любая непустая ось (strip/lower); civic **skip** unmapped → SignalDimension |
| Pack vocabulary (**Contour2**) | **`taxonomy.json` in pack dir** | GPT normalizer + operator copy. **SSR-31:** `axes[]` = **node-defined** (не lockstep к 13); structural: unique / non-empty; `internal_axes` ⊆ axes; map keys ∈ axes |
| Payload validate | `payload.schema.json` | `SchemaRuntime.validate` |
| Content admission | GPT `inbound-validation.md` | GPT interview only |

`TAXONOMY_AXIS_VALUES` (13) = **tallinn / civic reference** set (seed + docs), **не** reject SSOT для Contour1/Contour2. Tallinn 13 = exemplar data.

Pack Contour2 (`taxonomy.json`) — словарь + `axis_to_signal_map` для copy-paste. Wire Contour1 остаётся на `narrative.taxonomy`.

### Authoring node taxonomy (operator setup)

1. Выбрать оси ноды (язык домена); tallinn 13 — только стартовая точка (trim/extend свободно).
2. Заполнить `canonical_keys` + `axis_to_signal_map` согласованно с `axes[]`.
3. В `pack.json` задать `"taxonomy_schema": "taxonomy.json"`, когда нужен Contour2.
4. Wire GPT taxonomy может использовать **те же** axis ids (после SSR-32 Contour1 open).
5. **Не** изобретать `ClusterLens` ids из имён осей.
6. Копировать tallinn taxonomy только как шаблон — не как закон «ровно 13».

Sibling conflict: [GPT-SSR-15](../../../../GPT%20UI/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GPT-SSR-15-taxonomy-meta-axis-lockstep.md) (lock Pack Builder meta to 13) must be **superseded/inverted** in a GPT wave — gateway D-SSR-11 wins. Gateway SSR-33 **only records** this handoff; it does **not** edit GPT files.

### Operator copy-paste (gateway → GPT, byte-identical)

Gateway `schema-packs/` = **SSOT**. GPT Instructions получают **byte-identical** копию трёх JSON. Gateway P3 **не** коммитит GPT JSON без review оператора ([GPT-SSR-05](../../../../GPT%20UI/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GPT-SSR-05-taxonomy-json-pack-copy-paste.md)).

1. **Edit SSOT** в gateway `schema-packs/<schema_id>/<schema_version>/` (taxonomy keys, `canonical_keys`, `axis_to_signal_map`).
2. **Copy three JSON byte-identical** в `GPT UI/instructions/schema-packs/<schema_id>/<schema_version>/`:
   - `pack.json`
   - `payload.schema.json`
   - `taxonomy.json`
3. **Verify checksum** (recommended):
   ```bash
   shasum -a 256 schema-packs/tallinn_civic/v1/{pack,payload.schema,taxonomy}.json \
     "GPT UI/instructions/schema-packs/tallinn_civic/v1/"*.json
   ```
4. **Update GPT** [`schema-packs/README.md`](../../../../GPT%20UI/instructions/schema-packs/README.md) active pair, если id/version сменились.
5. **Update GPT** `inbound-validation.md` §2 pointer на taxonomy JSON path (GPT-SSR-06 delta).
6. **Upload Custom GPT Instructions** — **без** Actions re-import, если OpenAPI wire не менялся.

**Handoff paths (tallinn example):**

| Gateway SSOT | GPT mirror path |
|--------------|-----------------|
| `doge-complaints-gateway/schema-packs/tallinn_civic/v1/pack.json` | `GPT UI/instructions/schema-packs/tallinn_civic/v1/pack.json` |
| same dir `payload.schema.json` | same |
| same dir `taxonomy.json` | same |

**Deprecation policy (document, don't delete GPT file):** GPT [`story-label-taxonomy.md`](../../../../GPT%20UI/instructions/story-label-taxonomy.md) — **redirect stub** (GPT-SSR-10). Enum SSOT = gateway pack + GPT mirror `taxonomy.json`. Process rules: GPT `ingest-validation.md` Label process rules. Archive: `GPT UI/instructions/archive/story-label-taxonomy.v0.2.3.md`.

Residual: mobility/legal taxonomy copy-paste — **tallinn first** (пока без `taxonomy_schema` на legal/mobility).

### Как сменить пороги / линзы / geo без `.env`

1. Править **активный** каталог: `schema-packs/<NODE_SCHEMA_ID>/<NODE_SCHEMA_VERSION>/pack.json` → блок `node_clustering.civic` (civic) или элемент `exact_lenses[]` (pack exact, включая его `readiness_policy` / `min_size`).
2. Рестарт процесса (`make serve` / redeploy). Boot резолвит pack заново; битый / missing `node_clustering` → `ConfigError`.
3. Не добавлять семантические `CLUSTER_*` в `.env` «поверх» pack — они не читаются.

Cron — **процесс**, не pack: `CLUSTER_CRON_ENABLED` / `CLUSTER_CRON_INTERVAL_S` остаются в env. Второй cron не нужен. Unbound legacy READY_FOR_PROFILE идёт в civic engine, собранный из того же активного `node_clustering.civic`.

### Карточка Issue

На `GET /node/issues` сырой payload **не** вываливается. Если в pack есть `card_fields` (список dotted path), на карточке появляется sidecar `schema_card` — именованные листья, не весь JSON ([`dto.py`](../../../src/core/projection/dto.py), [`card_fields.py`](../../../src/core/projection/card_fields.py)). Пути `forbidden` / `node_private` не попадают даже если их перечислили. Нет `card_fields` — обычная civic-форма карточки.

---

## Публичный API ноды

Канон (роуты в [`asgi_app.py`](../../../src/core/api/asgi_app.py)):

- `GET /node/issues` — список
- `GET /node/issues/{issue_id}` — одна карточка
- `POST /node/issues` — запись public-content (нужен service token)
- `GET /node/network-pulse` — Pulse L1, это **не** список issues
- `GET /node/emerging-signals` — Emerging L2, ключ `signals`, не issues

Старые `/tallinn/…` сняты: запрос на них даёт 404, без редиректа.

Liveness: `GET /health`. Готовность БД: `GET /ready` (`ready` или `degraded`).

Как прогнать это против живого `make serve` — раздел smoke ниже и [test-matrix](../testing/test-matrix-by-type-layer-mocks.md). Без uvicorn те же пути закрывают `tests/test_gw_ssr_15_scenarios.py` и `tests/test_req24_issues_read_api.py`.

---

## Как добавить свою модель

1. Каталог `schema-packs/<id>/<version>/`.
2. `pack.json` по таблице loader keys (README паков): `field_policy`, хотя бы одна exact-lens, `readiness_policy` с тремя knobs, обязательный `node_clustering.civic`. Числа порогов civic и exact — **в файле пака**, не в `.env` и не копировать civic default из Python.
3. `payload.schema.json` — схема `structured_payload`.
4. Опционально `taxonomy.json` + `"taxonomy_schema": "taxonomy.json"` в manifest — когда нужен civic Contour2 / GPT byte-identical copy-paste (см. §Operator copy-paste выше). Без ключа taxonomy не грузится.
5. Чтобы **эта** нода принимала intake на новый pack, выставить `NODE_SCHEMA_ID` / `NODE_SCHEMA_VERSION` на ту же пару и прислать `schema_binding` = env. Второй cron не нужен.

Не делать: новый член `ClusterLens`; колонки «под поле»; HTTP filter path; менять wire `narrative.taxonomy` / GW-TAX-01 «ради pack JSON».

Пример civic-as-pack (fixture [`gw_ssr_08_tallinn_civic_envelope.json`](../../../tests/fixtures/gw_ssr_08_tallinn_civic_envelope.json)):

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

Нарратив (title/description) обязателен и для pack: payload его не заменяет. Для `legal_process` в binding другие поля — см. `payload.schema.json` того пака.

---

## База

Pack не создаёт новые таблицы. На `stories` нужны шесть nullable колонок binding (`schema_id`, `bound_schema_version`, профили, `structured_payload`, `payload_hash`) — они уже в миграции [`20260828_1400_gw_ssr_02_stories_schema_binding.sql`](../../../supabase/migrations/20260828_1400_gw_ssr_02_stories_schema_binding.sql). Civic-строки живут с `NULL`.

- **in_memory** — ничего.
- **sqlite** — `ALTER` при `ensure_schema()`.
- **Hosted Supabase** — применить ту же миграцию, если колонок ещё нет; иначе omit-probe вырезает binding из SELECT/save (civic живёт, pack на host не пишется). После apply — рестарт процесса. Эти имена **не** кладут в `required_columns_ready`, иначе `/ready` станет 503 до миграции.

---

## Чего ещё нет

- Полный GPT operator manual rewrite — GPT-SSR-09 (здесь только checklist + paths). Без `schema_binding` == `NODE_SCHEMA_*` прод-intake из GPT получит 4xx.
- Overlay карточки в spa-app — sibling spa-16, не этот мануал. Пути SPA-клиентов уже `/node/…`.
- IDX (`story_dimensions`) и generic processors — черновики SSR-06/07.
- mobility/legal `taxonomy.json` seed — residual после tallinn.

---

## Проверка живого сервера

Поднять gateway (`make serve`, [server-env-quickstart](./server-env-quickstart.md)). В `.env.test`: `GATEWAY_URL=http://127.0.0.1:8000` (только localhost).

```bash
cd doge-complaints-gateway
.venv/bin/python -m pytest tests/smoke/test_local_server_smoke.py -q
```

Там: `/health`, `/ready`, список и карточка `/node/issues`, Pulse, Emerging, 404 на `/tallinn/issues`. Подробности запуска — [test-matrix](../testing/test-matrix-by-type-layer-mocks.md) и [06-testing-architecture](../bootstrap-infrastructure/06-testing-architecture.md) слой 6.
