# 29. Living Issues — живые issues с нарастающим кластером

Дата: 2026-05-05  
Статус: решение принято — готово к задачированию  
Зависит от: `28-clustering-cron-scheduler.md` (batch processing), `27-doge-issue-domain-rename.md` (DOGEIssue)  
Связано: `07-dynamic-clusters-product-model.md`, `25-clustering-engine-target-state-spec.md`

---

## 1. Контекст и проблема

В текущей модели каждый раз, когда кластер (`cluster_id`) набирает достаточно историй, создаётся **новый issue**. Истории из предыдущего батча уже в статусе `CLUSTERED` и исключены. Это порождает несколько issues для одной и той же темы в разное время — множество отдельных снимков вместо живой картины.

**Целевая модель:** один `cluster_id` → один активный `DOGEIssue`. При появлении новой волны matching историй они **прикрепляются к существующему issue**, а не создают новый.

---

## 2. Ключевой факт из кода

`find_promoted_by_cluster_id(cluster_id)` уже реализован во **всех трёх backends** (`InMemoryIssueCandidateStore`, `SqliteIssueCandidateStore`, `SupabaseIssueCandidateStore`) — в таблице `issue_candidates`.

Метод есть в Protocol `IssueCandidateStore`:
```python
def find_promoted_by_cluster_id(self, cluster_id: str) -> IssueCandidateRecord | None:
    """Return a promoted candidate for cluster_id, if any."""
```

**Инфраструктурный gap:** `IssueCreateService.create_issue()` не вызывает этот метод — не проверяет, существует ли уже активный issue для данного `cluster_id`.

---

## 3. Целевая логика `IssueCreateService.create_issue()`

Сейчас (snapshot model):
```
create_issue(command)
  └── create_candidate → promote → project → save
```

После (living model):
```
create_issue(command)
  ├── find_promoted_by_cluster_id(command.cluster_id)
  │     ├── None → CREATE PATH (текущая логика)
  │     └── existing → EXTEND PATH (новое)
  │
  └── EXTEND PATH:
        ├── attach new stories to existing issue
        ├── update readiness_score
        ├── rebuild projection from updated story set
        └── save updated projection to doge_issues
```

---

## 4. Новый метод: `extend_candidate()` на `IssuePromotionService`

**Файл:** `src/core/promotion/service.py`

```python
def extend_candidate(
    self,
    candidate_id: str,
    *,
    additional_story_ids: tuple[str, ...],
    new_readiness_score: int,
) -> IssueCandidateRecord:
    """
    Attach new stories to an already-PROMOTED candidate.
    Only valid for PROMOTED status.
    """
```

**Логика:**
1. Загрузить `current` по `candidate_id`
2. Проверить `current.status == PROMOTED` — если нет, бросить `PromotionStateError`
3. Вычислить `merged_story_ids = tuple(sorted(set(current.story_ids) | set(additional_story_ids)))` — дедупликация
4. Создать новый `IssueCandidateRecord` с обновлёнными `story_ids` и `readiness_score`
5. Сохранить через `self.candidates.save()`
6. Добавить запись в `audit_log` с `actor="system"`, `rationale="cluster_growth_extend"`, `related_story_ids=additional_story_ids`
7. Вернуть обновлённый record

`IssueCandidateRecord` — `frozen=True` dataclass, обновление происходит через создание нового экземпляра (паттерн уже применяется во всех методах `IssuePromotionService`).

---

## 5. Extend path в `IssueCreateService`

**Файл:** `src/core/application/issue_create.py`

```python
def create_issue(self, command: IssueCreateCommand) -> IssueCreateResult:
    # ... validation ...

    existing = self.promotion_service.candidates.find_promoted_by_cluster_id(
        command.cluster_id
    )

    if existing is not None:
        return self._extend_issue(existing, command)
    else:
        return self._create_issue(command)   # текущая логика вынести в приватный метод
```

**`_extend_issue(existing, command)`:**

1. Вычислить новые stories = `set(command.story_ids) - set(existing.story_ids)` — только действительно новые
2. Если новых историй нет → вернуть `IssueCreateResult` для `existing` без изменений (idempotency)
3. Вызвать `self.promotion_service.extend_candidate(existing.candidate_id, additional_story_ids=new_stories, new_readiness_score=command.readiness_score)`
4. Перестроить проекцию: `bridge.build_projection_input(issue_id=existing.candidate_id, promoted_title=updated.title, story_ids=updated.story_ids)`
5. Вызвать `projection_service.project(projection_input)` → обновлённый `DOGEIssue`
6. Сохранить через `issue_projection_store.save_projection(...)` — тот же `issue_id`, перезапишет существующую запись в `doge_issues`
7. Сохранить `issue_story_link_store.save_issue_story_links(...)` только для новых stories
8. Вернуть `IssueCreateResult` с `issue_id=existing.candidate_id`, `status=PROMOTED`

---

## 6. Что меняется в DB при extend

| Таблица | Действие | Ключ |
|---------|----------|------|
| `issue_candidates` | UPDATE: `story_ids_json`, `readiness_score` | `candidate_id` |
| `review_audit_log` | INSERT: новая запись `cluster_growth_extend` | |
| `doge_issues` | UPDATE: `payload_json`, `updated_at`, `policy_version` | `issue_id` |
| `doge_issue_embeddings` | UPDATE: новый вектор от обновлённой проекции | `issue_id` |
| `issue_story_links` | INSERT: только новые stories | `issue_id, story_id` |
| `stories` | UPDATE: статус новых stories → `CLUSTERED` | `story_id` |

---

## 7. Требования к store-методам

### 7.1 `IssueProjectionStore` — добавить `update_projection`

Текущий `save_projection()` может работать как upsert (INSERT OR REPLACE в SQLite, upsert в Supabase). Нужно проверить и задокументировать: **`save_projection()` должен быть idempotent upsert** — если запись с `issue_id` уже существует, перезаписать `payload_json`, `policy_version`, `updated_at`.

Если текущая реализация не upsert — исправить, не добавляя новый метод.

### 7.2 `IssueProjectionEmbeddingStore` — аналогично upsert

### 7.3 `IssueStoryLinkStore` — должен игнорировать дубли

При `save_issue_story_links()` для уже существующей пары `(issue_id, story_id)` не должна возникать ошибка. `INSERT OR IGNORE` в SQLite, `ON CONFLICT DO NOTHING` в Supabase.

### 7.4 `IssueCandidateStore.update()` — может потребоваться

SQLite и Supabase реализации `save()` должны поддерживать UPDATE существующей записи (не только INSERT). Проверить текущую реализацию.

---

## 8. Инварианты living issues

**INV-LI-01 — Один активный issue на cluster_id:** для любого `cluster_id` существует максимум один `IssueCandidateRecord` со статусом `PROMOTED`.

**INV-LI-02 — Дедупликация story_ids:** `story_ids` в `IssueCandidateRecord` не содержит дублей. `set()` при merge гарантирует это.

**INV-LI-03 — CLUSTERED непрерывен:** story, прикреплённая к issue (как при create, так и при extend), всегда помечается `CLUSTERED` — вне зависимости от пути.

**INV-LI-04 — Проекция согласована со story_ids:** `DOGEIssue` всегда содержит aggregate_text от актуального набора `story_ids`. После каждого extend — проекция перестраивается.

**INV-LI-05 — Audit trail полон:** каждый extend фиксируется в `review_audit_log` с указанием добавленных `story_ids`.

---

## 9. Взаимодействие с cron (doc 28)

`process_all_pending()` вызывает `issue_create_service.create_issue()` — поведение прозрачное: create или extend решается внутри сервиса. Оркестратор не знает о living/snapshot различии.

Важный сценарий: если две волны историй приходят до первого cron-тика, `process_all_pending()` загрузит их вместе как один большой батч. В этом случае create path создаёт issue сразу с обеими волнами. Extend path нужен только если предыдущий батч уже был обработан.

---

## 10. Порядок реализации

| # | Задача | Файлы |
|---|--------|-------|
| 1 | Проверить и при необходимости исправить upsert-поведение `save_projection()` и `save_issue_story_links()` | `db_sqlite.py`, `db_supabase.py`, `repositories.py` |
| 2 | Реализовать `extend_candidate()` на `IssuePromotionService` | `promotion/service.py` |
| 3 | Добавить unit-тесты `extend_candidate()`: happy path, двойной extend (дедупликация), invalid status | `tests/test_promotion_service.py` |
| 4 | Вынести create logic из `create_issue()` в `_create_issue()`, добавить `_extend_issue()` | `application/issue_create.py` |
| 5 | Добавить тест: create path (existing=None), extend path (existing found), idempotent extend (нет новых stories) | `tests/test_issue_create.py` |
| 6 | Проверить SQLite/Supabase `find_promoted_by_cluster_id` — корректно ли работает | `db_sqlite.py`, `db_supabase.py` |
| 7 | E2E тест: два батча с одним cluster_id → один issue с объединёнными story_ids | e2e |

---

## 11. Acceptance criteria

**AC-29-1:** Два последовательных `process_all_pending()` с историями одного кластера создают **один** issue (не два).

**AC-29-2:** После второго прогона issue содержит story_ids из обоих батчей.

**AC-29-3:** `review_audit_log` содержит запись `cluster_growth_extend` для каждого extend-события.

**AC-29-4:** `DOGEIssue` (проекция) после extend перестроена: `description` отражает aggregate text всех story_ids.

**AC-29-5:** `extend_candidate()` с уже имеющимися story_ids (нет новых) не создаёт дублей и не меняет score без причины.

**AC-29-6:** Все stories обоих батчей имеют статус `CLUSTERED` после обработки.
