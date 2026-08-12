## Task workspace — `task-m2-08-05-t03-persistence-geo-snapshot-jsonb`

- Story: [`../STORY-M2-08-05-geo-scope-node-architecture-and-filtering.md`](../STORY-M2-08-05-geo-scope-node-architecture-and-filtering.md)
- Decision Ref: REQ-35 §4 (`infrastructure/db_*.py`)

## Task: implement — persist geo admin fields in story store

### Цель
Сохранять и читать новые admin-поля `StoryGeoSnapshot` в SQLite и Supabase adapters (колонки или JSONB), чтобы roundtrip intake → cluster не терял geo granularity.

### Факты из кода
1. [`src/core/infrastructure/db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py) L88, L96–103 — persist/read: `geo_normalized_label`, lat/lon, confidence, provider, `geo_cluster_tags_json` only.
2. [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) — аналогичный паттерн для geo snapshot (проверить `_story_record_from_*` при реализации).
3. REQ-35 §4 — cascade включает `infrastructure/db_*.py` для новых полей geo snapshot.

### Gap / Проблема
GAP-35-07: persistence layer не хранит admin-уровни → после reload story geo filter/scope ломается.

### AC/DoD
- [x] (P0) SQLite write/read roundtrip сохраняет все четыре `admin_*` поля (или JSON blob с ними).
- [x] (P0) Supabase adapter parity для тех же полей.
- [x] (P1) Миграция/SQL bootstrap только если требуется схемой (зафиксировать путь в acceptance).
- [x] (P1) `None` admin fields сериализуются без потери.

### Где менять код
- [`src/core/infrastructure/db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py)
- При необходимости: `supabase/migrations/*` или sqlite schema init

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_story_signal_store.py tests/test_db_backed_pipeline_e2e.py -q --tb=short -k geo
```
