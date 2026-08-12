## Task workspace — `task-m2-08-05-t01-story-geo-snapshot-admin-levels`

- Story: [`../STORY-M2-08-05-geo-scope-node-architecture-and-filtering.md`](../STORY-M2-08-05-geo-scope-node-architecture-and-filtering.md)
- Decision Ref: [`../../../../../../requirements/35-geo-scope-node-architecture-and-filtering.md`](../../../../../../requirements/35-geo-scope-node-architecture-and-filtering.md) §3.1; gap-interview G-02

## Task: implement — StoryGeoSnapshot admin hierarchy fields

### Цель
Добавить в `StoryGeoSnapshot` структурированные admin-поля (`admin_district`, `admin_settlement`, `admin_region`, `admin_country`), без которых `CLUSTER_GEO_FILTER` на уровнях district/settlement/region технически невозможен.

### Факты из кода
1. [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py) L27–36 — `StoryGeoSnapshot` содержит только `normalized_label`, coords, `confidence`, `provider`, `cluster_tags`.
2. REQ-35 §1 — `CLUSTER_GEO_FILTER` объявлен, но engine не фильтрует; корневая причина — нет admin-полей на snapshot.
3. G-02 ([`gap-interview-decisions-2026-05-13.md`](../../../../../../analysis/gap-interview-decisions-2026-05-13.md) L169–176) — зафиксированы четыре admin-поля с `None` default.

### Gap / Проблема
GAP-35-01: модель geo не хранит уровни district/settlement/region/country отдельно от `cluster_tags`.

### AC/DoD
- [x] (P0) `StoryGeoSnapshot` включает `admin_district`, `admin_settlement`, `admin_region`, `admin_country` (`str | None = None`).
- [x] (P0) Frozen dataclass остаётся backward-compatible для существующих call sites (новые поля optional).
- [x] (P1) `core/domain/__init__.py` re-exports без изменения public API surface.

### Где менять код
- [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -c "from core.domain import StoryGeoSnapshot; s=StoryGeoSnapshot('x',0,0,1,'p'); assert hasattr(s,'admin_settlement')"
```
