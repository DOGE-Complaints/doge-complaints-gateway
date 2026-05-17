# REQ-40: Geo Propagation to Issue Projection

**Дата:** 2026-05-17  
**Статус:** Реализовано (STORY-M2-06-05, 2026-05-17)  
**Источник:** SA-18 §2, §3, §5, §6, §9 Phase 1 + Phase 3  
**Приоритет:** P2 (blocker для REQ-24 geo-фильтрации)  
**Блокирует:** REQ-24 §4 (geo-фильтры), AC-14 – AC-19  
**Связанные SA:** SA-18 (`18-issue-filtering-and-geo-search-architecture.md`), SA-09 (`09-module-geo-intelligence.md`)

---

## 1. Контекст и gap

### 1.1 Что уже работает

`GeoService.resolve_for_story()` (`src/core/geo/service.py`) разрешает geo по `location_query` и возвращает `StoryGeoSnapshot`. Snapshot сохраняется в `StoryRecord.geo` (поле `geo: StoryGeoSnapshot | None` в `src/core/domain/contracts.py:61`).

`StoryGeoSnapshot` содержит:
```python
normalized_label: str         # "Kalamaja, Tallinn"
latitude: float               # WGS84
longitude: float              # WGS84
confidence: float
provider: str
cluster_tags: tuple[str, ...] = ()
admin_district: str | None    # "Põhja-Tallinn", "Kesklinn"
admin_settlement: str | None  # "Tallinn", "Narva"
admin_region: str | None      # "Harju maakond"
admin_country: str | None     # "EE"
```

### 1.2 Propagation gap

Geo существует на story-уровне, но **не попадает в issue projection**:

```
Story intake → GeoService.resolve() → StoryRecord.geo (StoryGeoSnapshot)
                                              ↓
                              [GEO PROPAGATION GAP]
                                              ↓
           StoryPromotionProjectionBridge.build_projection_input()
                — читает StoryRecord, но geo игнорируется
                         ↓
              ProjectionInput (нет geo полей)  ← src/core/projection/input.py
                         ↓
              DOGEIssue.to_public_dict() (нет geo) ← src/core/projection/dto.py
                         ↓
              doge_issues.payload_json (нет geo)
```

**Следствие:** любой geo-фильтр на `GET /tallinn/issues` невозможен до закрытия этого gap.

---

## 2. Принцип выбора geo для issue

Issue агрегирует несколько stories; у каждой может быть своё `StoryGeoSnapshot`.

**MVP-решение: geo доминантной истории.**

`select_dominant_story()` (`src/core/projection/extraction_policy.py:26`) уже используется для выбора title/type/labels. Та же история используется как источник geo. Рациональность: доминантная история — наиболее сигнальная (наивысший `alpha_score` из `src/core/cluster/alpha.py`), т.е. наиболее характерная для кластера.

**Альтернатива: центроид координат всех stories** — более точен для географически распределённых кластеров, но:
- требует centroid-расчёта
- `admin_district`/`admin_settlement` центроида нет — нужен обратный geocoding
- за пределами MVP Таллинна (stories в пределах одного района)

> `TODO v2: centroid geo` — при выходе за пределы одного settlement.

Если у доминантной истории `geo = None` → issue публикуется без geo-поля в payload (не ошибка; issue без геолокации исключается из geo-фильтров на стороне read).

---

## 3. Стратегия хранения

### 3.1 Варианты

**Вариант I — geo inline в `payload_json`**

Geo-поля добавляются в `DOGEIssue` и автоматически попадают в `payload_json` (уже хранится как TEXT/jsonb в `doge_issues`). Фильтрация — Python post-fetch; для Supabase — jsonb operators.

- **Плюс:** никаких изменений в DDL таблицы `doge_issues`; нет SQL миграции; нет schema drift между SQLite и Supabase
- **Минус:** bbox-фильтрация в Python (full table scan); нет пространственного индекса

**Вариант II — отдельные geo-колонки**

Добавить колонки: `geo_lat REAL`, `geo_lon REAL`, `geo_district TEXT` и т.д.; индексировать.

- **Плюс:** SQL-side bbox фильтрация, пространственный индекс
- **Минус:** migration обязательна; schema drift; сложнее поддерживать три backend

**Выбранный вариант:** Вариант I — inline в `payload_json`. Достаточно для demo-масштаба (сотни записей). Вариант II — путь для production при реальной нагрузке.

### 3.2 Geo sub-object в `payload_json`

`DOGEIssue.to_public_dict()` → вложенный объект `"geo"`:

```json
{
  "id": "issue:abc123",
  "status": "PUBLISHED",
  "type": "INCIDENT",
  "labels": ["infrastructure"],
  "title": { "et": "...", "ru": "...", "en": "..." },
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
```

Issue без geo (`dominant_story.geo is None`) — поле `"geo"` **отсутствует** в dict (не `null`; отсутствует). Это позволяет SPA надёжно проверять наличие: `if issue.geo`.

---

## 4. Изменения в коде (Phase 1)

### 4.1 `ProjectionInput` — добавить geo-поля

Файл: `src/core/projection/input.py`

```python
@dataclass(frozen=True)
class ProjectionInput:
    issue_id: str
    status: str
    issue_type: str
    labels: tuple[str, ...]
    title: I18nText
    summary: I18nText | None
    description: I18nText
    institution: str | None = None
    created_at: str | None = None
    arweave_txid: str | None = None
    image_txid: str | None = None
    image_hash: str | None = None
    # Новые geo-поля (REQ-40):
    geo_lat: float | None = None
    geo_lon: float | None = None
    geo_normalized_label: str | None = None
    geo_admin_district: str | None = None
    geo_admin_settlement: str | None = None
    geo_admin_region: str | None = None
    geo_admin_country: str | None = None
```

### 4.2 `DOGEIssue` — добавить geo + serialize

Файл: `src/core/projection/dto.py`

```python
@dataclass(frozen=True)
class DOGEIssue:
    # ... существующие поля ...
    geo: dict[str, object] | None = None  # новое

    def to_public_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = { ... }  # существующие поля
        if self.geo is not None:
            out["geo"] = self.geo       # только если geo присутствует
        return out
```

### 4.3 `project_distinct_issue()` — маппинг geo

Файл: `src/core/projection/mapper.py`

```python
def project_distinct_issue(data: ProjectionInput) -> DOGEIssue:
    ...
    geo: dict[str, object] | None = None
    if data.geo_lat is not None and data.geo_lon is not None:
        geo = {
            "lat": data.geo_lat,
            "lon": data.geo_lon,
        }
        if data.geo_normalized_label:
            geo["label"] = data.geo_normalized_label
        if data.geo_admin_district:
            geo["district"] = data.geo_admin_district
        if data.geo_admin_settlement:
            geo["settlement"] = data.geo_admin_settlement
        if data.geo_admin_region:
            geo["region"] = data.geo_admin_region
        if data.geo_admin_country:
            geo["country"] = data.geo_admin_country
    return DOGEIssue(
        ...,
        geo=geo,
    )
```

### 4.4 `build_projection_input_from_draft()` — принять geo

Файл: `src/core/projection/extraction_policy.py`

```python
def build_projection_input_from_draft(
    *,
    issue_id: str,
    draft: StoryProjectionDraft,
    geo_snapshot: StoryGeoSnapshot | None = None,  # новый параметр
) -> ProjectionInput:
    return ProjectionInput(
        ...,
        geo_lat=geo_snapshot.latitude if geo_snapshot else None,
        geo_lon=geo_snapshot.longitude if geo_snapshot else None,
        geo_normalized_label=geo_snapshot.normalized_label if geo_snapshot else None,
        geo_admin_district=geo_snapshot.admin_district if geo_snapshot else None,
        geo_admin_settlement=geo_snapshot.admin_settlement if geo_snapshot else None,
        geo_admin_region=geo_snapshot.admin_region if geo_snapshot else None,
        geo_admin_country=geo_snapshot.admin_country if geo_snapshot else None,
    )
```

### 4.5 `StoryPromotionProjectionBridge.build_projection_input()` — извлечь geo доминанты

Файл: `src/core/application/issue_create.py`

```python
def build_projection_input(
    self,
    *,
    issue_id: str,
    promoted_title: str,
    story_ids: tuple[str, ...],
) -> ProjectionInput:
    ...
    dominant_story = select_dominant_story(cluster_stories)
    geo_snapshot = dominant_story.geo  # ← НОВОЕ: geo из доминантной истории
    ...
    return build_projection_input_from_draft(
        issue_id=issue_id,
        draft=draft,
        geo_snapshot=geo_snapshot,   # ← НОВОЕ
    )
```

---

## 5. Cascade — файлы изменений (Phase 1)

| # | Файл | Изменение |
|---|------|-----------|
| 1 | `src/core/projection/input.py` | + 7 geo-полей (`geo_lat`, `geo_lon`, `geo_normalized_label`, `geo_admin_district`, `geo_admin_settlement`, `geo_admin_region`, `geo_admin_country`) |
| 2 | `src/core/projection/dto.py` | + `geo: dict[str, object] \| None`; update `to_public_dict()` |
| 3 | `src/core/projection/mapper.py` | `project_distinct_issue()` — geo маппинг из input → geo dict |
| 4 | `src/core/projection/extraction_policy.py` | `build_projection_input_from_draft()` + параметр `geo_snapshot` |
| 5 | `src/core/application/issue_create.py` | `StoryPromotionProjectionBridge.build_projection_input()` — извлечь `dominant_story.geo` → передать |

---

## 6. Почтовый индекс (Phase 3, post-demo)

**Текущее состояние:** `postal_code` отсутствует в `StoryGeoSnapshot` (`src/core/domain/contracts.py`), в stub-адаптерах (`src/core/infrastructure/providers.py`), в DDL всех таблиц.

**Целевое состояние (Phase 3):**

| Файл | Изменение |
|------|-----------|
| `src/core/domain/contracts.py` | `StoryGeoSnapshot` + `postal_code: str \| None = None` |
| `src/core/geo/providers.py` | Populate `postal_code` из geocoder response (OpenCage: `components.postcode`) |
| `src/core/infrastructure/db_sqlite.py` | `ALTER TABLE stories ADD COLUMN geo_postal_code TEXT` |
| `src/core/infrastructure/db_supabase.py` | Аналогично |
| `supabase/migrations/` | Migration добавить колонку |
| `src/core/projection/input.py` | + `geo_postal_code: str \| None` |
| `src/core/projection/dto.py` | + в `geo` sub-object: `"postal_code"` |

Demo-stub: `postal_code = None` → `geo_postal_code`-фильтр (REQ-24) возвращает 0 результатов — ожидаемо, не ошибка.

---

## 7. Acceptance Criteria

### AC-1: geo присутствует в payload issue c геолокацией — [x]

```
POST /intake/stories  с location_query="Kalamaja, Tallinn"
→ story создана с geo != None
→ GET /tallinn/issues
→ issue.geo == { "lat": ..., "lon": ..., "district": ..., "settlement": "Tallinn", ... }
```

### AC-2: issue без geo — поле отсутствует (не null) — [x]

```
POST /intake/stories  без location_query
→ GET /tallinn/issues
→ в объекте issue нет ключа "geo" (not "geo": null, а ключа нет вообще)
```

### AC-3: geo в payload = geo доминантной истории кластера — [x]

```
# cluster с 2 историями: s1 (geo=Kalamaja), s2 (geo=Mustamäe)
# s1 — доминантная (более высокий alpha_score)
→ issue.geo.district == доминантная история's admin_district
```

### AC-4: обратная совместимость — существующие issues без geo не ломаются — [x]

```
# Issues, созданные до REQ-40, не имеют geo в payload
GET /tallinn/issues
→ 200; issue без geo поля — возвращается корректно без geo
```

---

## 8. Out of scope (этого REQ)

| Что | Почему |
|-----|--------|
| Geo-фильтры на `GET /tallinn/issues` | REQ-24 (зависит от этого REQ) |
| Centroid geo по всем story кластера | Phase 2 post-demo |
| Postal code наполнение данными | Phase 3 post-demo |
| Пространственный индекс (PostGIS, R-tree) | не нужен при demo-масштабе |
| Reverse geocoding при centroid | Phase 2 |
