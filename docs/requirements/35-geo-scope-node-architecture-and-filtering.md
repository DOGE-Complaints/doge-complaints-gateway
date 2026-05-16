# REQ-35: Geo Scope, Node Architecture and Geo Filtering

**Статус:** Требует реализации (частично — `CLUSTER_GEO_FILTER` объявлен, не используется)  
**Источник:** Gap-интервью 2026-05-13, G-02  
**Приоритет:** P1  
**Связанные SA:** SA-09, SA-10, cluster-engine/03  

---

## 1. Контекст

`CLUSTER_GEO_FILTER` объявлен в `config/schema.py` и читается в `AppConfig`, но `cluster/engine.py` не содержит ни одного условия по гео — переменная игнорируется.

`StoryGeoSnapshot` хранит только `normalized_label` (строка) и `cluster_tags: tuple[str,...]` (теги вида `"place:tallinn"`). Структурированных полей по admin-уровням (район, населённый пункт, регион, страна) нет — без них `CLUSTER_GEO_FILTER=settlement` технически невозможен.

---

## 2. Нодовая архитектура (продуктовое видение)

### Публичные ноды
- Принимают intake от граждан
- Деплоят свою GPT-версию (`API_BASE_URL` этой ноды)
- Пример: Таллинская нода с `CLUSTER_GEO_SCOPE=settlement:tallinn`

### Приватные ноды (roadmap, не в этом REQ)
- Не принимают intake от граждан
- Читают токенизированные raw stories из web3
- Делают свою кластеризацию

---

## 3. Требования

### 3.1 `StoryGeoSnapshot` — структурированные admin-уровни

```python
@dataclass(frozen=True)
class StoryGeoSnapshot:
    normalized_label: str
    latitude: float
    longitude: float
    confidence: float
    provider: str
    cluster_tags: tuple[str, ...] = ()
    # Новые поля:
    admin_district: str | None = None    # "Kalamaja", "Mustamäe"
    admin_settlement: str | None = None  # "Tallinn", "Narva"
    admin_region: str | None = None      # "Harju maakond", "Ida-Viru"
    admin_country: str | None = None     # "EE"
```

Реальный маппинг от провайдера (OpenCage/Nominatim) → admin-уровни — post-demo. Для demo: обновить стабы (`_TallinnOpenCageStub`, `_NarvaNominatimStub`) с захардкоженными значениями новых полей.

### 3.2 `CLUSTER_GEO_FILTER` — реализовать логику в engine

| Значение | Уровень гранулярности | Пример (Эстония) |
|----------|-----------------------|-----------------|
| `district` | Район населённого пункта | Kalamaja, Mustamäe |
| `settlement` | Город/деревня | Tallinn, Narva |
| `region` | Регион | Harju maakond |
| `country` | Страна | EE |

**Дефолт:** `country` (если не задан — все истории из страны кластеризуются вместе).

Логика в `cluster/engine.py`: при формировании кластера истории фильтруются по соответствующему admin-полю `StoryGeoSnapshot`. Истории без гео-данных (`geo = None`) не фильтруются по гео — участвуют во всех кластерах (geo-агностичные проблемы).

### 3.3 `CLUSTER_GEO_SCOPE` — новый env var (зона ответственности ноды)

- **Формат:** `<level>:<value>`, напр. `settlement:tallinn`, `region:harju_maakond`
- **Дефолт:** не задан = нода принимает всё
- **Поведение при наличии:** история с геолокацией вне скоупа → **HTTP 4xx на intake**

**Разница от `CLUSTER_GEO_FILTER`:**
- `GEO_FILTER` = гранулярность объединения в кластеры
- `GEO_SCOPE` = какие истории нода принимает вообще (зона ответственности)

**Пример:** Таллинская нода: `CLUSTER_GEO_SCOPE=settlement:tallinn`, `CLUSTER_GEO_FILTER=district`. Принимает только таллинские истории, кластеризует по районам.

### 3.4 Rejection logic на intake

При `CLUSTER_GEO_SCOPE` задан:
1. Распарсить `<level>:<value>` из env var
2. Разрешить `location_query` из intake через GeoService
3. Сравнить соответствующий admin-уровень с `value`
4. Несовпадение → HTTP 422 с `code: GEO_SCOPE_MISMATCH`

Истории без `location_query` (geo-агностичные): допустимы всегда (не зависят от скоупа).

---

## 4. Cascade — файлы для изменения

| Файл | Изменение |
|------|-----------|
| `domain/contracts.py` | `StoryGeoSnapshot` новые поля |
| `geo/providers.py` | Обновить стабы Tallinn/Narva под новые поля |
| `cluster/engine.py` | Реализовать geo-фильтрацию по `CLUSTER_GEO_FILTER` |
| `api/handlers.py` | Geo scope rejection на intake |
| `config/schema.py` | `CLUSTER_GEO_SCOPE` новая env var + валидация формата |
| `example.env` | Документировать `CLUSTER_GEO_FILTER` и `CLUSTER_GEO_SCOPE` |
| `infrastructure/db_*.py` | Новые поля в JSONB geo snapshot |

---

## 5. Acceptance Criteria

- [ ] `StoryGeoSnapshot` содержит `admin_settlement`, `admin_country` (минимум) после geo resolve
- [ ] `CLUSTER_GEO_SCOPE=settlement:tallinn` → история с нарвской геолокацией → HTTP 422
- [ ] `CLUSTER_GEO_SCOPE=settlement:tallinn` → история без `location_query` → принята
- [ ] `CLUSTER_GEO_FILTER=settlement` → истории из Таллина и Нарвы попадают в разные кластеры
- [ ] `CLUSTER_GEO_FILTER=country` (дефолт) → все эстонские истории кластеризуются вместе
- [ ] Демо-стабы возвращают корректные admin-уровни

---

## 6. Не в scope этого REQ

- Реальная интеграция с OpenCage/Nominatim API (post-demo)
- Приватные ноды / web3 токенизация (roadmap)
- Нодовая аутентификация / криптоверификация типа ноды
