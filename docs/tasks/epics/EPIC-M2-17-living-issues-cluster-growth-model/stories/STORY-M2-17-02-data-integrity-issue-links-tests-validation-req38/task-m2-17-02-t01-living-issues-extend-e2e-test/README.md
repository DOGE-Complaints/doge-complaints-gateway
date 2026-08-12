## Task workspace — `task-m2-17-02-t01-living-issues-extend-e2e-test`

- Story: [`../STORY-M2-17-02-data-integrity-issue-links-tests-validation-req38.md`](../STORY-M2-17-02-data-integrity-issue-links-tests-validation-req38.md)
- Decision Ref: [`../../../../../../requirements/38-data-integrity-issue-links-tests-validation.md`](../../../../../../requirements/38-data-integrity-issue-links-tests-validation.md) §1; G-10; audit GAP-38-01

---
**Приоритет:** P2  
**Сложность:** M  
**Оценка времени:** 2–3 ч  
**Статус:** ready  
**Wave:** `pkg-000017`  
---

## Task: tests — `test_living_issues_extend_existing.py` (living issues extend flow)

### Цель
Добавить e2e тест extend flow: 2 stories → promote → 3-я story → `process_story()` → issue обновлён (`story_count=3`, union `canonical_labels`).

### Факты из кода
1. REQ-38 §1 — файл `tests/test_living_issues_extend_existing.py` **не найден** (audit GAP-38-01).
2. [`tests/test_e2e_story_cluster_issue_pipeline.py`](../../../../../../../tests/test_e2e_story_cluster_issue_pipeline.py) L212 — `test_e2e_living_issue_two_batches_reuses_issue_and_appends_stories` использует `process_all_pending()`, не `process_story()`; 2→4 stories, без assert labels union.
3. [`promotion/service.py`](../../../../../../../src/core/promotion/service.py) — `extend_candidate()` реализован; [`issue_create.py`](../../../../../../../src/core/application/issue_create.py) — `_extend_issue` path.
4. [`cluster_orchestrator.py`](../../../../../../../src/core/application/cluster_orchestrator.py) — `process_story()` вызывает create/extend через `IssueCreateService`.

### Gap / Проблема
**GAP-38-01:** нет dedicated e2e файла по REQ-38; partial coverage не закрывает AC-2/AC-3 G-10.

### AC/DoD
- [ ] (P0) Создать `tests/test_living_issues_extend_existing.py`.
- [ ] (P0) Flow: 2 stories cluster+promote → add 3rd → `orchestrator.process_story(third_id)` → issue extended.
- [ ] (P0) Assert `len(promoted.story_ids) == 3` (или эквивалент story_count).
- [ ] (P0) Assert labels = union canonical_labels всех трёх stories.
- [ ] (P1) in_memory backend обязательно; sqlite — по возможности (REQ §1).
- [ ] (P2) supabase mock/stub — отдельный подтест или defer to T05 matrix.

### Где менять код
- **Создать:** [`tests/test_living_issues_extend_existing.py`](../../../../../../../tests/test_living_issues_extend_existing.py)

### Out of scope
- `issue_story_links` DDL (T02)
- Arweave validation (T04)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_living_issues_extend_existing.py -q --tb=short
```
