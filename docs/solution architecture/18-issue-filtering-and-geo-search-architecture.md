# SA-18: Issue Filtering & Geo Search Architecture

**Дата:** 2026-05-17  
**Источник:** Gap-анализ REQ-24 + аудит кода; geo-интервью 2026-05-13 (SA-09)  
**Метод:** Factual code audit only — только факты из кода  
**Область:** `GET /tallinn/issues` — расширенная фильтрация + geo-поиск

---

## 1. Текущее состояние — факты из кода

### 1.1 Projection payload: что хранится

`DOGEIssue.to_public_dict()` (`src/core/projection/dto.py`) — единственный источник данных для `payload_json` в `doge_issues`:

| Поле | Тип | Nullable |
|------|-----|----------|
| `id` | string | нет |
| `status` | string | нет |
| `type` | string | нет |
| `labels` | string[] | нет (может быть `[]`) |
| `title` | `{et, ru, en}` | нет |
| `summary` | `{et, ru, en}` | нет |
| `description` | `{et, ru, en}` | нет |
| `institution` | string | да |
| `created_at` | ISO8601 string | да |
| `arweave_txid` | string | да |
| `image_txid` | string | да |
| `image_hash` | string | да |

**Geo-полей нет ни одного.** `ProjectionInput` (`src/core/projection/input.py`) также не содержит geo-полей.

### 1.2 Таблица хранения (`doge_issues`, SQLite / `tallinn_issues_projections`, Supabase)

```sql
CREATE TABLE IF NOT EXISTS doge_issues (
    issue_id        TEXT PRIMARY KEY,
    status          TEXT NOT NULL,          -- ← единственный SQL-индексируемый фильтр
    payload_json    TEXT NOT NULL,
    policy_version  TEXT NOT NULL,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
)
```

**Geo-колонок нет.** `created_at` хранится как TEXT (ISO8601), не как TIMESTAMPTZ.

### 1.3 Текущие фильтры (REQ-24)

| Параметр | Реализация | Уровень |
|----------|-----------|---------|
| `status` | WHERE status IN (...) | SQL — эффективно |
| `type` | `payload.get("type") != issue_type` | Python post-fetch |
| `labels` | `any(l in payload["labels"] for l in labels)` | Python post-fetch |

Все три — post-fetch в Python для InMemory и SQLite. В Supabase `status` — SQL, `type` — jsonb, `labels` — Python.

### 1.4 Geo-данные: где они есть

`StoryGeoSnapshot` (`src/core/domain/contracts.py:28`) — привязан к `StoryRecord.geo`:

```python
@dataclass(frozen=True)
class StoryGeoSnapshot:
    normalized_label: str
    latitude: float          # WGS84
    longitude: float         # WGS84
    confidence: float
    provider: str
    cluster_tags: tuple[str, ...] = ()
    admin_district: str | None = None    # "Kalamaja", "Põhja-Tallinn"
    admin_settlement: str | None = None  # "Tallinn", "Narva"
    admin_region: str | None = None      # "Harju maakond"
    admin_country: str | None = None     # "EE"
```

**Geo есть на story-уровне. На issue-уровне — нет.**

### 1.5 Почтовый индекс

`StoryGeoSnapshot` не содержит `postal_code`. Поле отсутствует как в модели, так и в Nominatim/OpenCage stub-адаптерах (`src/core/infrastructure/providers.py`, `src/core/geo/providers.py`). Postal code — gap: требует обогащения при geocoding.

---

## 2. Gap: geo не персистируется в projection

```
Story intake → GeoService.resolve() → StoryRecord.geo (StoryGeoSnapshot)
                                              ↓
                              [GEO PROPAGATION GAP]
                                              ↓
           StoryPromotionProjectionBridge.build_projection_input()
                — читает StoryRecord, но geo игнорируется
                         ↓
              ProjectionInput (нет geo полей)
                         ↓
              DOGEIssue.to_public_dict() (нет geo)
                         ↓
              doge_issues.payload_json (нет geo)
```

**Вывод:** для любой geo-фильтрации issue-уровня необходимо сначала закрыть этот propagation gap.

---

## 3. Принцип: какое geo брать для issue

Issue агрегирует несколько stories. Каждая story может иметь свои координаты.

**Решение: доминантная история (`select_dominant_story()`).**

`src/core/projection/extraction_policy.py:26` — функция уже существует и используется для title/type/labels. Geo берётся с той же истории. Рациональность: доминантная история — самая сигнальная (наивысший `alpha_score`), т.е. наиболее характерная для кластера. Это же geo будет использоваться как «местоположение проблемы».

**Альтернатива: центроид координат всех историй** — точнее для географически распределённых кластеров, но:
- добавляет сложность (нужен centroid-расчёт)
- `admin_district`/`admin_settlement` у центроида нет — нужен обратный geocoding
- не нужен для MVP Таллинна, где stories в пределах одного района

**MVP-решение:** `dominant_story.geo` → issue geo. Отмечено как `TODO: centroid v2`.

---

## 4. Архитектура расширенной фильтрации

### 4.1 Полная матрица фильтров

#### Категориальные фильтры (строки/перечисления)

| Параметр API | Источник | Уровень фильтрации | Оператор |
|-------------|---------|-------------------|---------|
| `status` | колонка `status` | SQL | OR (multi-value) |
| `type` | `payload_json->>'type'` | SQL (Supabase) / Python (SQLite) | exact match |
| `labels` | `payload_json->'labels'` | jsonb `?|` (Supabase) / Python (SQLite) | OR (any match) |
| `institution` | `payload_json->>'institution'` | Python post-fetch | exact match |

#### Временны́е фильтры

| Параметр API | Источник | Уровень фильтрации |
|-------------|---------|-------------------|
| `created_after` | колонка `created_at` (TEXT ISO8601) | Python сравнение строк (лексикографически корректно для ISO8601) |
| `created_before` | колонка `created_at` | Python post-fetch |

#### Geo-фильтры: режим A — Пространственный (bbox)

Задаётся прямоугольником координат — эквивалент «зума» на карте Google Maps.

| Параметр API | Тип | Описание |
|-------------|-----|---------|
| `geo_lat_min` | float | Нижняя граница широты (south) |
| `geo_lat_max` | float | Верхняя граница широты (north) |
| `geo_lon_min` | float | Левая граница долготы (west) |
| `geo_lon_max` | float | Правая граница долготы (east) |

Логика: `geo_lat_min ≤ issue.geo_lat ≤ geo_lat_max AND geo_lon_min ≤ issue.geo_lon ≤ geo_lon_max`

Issues без geo → исключаются из bbox-выборки (geo = NULL → не попадают в bbox).

Пример — центр Таллинна (bbox примерный):
```
?geo_lat_min=59.43&geo_lat_max=59.46&geo_lon_min=24.72&geo_lon_max=24.77
```

#### Geo-фильтры: режим B — Идентификаторы адреса

Фильтрация по структурированным admin-уровням geocoder-а.

| Параметр API | Соответствие в StoryGeoSnapshot | Тип |
|-------------|-------------------------------|-----|
| `geo_district` | `admin_district` | string (case-insensitive нормализованный) |
| `geo_settlement` | `admin_settlement` | string |
| `geo_region` | `admin_region` | string |
| `geo_country` | `admin_country` | string (ISO 3166-1 alpha-2 рекомендован) |
| `geo_postal_code` | `postal_code` (gap — см. §5.3) | string |

Логика: все указанные параметры — AND. Несколько значений одного параметра — OR.

Пример — все issues в Каламая или Пыхья-Таллинн:
```
?geo_district=Kalamaja&geo_district=Põhja-Tallinn
```

#### Комбинирование режимов

Оба режима могут использоваться одновременно. AND-семантика: issue должен удовлетворить bbox И все address-параметры.

```
?geo_lat_min=59.43&geo_lat_max=59.46&geo_lon_min=24.72&geo_lon_max=24.77&geo_district=Kesklinn
```

Практический сценарий: SPA задаёт bbox через Google Maps, дополнительно уточняя районом.

---

## 5. Стратегия хранения geo в projection

### 5.1 Два варианта

**Вариант I — geo inline в `payload_json`**
- Добавить geo-поля в `DOGEIssue` и `ProjectionInput`
- Они автоматически попадают в `payload_json`
- Фильтрация — Python post-fetch (как сейчас для `type`)
- Для Supabase — jsonb operators на `payload_json->>'geo_lat'` и т.д.
- **Плюс:** минимальный schema impact, нет новых колонок
- **Минус:** bbox-фильтрация в Python (full table scan)

**Вариант II — отдельные geo-колонки в таблице**
- Добавить колонки: `geo_lat REAL`, `geo_lon REAL`, `geo_district TEXT`, `geo_settlement TEXT`, `geo_region TEXT`, `geo_country TEXT`
- Индексировать для быстрого bbox-запроса
- **Плюс:** SQL-side bbox фильтрация, пространственный индекс возможен
- **Минус:** migration, schema drift между SQLite и Supabase

**Решение MVP:** Вариант I (inline в payload_json) — проще, достаточно для масштаба demo (сотни, не миллионы записей). Вариант II — путь для production при реальной нагрузке.

### 5.2 Geo-поля в payload_json

Добавить в `DOGEIssue` / `ProjectionInput` / `ProjectionInput`:

```python
# ProjectionInput — новые поля
geo_lat: float | None = None
geo_lon: float | None = None
geo_normalized_label: str | None = None
geo_admin_district: str | None = None
geo_admin_settlement: str | None = None
geo_admin_region: str | None = None
geo_admin_country: str | None = None
```

`DOGEIssue.to_public_dict()` — добавить `geo` sub-object:

```json
{
  "id": "...",
  "geo": {
    "lat": 59.437,
    "lon": 24.753,
    "label": "Kalamaja, Tallinn",
    "district": "Põhja-Tallinn",
    "settlement": "Tallinn",
    "region": "Harju maakond",
    "country": "EE"
  }
}
```

`geo` присутствует только если у доминантной истории есть `StoryGeoSnapshot`. Если geo = None → поле отсутствует в dict (не `null`, а отсутствует) для совместимости с SPA.

### 5.3 Почтовый индекс (postal_code)

**Текущее состояние:** `postal_code` отсутствует в `StoryGeoSnapshot`, в Nominatim/OpenCage stub-адаптерах, в DDL всех таблиц.

**Подход:**
1. Добавить `postal_code: str | None = None` в `StoryGeoSnapshot`
2. Populate из geocoder response при реальном resolve (post-demo)
3. Demo-stub: `postal_code = None` → фильтр `geo_postal_code` возвращает 0 результатов (ожидаемо для demo)

`geo_postal_code` фильтр в API — принимается, но без `postal_code` в данных даёт пустой результат. Не ошибка.

---

## 6. Propagation pipeline: как geo попадает в projection

### 6.1 Текущий flow (без geo)

```
StoryPromotionProjectionBridge.build_projection_input()
  → select_dominant_story(cluster_stories) → dominant_story
  → extraction_policy.build_draft(dominant_story, cluster_stories)
     → canonical_issue_type_from_story(dominant_story)
     → canonical_labels_from_cluster(cluster_stories)
  → build_projection_input_from_draft(issue_id, draft)
     → ProjectionInput(issue_id, status, issue_type, labels, title, summary, description)
     ← НЕТ geo
```

### 6.2 Целевой flow (с geo)

```
StoryPromotionProjectionBridge.build_projection_input()
  → select_dominant_story(cluster_stories) → dominant_story
  → geo_snapshot = dominant_story.geo  ← НОВОЕ
  → extraction_policy.build_draft(...)
  → build_projection_input_from_draft(issue_id, draft, geo=geo_snapshot)  ← НОВОЕ
     → ProjectionInput(
         ...,
         geo_lat=geo_snapshot.latitude if geo_snapshot else None,
         geo_lon=geo_snapshot.longitude if geo_snapshot else None,
         geo_admin_district=geo_snapshot.admin_district if geo_snapshot else None,
         ...
       )
```

### 6.3 Файлы изменений (propagation gap)

| Файл | Изменение |
|------|----------|
| `src/core/projection/input.py` | Добавить 7 geo-полей в `ProjectionInput` |
| `src/core/projection/dto.py` | Добавить `geo: dict \| None` в `DOGEIssue`; `to_public_dict()` — serialize |
| `src/core/projection/mapper.py` | `project_distinct_issue()` — передать geo из `data` |
| `src/core/application/issue_create.py` | `StoryPromotionProjectionBridge.build_projection_input()` — извлечь `dominant_story.geo` → передать в `build_projection_input_from_draft()` |
| `src/core/projection/extraction_policy.py` | `build_projection_input_from_draft()` — принять geo и пробросить |

---

## 7. Filter engine: реализация

### 7.1 Protocol расширения `IssueProjectionReadStore`

```python
class IssueProjectionReadStore(Protocol):
    def list_projections(
        self,
        *,
        status: list[str] | None = None,
        issue_type: str | None = None,
        labels: list[str] | None = None,
        institution: str | None = None,
        created_after: str | None = None,   # ISO8601
        created_before: str | None = None,  # ISO8601
        geo_lat_min: float | None = None,
        geo_lat_max: float | None = None,
        geo_lon_min: float | None = None,
        geo_lon_max: float | None = None,
        geo_district: list[str] | None = None,
        geo_settlement: list[str] | None = None,
        geo_region: list[str] | None = None,
        geo_country: list[str] | None = None,
        geo_postal_code: list[str] | None = None,
    ) -> list[dict[str, object]]: ...
```

### 7.2 Порядок применения фильтров (InMemory / SQLite)

```
1. status → SQL WHERE (существующий)
2. created_after / created_before → SQL WHERE (лексикографическое ISO8601)
3. Python post-fetch loop:
   a. type
   b. labels (OR)
   c. institution
   d. geo_district (OR, normalize_geo_token)
   e. geo_settlement (OR)
   f. geo_region (OR)
   g. geo_country (OR)
   h. geo_postal_code (OR)
   i. bbox: geo_lat_min/max + geo_lon_min/max (AND)
```

### 7.3 Нормализация geo-строк при фильтрации

Использовать `normalize_geo_token()` из `src/core/geo/scope.py:15`:

```python
def normalize_geo_token(value: str | None) -> str:
    if value is None:
        return ""
    return "".join(ch for ch in value.strip().lower() if ch.isalnum())
```

Фильтр `?geo_district=Põhja-Tallinn` → `phjatallinn` должен совпасть с `geo.admin_district = "Põhja-Tallinn"` → `phjatallinn`.

### 7.4 Null-safety для geo-фильтров

Issue без geo (`"geo"` отсутствует в payload) → при любом активном geo-фильтре **исключается** из результата. Это ожидаемое поведение: если у issue нет геолокации, он не может удовлетворить пространственному условию.

---

## 8. API-контракт: query parameters

```
GET /tallinn/issues?
  status=NEW&status=PUBLISHED         — OR
  &type=INCIDENT                       — exact
  &labels=infrastructure&labels=waste  — OR
  &institution=Tallinna Kommunaalamet  — exact (case-sensitive)
  &created_after=2026-01-01T00:00:00Z  — ISO8601
  &created_before=2026-12-31T23:59:59Z
  &geo_lat_min=59.43&geo_lat_max=59.46
  &geo_lon_min=24.72&geo_lon_max=24.77
  &geo_district=Kalamaja
  &geo_settlement=Tallinn
  &geo_region=Harju+maakond
  &geo_country=EE
  &geo_postal_code=10411
```

Все параметры опциональны. Пустые — игнорируются (не `?geo_district=` → то же, что отсутствие параметра).

### 8.1 Response — geo в payload issue

```json
{
  "data": {
    "issues": [
      {
        "id": "issue:abc123",
        "status": "PUBLISHED",
        "type": "INCIDENT",
        "labels": ["infrastructure", "safety"],
        "title": {"et": "Katki tänav", "ru": "Сломанная дорога", "en": "Broken road"},
        "summary": {"et": "...", "ru": "...", "en": "..."},
        "description": {"et": "...", "ru": "...", "en": "..."},
        "institution": null,
        "created_at": "2026-05-17T10:00:00Z",
        "geo": {
          "lat": 59.4372,
          "lon": 24.7453,
          "label": "Kalamaja, Tallinn",
          "district": "Põhja-Tallinn",
          "settlement": "Tallinn",
          "region": "Harju maakond",
          "country": "EE"
        }
      }
    ]
  },
  "trace_id": "uuid"
}
```

Issue без geo:
```json
{
  "id": "issue:xyz999",
  ...
  (поле "geo" отсутствует)
}
```

---

## 9. Cascade — полный список файлов изменений

### Phase 1: Geo propagation (prerequisite)

| Файл | Изменение |
|------|----------|
| `src/core/projection/input.py` | + `geo_lat`, `geo_lon`, `geo_normalized_label`, `geo_admin_district`, `geo_admin_settlement`, `geo_admin_region`, `geo_admin_country` |
| `src/core/projection/dto.py` | + `geo: dict[str, object] \| None`; update `to_public_dict()` |
| `src/core/projection/mapper.py` | `project_distinct_issue()` — маппинг geo из input |
| `src/core/projection/extraction_policy.py` | `build_projection_input_from_draft()` — принять + пробросить geo |
| `src/core/application/issue_create.py` | `StoryPromotionProjectionBridge.build_projection_input()` — извлечь dominant_story.geo |

### Phase 2: Filter extension

| Файл | Изменение |
|------|----------|
| `src/core/application/issue_create.py` | `IssueProjectionReadStore` Protocol — добавить все geo параметры в сигнатуру |
| `src/core/infrastructure/repositories.py` | `InMemoryIssueProjectionStore.list_projections()` — все фильтры |
| `src/core/infrastructure/db_sqlite.py` | `SqliteIssueProjectionStore.list_projections()` — все фильтры |
| `src/core/infrastructure/db_supabase.py` | `SupabaseIssueProjectionStore.list_projections()` — все фильтры |
| `src/core/api/handlers.py` | `handle_tallinn_issues_list()` — принять все параметры |
| `src/core/api/asgi_app.py` | Route `GET /tallinn/issues` — добавить все Query параметры |

### Phase 3: Postal code enrichment (post-demo)

| Файл | Изменение |
|------|----------|
| `src/core/domain/contracts.py` | `StoryGeoSnapshot` + `postal_code: str \| None` |
| `src/core/geo/providers.py` | Populate postal_code из geocoder response |
| `src/core/infrastructure/db_sqlite.py` | `ALTER TABLE stories ADD COLUMN geo_postal_code TEXT` |
| `src/core/infrastructure/db_supabase.py` | Аналогично |
| `supabase/migrations/` | Migration добавить колонку |

---

## 10. Acceptance Criteria

### AC-1: Geo поле присутствует в payload issues с геолокацией

```
POST /intake/stories  с location_query
→ GET /tallinn/issues
→ issue.geo содержит { lat, lon, district, settlement, region, country }
```

### AC-2: Bbox-фильтр возвращает только issues в зоне

```
GET /tallinn/issues?geo_lat_min=59.43&geo_lat_max=59.46&geo_lon_min=24.72&geo_lon_max=24.77
→ все issues в ответе имеют geo.lat и geo.lon внутри bbox
→ issues вне bbox — не возвращаются
```

### AC-3: Issues без geo исключаются при активном geo-фильтре

```
GET /tallinn/issues?geo_district=Kesklinn
→ issues без поля "geo" в ответе отсутствуют
```

### AC-4: Address-фильтр по district (case-insensitive, нормализованный)

```
GET /tallinn/issues?geo_district=põhja-tallinn
→ возвращает issues с geo.district == "Põhja-Tallinn" (нормализация через normalize_geo_token)
```

### AC-5: Множественные значения geo_district — OR

```
GET /tallinn/issues?geo_district=Kalamaja&geo_district=Kesklinn
→ issues из обоих районов
```

### AC-6: Комбинирование bbox + district — AND

```
GET /tallinn/issues?geo_lat_min=...&geo_lat_max=...&geo_lon_min=...&geo_lon_max=...&geo_district=Kesklinn
→ только issues, удовлетворяющие ОБОИМ условиям
```

### AC-7: created_after / created_before

```
GET /tallinn/issues?created_after=2026-05-01T00:00:00Z&created_before=2026-05-31T23:59:59Z
→ только issues в мае 2026
```

### AC-8: Пустые geo-параметры игнорируются

```
GET /tallinn/issues?geo_district=
→ эквивалентно GET /tallinn/issues (без фильтра)
```

---

## 11. Что НЕ включает этот SA

| Что | Почему |
|-----|--------|
| Пространственный индекс (PostGIS, R-tree) | Не нужен при demo-масштабе |
| Центроид geo по всем story | Сложность без user value на MVP |
| Geo-фильтр для `POST /tallinn/issues` (поиск в admin) | Не применимо к write |
| Fuzzy text search по названиям улиц | Client-side в SPA |
| Reverse geocoding при centroid | Phase 2 |
| `geo_postal_code` наполнение данными | Phase 3 (geocoder enrichment) |
| Поддержка GeoJSON / Polygon boundaries | Beyond MVP |
