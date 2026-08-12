## Task workspace — `task-m2-17-02-t02-issue-story-links-story-index`

- Story: [`../STORY-M2-17-02-data-integrity-issue-links-tests-validation-req38.md`](../STORY-M2-17-02-data-integrity-issue-links-tests-validation-req38.md)
- Decision Ref: REQ-38 §2; G-11; audit GAP-38-03

---
**Приоритет:** P2  
**Сложность:** S  
**Оценка времени:** ~30 min  
**Статус:** ready  
**Wave:** `pkg-000017`  
---

## Task: data — `idx_issue_story_links_story` index

### Цель
Добавить индекс по `story_id` на `issue_story_links` в bootstrap и отдельную migration (REQ-38 DDL).

### Факты из кода
1. [`supabase/bootstrap/000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql) L135–142 — таблица `issue_story_links` есть; индекс `idx_issue_story_links_issue` на `issue_id` только.
2. [`supabase/migrations/20260427_1645_process_linkage.sql`](../../../../../../../supabase/migrations/20260427_1645_process_linkage.sql) L25–32 — та же схема, без `idx_issue_story_links_story`.
3. Audit GAP-38-03 — AC-1 G-11 (таблица) ✅; индекс по `story_id` ❌.

### Gap / Проблема
**GAP-38-03:** отсутствует `CREATE INDEX idx_issue_story_links_story ON issue_story_links(story_id)`.

### AC/DoD
- [ ] (P0) `create index if not exists idx_issue_story_links_story on public.issue_story_links(story_id)` в `000_full_init.sql`.
- [ ] (P0) Новая migration `supabase/migrations/20260517_*_issue_story_links_story_idx.sql`.
- [ ] (P1) Schema/bootstrap tests still green.

### Где менять код
- [`supabase/bootstrap/000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql)
- **Создать:** `supabase/migrations/20260517_*_issue_story_links_story_idx.sql`

### Out of scope
- `find_promoted_by_cluster_id` JOIN (T03)
- FK на `issues` / `stories` (audit: table names `doge_issues` — не в scope REQ)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_bootstrap_schema.py tests/test_process_linkage_sqlite.py -q -k issue_story 2>/dev/null || python3 -m pytest -q -k bootstrap
```
