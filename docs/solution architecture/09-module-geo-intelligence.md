# 09. Module: Geo Intelligence

## Decision
Из legacy сохраняется только смысл геомодуля, но реализация переписывается под новый каркас.

## Responsibilities
- normalize location hint;
- resolve coordinates via provider chain;
- persist resolved geo profile;
- provide geo features for clustering and issue framing.

## Target design
- `GeoService` (domain facade).
- `GeoResolverAdapter` (OpenCage/Nominatim/provider chain).
- `GeoCacheRepository` (single canonical table, no schema split).
- `GeoPolicy` (timeouts, retry, quotas).

## Mandatory fixes vs legacy
- единая таблица кэша (no `location_directory` vs `address_directory` mismatch);
- write-back cache на успешный resolve;
- explicit timeout/retry/circuit breaker;
- structured logs instead of prints;
- graceful fallback when provider unavailable.

## Data outputs
- canonical coordinates;
- location confidence score;
- normalized city/region/country;
- geo tags for cluster lenses.
- **structured admin levels** (v2): `admin_district`, `admin_settlement`, `admin_region`, `admin_country`

## StoryGeoSnapshot — целевые поля (v2, решения интервью 2026-05-13)

```python
@dataclass(frozen=True)
class StoryGeoSnapshot:
    normalized_label: str
    latitude: float
    longitude: float
    confidence: float
    provider: str
    cluster_tags: tuple[str, ...] = ()
    # Новые структурированные admin-уровни:
    admin_district: str | None = None    # "Kalamaja", "Mustamäe"
    admin_settlement: str | None = None  # "Tallinn", "Narva"
    admin_region: str | None = None      # "Harju maakond", "Ida-Viru"
    admin_country: str | None = None     # "EE"
```

## Node Geo Scope и Geo Filter (новые env vars)

| Env var | Описание | Дефолт |
|---------|----------|--------|
| `CLUSTER_GEO_FILTER` | Уровень гранулярности кластеризации: `district\|settlement\|region\|country` | `country` |
| `CLUSTER_GEO_SCOPE` | Зона ответственности ноды. Формат: `<level>:<value>`, напр. `settlement:tallinn`. Истории вне скоупа отклоняются на intake (HTTP 4xx) | не задан (принимает всё) |

**Разница:** `GEO_FILTER` — как группировать в кластеры; `GEO_SCOPE` — какие истории принимать вообще.

**Демо-стабы** (текущее состояние): `_TallinnOpenCageStub` и `_NarvaNominatimStub` достаточны для `country`-уровня фильтрации; реальный маппинг admin-уровней — post-demo.

## Решения интервью (2026-05-13)
Подробно: REQ-35, `docs/analysis/gap-interview-decisions-2026-05-13.md` G-02
