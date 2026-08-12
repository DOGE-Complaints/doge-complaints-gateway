## Task workspace — `task-m2-17-02-t03-supabase-linkage-lookup-semantics`

- Story: [`../STORY-M2-17-02-data-integrity-issue-links-tests-validation-req38.md`](../STORY-M2-17-02-data-integrity-issue-links-tests-validation-req38.md)
- Decision Ref: REQ-38 §2; G-11; audit GAP-38-02; **Variant A** (STORY conflict-scan)

---
**Приоритет:** P2  
**Сложность:** M  
**Оценка времени:** 1–2 ч  
**Статус:** ready  
**Wave:** `pkg-000017`  
---

## Task: implement — Supabase linkage lookup via `issue_story_links` (Variant A)

### Цель
Закрыть G-11 AC-3: `find_promoted_by_cluster_id()` корректно находит promoted issue через `issue_story_links`. **Не** перенаправлять `ClusterMembershipStore.save_membership()` в `issue_story_links` — N:M пишет `IssueStoryLinkStore.save_issue_story_links()` из `IssueCreateService`.

### Факты из кода
1. [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) ~L714 — `find_promoted_by_cluster_id()` запрашивает `issue_candidates` по `cluster_id` без JOIN `issue_story_links` (audit).
2. [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) ~L867 — `SupabaseClusterMembershipStore.save_membership()` → `/rest/v1/cluster_memberships`.
3. [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) ~L796 — `SupabaseIssueStoryLinkStore.save_issue_story_links()` → `issue_story_links`; caller [`issue_create.py`](../../../../../../../src/core/application/issue_create.py) L200–205.
4. TASK-LI-LINKS-DEDUP-01 (M2-17-01) — dedup contract Done; этот таск только lookup semantics.

### Gap / Проблема
**GAP-38-02:** AC-2 G-11 буквально требует `save_membership()` → `issue_story_links`; фактическая архитектура разделяет stores. **Решение Variant A:** уточнить traceability в REQ/story; реализовать JOIN lookup + regression tests для linkage store.

### AC/DoD
- [ ] (P0) `find_promoted_by_cluster_id()` (Supabase + parity backends where applicable) использует `issue_story_links` / consistent lookup path.
- [ ] (P0) `save_membership()` **не** дублирует запись в `issue_story_links`.
- [ ] (P0) Tests: Supabase mock and/or SQLite `test_process_linkage_sqlite.py` extended for lookup-after-link.
- [ ] (P1) При необходимости — минимальная правка REQ-38 §2.2 AC wording (Variant A) в requirements doc.

### Где менять код
- [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py)
- [`src/core/infrastructure/db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py) (if lookup parity needed)
- [`tests/test_process_linkage_sqlite.py`](../../../../../../../tests/test_process_linkage_sqlite.py) (или аналог)

### Out of scope
- DDL index (T02)
- Extend e2e (T01)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_process_linkage_sqlite.py tests/test_e2e_story_cluster_issue_pipeline.py -q --tb=short
```
