## Task workspace — `task-gw-l10n-01-t03-backfill-reproject-existing-issues`

- Story: [`../STORY-GW-L10N-01-projection-content-i18n-preservation.md`](../STORY-GW-L10N-01-projection-content-i18n-preservation.md)
- Depends on: T01 (reprojection uses updated extraction_policy)
- Decision Ref: backlog T03; operator choice = re-project script

---
**Priority:** P0  
**Complexity:** M  
**Estimate:** ~1.5 h  
**Status:** ready  
**Wave:** `pkg-000027`  
**Skill declared:** python-pro  
---

## Task: data — backfill re-project existing issues

### Цель
Бэкфилл: ре-проджектинг существующих issue, чтобы старые `payload_json` получили реальный контент из linked stories.

### Факты из кода
1. `doge_issues.payload_json` — JSON blob; DDL не меняется ([`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) `save_projection`).
2. `issue_story_links` связывает issue ↔ story ([`000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql) L139–145).
3. `StoryPromotionProjectionBridge.build_projection_input` — путь пересборки проекции ([`issue_create.py`](../../../../../../../src/core/application/issue_create.py) L126–159).
4. Существующего re-project скрипта в репозитории **нет** (grep `reproject`).

### AC/DoD
- [ ] (P0) One-off скрипт (e.g. `scripts/reproject_issue_i18n.py`) читает issue + story_ids → rebuild → `save_projection`.
- [ ] (P0) Dry-run режим (без записи) для оператора.
- [ ] (P1) Краткая инструкция в README таска или комментарий в скрипте: порядок запуска после T01/T02 deploy.
- [ ] (P1) Parent AC «Решён вопрос бэкфилла» — evidence в acceptance (count updated / sample payload).

### Где менять код
- Новый: `doge-complaints-gateway/scripts/reproject_issue_i18n.py` (или эквивалент)

### Out of scope
- Автоматический cron re-project
- GW-L10N-02 `original_locale` backfill

### Команды проверки
```bash
cd doge-complaints-gateway && python3 scripts/reproject_issue_i18n.py --help
```
