## Task workspace — `task-m2-08-05-t08-audit-gap35-01-sqlite-admin-geo-roundtrip`

- Story: [`../STORY-M2-08-05-geo-scope-node-architecture-and-filtering.md`](../STORY-M2-08-05-geo-scope-node-architecture-and-filtering.md)
- Decision Ref: [`../../../../../../analysis/audit-req35-geo-scope-node-architecture-2026-05-16.md`](../../../../../../analysis/audit-req35-geo-scope-node-architecture-2026-05-16.md) §5 — **AUDIT-GAP-35-01** (не путать с implementation-wave GAP-35-01 в T01)

---
**Приоритет:** P1  
**Сложность:** S  
**Оценка времени:** ~15 мин  
**Статус:** ready  
**Wave:** `audit-req35-2026-05-16` (override-only; **не** в `pkg-000014`)  
**Supersedes / Superseded by:** complements T03, T07; does not reopen T01–T07 implementation wave  
---

## Task: tests — SQLite roundtrip asserts `geo_admin_*` on `StoryGeoSnapshot`

### Цель
Добавить asserting-тест, что все четыре admin-поля (`admin_district`, `admin_settlement`, `admin_region`, `admin_country`) переживают **SQLite** roundtrip через `SqliteStoryRepository` после `save_story` → `get_story`.

Закрыть **AUDIT-GAP-35-01** из внешнего аудита REQ-35 (2026-05-16): DB-слой реализован, но регрессия сериализации admin-полей сейчас не детектируется тестами.

### Почему это важно (риск)
Без SQLite-assert утверждение «persistence сохраняет admin-уровни» опирается только на код-ревью. Любой future refactor `db_sqlite.py` (порядок колонок, миграция, upsert) может сломать roundtrip незаметно — T03/T07 не покрывают этот путь end-to-end на SQLite.

### Out of scope
- Правки [`src/core/infrastructure/db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py) (аудит: запись/чтение уже корректны).
- Новый `pkg-*.yaml` или смена `gateway-active-package.current.yaml`.
- Supabase live roundtrip (опционально P2, отдельный таск).
- Расширение `test_intake_geo_scope_accepts_tallinn_location` post-202 assert (не заменяет прямой repo roundtrip).

### Факты из кода
1. [`tests/test_geo_candidate_persistence_roundtrip.py`](../../../../../../../tests/test_geo_candidate_persistence_roundtrip.py) L43–69 — `test_geo_snapshot_roundtrip_persists_on_story_record` использует `InMemoryStoryRepository()`; проверяются `normalized_label`, `provider`, `cluster_tags` — **не** `admin_*`.
2. [`tests/test_story_repository_lifecycle.py`](../../../../../../../tests/test_story_repository_lifecycle.py) L107–131 — `SqliteStoryRepository` roundtrip есть, но story **без** `geo` / admin-полей.
3. [`src/core/infrastructure/db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py) L37–40 — запись `geo.admin_district` … `geo.admin_country` в INSERT params.
4. [`src/core/infrastructure/db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py) L107–124 — чтение `geo_admin_*` из row в `StoryGeoSnapshot`.
5. Аудит §5 — рекомендуемое имя: `test_geo_admin_fields_survive_sqlite_roundtrip()`.

### Gap / Проблема
**AUDIT-GAP-35-01** (audit §5; ID коллидирует с закрытым implementation GAP-35-01 в T01): нет теста, верифицирующего SQLite persistence для `geo_admin_*`. In-memory-only roundtrip не считается закрытием этого gap.

### AC/DoD
- [x] (P0) Новый тест `test_geo_admin_fields_survive_sqlite_roundtrip` в `tests/test_geo_candidate_persistence_roundtrip.py` — green.
- [x] (P0) Используется `SqliteDatabase.from_url("sqlite:///:memory:")` + `db.ensure_schema()` + `SqliteStoryRepository`.
- [x] (P0) После `save_story` → `get_story`: `admin_settlement`, `admin_country`, `admin_district`, `admin_region` совпадают с исходным `StoryGeoSnapshot`.
- [x] (P1) `python3 -m pytest tests/test_geo_candidate_persistence_roundtrip.py -q` — green.
- [x] (P1) `python3 -m pytest -q` — без регрессий.

### Где менять код
- [`tests/test_geo_candidate_persistence_roundtrip.py`](../../../../../../../tests/test_geo_candidate_persistence_roundtrip.py) — добавить тест и импорт `SqliteStoryRepository`; helper для `StoryRecord` с geo (паттерн: [`tests/test_story_repository_lifecycle.py`](../../../../../../../tests/test_story_repository_lifecycle.py) + `tests/intake_v2_fixtures.make_story_record`).

### План выполнения
1. Импортировать `SqliteStoryRepository` рядом с существующим `SqliteDatabase`.
2. Собрать `StoryGeoSnapshot` с заполненными всеми четырьмя `admin_*` (значения как в audit-примере или Tallinn stub).
3. Построить минимальный `StoryRecord` с `geo=snapshot` (через `make_story_record` или локальный helper).
4. `repo.save_story(record)` → `loaded = repo.get_story(record.story_id)`.
5. Assert все admin-поля на `loaded.geo`.
6. Прогнать pytest (файл + полный suite).

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_geo_candidate_persistence_roundtrip.py::test_geo_admin_fields_survive_sqlite_roundtrip -q --tb=short
cd doge-complaints-gateway && python3 -m pytest tests/test_geo_candidate_persistence_roundtrip.py -q
cd doge-complaints-gateway && python3 -m pytest -q
```

### Исполнение (override)
Запуск только по метке оператора: `run_mode=story08_05_audit_req35_followup` — см. [`Gateway_builder.plan.md`](../../../../../../../.cursor/plans/Gateway_builder.plan.md).
