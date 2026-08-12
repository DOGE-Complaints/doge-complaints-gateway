## Task workspace — `task-m2-02-12-t11-req46-legacy-hint-stories-purge-and-drop-columns-migration`

- Story: [`../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md`](../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md)
- Decision Ref: [`../../../../../../analysis/req46-t07-narrative-title-hint-gate-unblock-runbook-2026-06-02.md`](../../../../../../analysis/req46-t07-narrative-title-hint-gate-unblock-runbook-2026-06-02.md); [`../../../../../../requirements/46-demo-services-enablement-and-response-transparency.md`](../../../../../../requirements/46-demo-services-enablement-and-response-transparency.md) §2.4
- Supersedes gate branch: T07 blocked at COUNT=192 → operator confirmed test-only data

---
**Priority:** P0  
**Complexity:** M  
**Estimate:** ~1 h (+ operator apply on hosted)  
**Status:** ready  
**Wave:** override `run_mode=story02_12_req46_title_hint_purge_and_cleanup` (T11)  
---

## Task: data — purge legacy-hint stories + derived issues + DROP columns

### Цель
Один SQL-файл в `supabase/migrations/`: удалить 192 test stories с непустым `narrative_title_hint*`, связанные `doge_issues` (политика **any_link**), process-linkage rows; затем DROP четырёх legacy-колонок.

### Факты из схемы
1. [`supabase/bootstrap/000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql) L139–145 — `issue_story_links` **без** FK на `stories` → ручной DELETE до `DELETE FROM stories`.
2. L63–67, L69–76, L148–163 — `ON DELETE CASCADE` от `stories`: `idempotency_keys`, `story_embeddings`, `story_signals`, `cluster_memberships`.
3. L88–104 — `doge_issues` / `doge_issue_embeddings`; удалять issues с любой ссылкой на purge-set story.

### AC/DoD
- [ ] (P0) `supabase/migrations/20260603_1200_req46_title_hint_test_purge_and_column_drop.sql` в репозитории.
- [ ] (P0) Миграция в `BEGIN`/`COMMIT`; preflight SELECT закомментированы; post-purge COUNT hint = 0; `ALTER TABLE stories DROP COLUMN …`.
- [ ] (P0) Оператор: applied on hosted Supabase; evidence в [`acceptance-verification-m2-02-12-t11.md`](./acceptance-verification-m2-02-12-t11.md) (pre: 192 stories).
- [ ] (P1) T12/T13 **не** деплоить до успешного apply этой миграции.

### Out of scope
- Python persistence (T12); tests (T13); `pkg-000026` YAML.

### Команды проверки (оператор, после apply)
```sql
SELECT COUNT(*) FROM stories
WHERE narrative_title_hint IS NOT NULL
   OR narrative_title_hint_et IS NOT NULL
   OR narrative_title_hint_ru IS NOT NULL
   OR narrative_title_hint_en IS NOT NULL;
-- Expected: ERROR (columns dropped) OR 0 before DROP only
```
