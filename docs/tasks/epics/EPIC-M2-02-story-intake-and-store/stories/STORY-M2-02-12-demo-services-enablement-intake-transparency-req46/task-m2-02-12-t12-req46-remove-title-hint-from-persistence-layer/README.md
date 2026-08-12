## Task workspace — `task-m2-02-12-t12-req46-remove-title-hint-from-persistence-layer`

- Story: [`../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md`](../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md)
- Depends on: T11 migration applied on hosted Supabase
- Decision Ref: REQ-46 §2.4 B/C

---
**Priority:** P0  
**Complexity:** M  
**Estimate:** ~1 h  
**Status:** ready  
**Wave:** override `run_mode=story02_12_req46_title_hint_purge_and_cleanup` (T12)  
---

## Task: implement — remove `narrative_title_hint*` from persistence and health

### Цель
Код не обращается к удалённым колонкам; `/health` `required_columns_ready()` не SELECTит `narrative_title_hint*`.

### Где менять
- [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py)
- [`src/core/infrastructure/db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- [`supabase/bootstrap/000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql)

### AC/DoD
- [ ] (P0) `rg narrative_title_hint src/` → no matches
- [ ] (P0) `save_story` / `_STORY_SELECT_FIELDS` / `_i18n_dict_from_supabase_row` без hint
- [ ] (P0) `required_columns_ready()` и `required_stories_narrative_extension_columns_ready()` без hint columns
- [ ] (P1) Hosted migration T11 applied before deploy

### Команды
```bash
cd doge-complaints-gateway && rg narrative_title_hint src/ && echo "must be empty"
```
