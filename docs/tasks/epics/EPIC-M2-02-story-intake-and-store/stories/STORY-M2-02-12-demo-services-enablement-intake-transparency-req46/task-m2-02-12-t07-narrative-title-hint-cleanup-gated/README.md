## Task workspace — `task-m2-02-12-t07-narrative-title-hint-cleanup-gated`

- Story: [`../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md`](../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md)
- Decision Ref: [`../../../../../../requirements/46-demo-services-enablement-and-response-transparency.md`](../../../../../../requirements/46-demo-services-enablement-and-response-transparency.md) §2.4

---
**Priority:** P2  
**Complexity:** M  
**Estimate:** ~1.5 h  
**Status:** superseded  
**Wave:** `pkg-000026` → override T11–T13 (`run_mode=story02_12_req46_title_hint_purge_and_cleanup`)  
---

**Superseded (2026-06-02):** Gate returned **192** test stories with non-null hint. Work moved to:
- T11 [`../task-m2-02-12-t11-req46-legacy-hint-stories-purge-and-drop-columns-migration/README.md`](../task-m2-02-12-t11-req46-legacy-hint-stories-purge-and-drop-columns-migration/README.md)
- T12 [`../task-m2-02-12-t12-req46-remove-title-hint-from-persistence-layer/README.md`](../task-m2-02-12-t12-req46-remove-title-hint-from-persistence-layer/README.md)
- T13 [`../task-m2-02-12-t13-req46-title-hint-cleanup-tests-bootstrap-parity/README.md`](../task-m2-02-12-t13-req46-title-hint-cleanup-tests-bootstrap-parity/README.md)

## Task: implement — DROP `narrative_title_hint*` columns (conditional) — archived spec

### Gate (обязательно перед стартом)
Исходный контракт: выполнять **только** если SQL из REQ §2.4 возвращает `0`:

```sql
SELECT COUNT(*) FROM stories
WHERE narrative_title_hint IS NOT NULL
   OR narrative_title_hint_et IS NOT NULL
   OR narrative_title_hint_ru IS NOT NULL
   OR narrative_title_hint_en IS NOT NULL;
```

Если count > 0 → **stop**; task status `blocked` / `deferred` в индексе; story может закрыться без T07.

### Цель
Удалить dead legacy columns и код paths, которые пишут `None` на каждый save ([`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) L464–467).

### Факты из кода
1. [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) — `_STORY_SELECT_FIELDS`, `save_story()` null writes, `_i18n_dict_from_supabase_row` fallbacks.
2. [`db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py) — schema + CRUD references.
3. REQ §2.4 — migration `ALTER TABLE ... DROP COLUMN`.

### AC/DoD (REQ-46 §4 Title hint)
- [ ] (P0) Gate SQL documented in acceptance evidence (screenshot or query output).
- [ ] (P0) `supabase/migrations/YYYYMMDD_narrative_title_hint_cleanup.sql` applied.
- [ ] (P0) `db_supabase.py` / `db_sqlite.py` — no `narrative_title_hint*` references.
- [x] (P0) `required_columns_ready()` / column lists — **N/A (verified 2026-06-02):** `narrative_title_hint*` отсутствует в readiness-чеках [`dependencies.py`](../../../../../../../src/core/api/dependencies.py) (audit G4); работа не требуется при cleanup.
- [ ] (P1) Tests green after cleanup.

### Out of scope
- REQ-47.
- Non-null title_hint data migration (if gate fails).

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_supabase_bootstrap_schema.py tests/test_story_repository.py
```
