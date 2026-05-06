# Аудит кода против requirement 29 — Living Issues Cluster Growth Model

**Дата:** 2026-05-06  
**Scope:** `src/core/promotion/service.py`, `src/core/application/issue_create.py`, `src/core/application/cluster_orchestrator.py`, `src/core/promotion/repositories.py`, `src/core/infrastructure/db_sqlite.py`, `src/core/infrastructure/db_supabase.py`  
**Тесты:** `tests/test_issue_promotion_service.py`, `tests/test_issue_create_service.py`, `tests/test_e2e_story_cluster_issue_pipeline.py`  
**Методология:** Верификация каждого утверждения прямо из кода; никаких предположений.

---

## 1. Результат прогона тестов

```
.venv/bin/python -m pytest tests/test_issue_promotion_service.py \
  tests/test_issue_create_service.py \
  tests/test_e2e_story_cluster_issue_pipeline.py -q
16 passed in 0.67s
```

---

## 2. AC-матрица — фактический статус

| AC | Формулировка req29 | Код | Тест | Статус |
|----|--------------------|-----|------|--------|
| AC-29-1 | Два `process_all_pending()` с историями одного кластера создают **один** issue | `issue_create.py:130-135`: `find_promoted_by_cluster_id()` → extend path | `test_e2e_living_issue_two_batches_reuses_issue_and_appends_stories`: `second_issue_ids == [issue_id]` | ✅ |
| AC-29-2 | После второго прогона issue содержит story_ids из обоих батчей | `_extend_issue():217`: `extend_candidate(additional_story_ids=...)` → merged set union | `assert set(promoted.story_ids) == {"s1","s2","s3","s4"}` | ✅ |
| AC-29-3 | `review_audit_log` содержит запись `cluster_growth_extend` | `service.py:166-176`: `audit_log.append(rationale="cluster_growth_extend", related_story_ids=additional_story_ids)` | `assert [entry.rationale for entry in audit][-1] == "cluster_growth_extend"` | ✅ |
| AC-29-4 | `DOGEIssue` после extend перестроена с aggregate_text всех story_ids | `_extend_issue():222-228`: `bridge.build_projection_input(story_ids=updated.story_ids)` — полный набор merged IDs | Тест проверяет только `issue_id == second.issue_id`, контент проекции **не проверяется** | ⚠️ partial |
| AC-29-5 | `extend_candidate()` без новых stories не создаёт дублей, не меняет score | `_extend_issue():202-215`: early return без вызова `extend_candidate()` | `test_idempotent_extend`: `readiness_score == 70` (не 99), `len(audit) == 1` | ✅ |
| AC-29-6 | Все stories обоих батчей имеют статус `CLUSTERED` | `cluster_orchestrator.py:237-241`: цикл `update_lifecycle_status(CLUSTERED)` для всех `member_story_ids` | E2E тест **не проверяет** `lifecycle_status` историй из обоих батчей | ⚠️ partial |

---

## 3. Инварианты req29 — фактический статус

| Инвариант | Определение | Реализация | Статус |
|-----------|-------------|------------|--------|
| INV-LI-01 | Один активный PROMOTED issue на cluster_id | `create_issue()` сначала вызывает `find_promoted_by_cluster_id()` — если нашли, идёт extend, не create | ✅ |
| INV-LI-02 | Нет дублей в `story_ids` | `extend_candidate():154-156`: `tuple(sorted(set(current.story_ids).union(set(additional_story_ids))))` | ✅ |
| INV-LI-03 | Story при extend всегда `CLUSTERED` | Orchestrator строка 237-241 охватывает оба пути | ✅ (логически), тест ⚠️ |
| INV-LI-04 | Проекция согласована с актуальным `story_ids` | `_extend_issue():222-228`: проекция перестраивается от `updated.story_ids` | ✅ impl, тест ⚠️ |
| INV-LI-05 | Audit trail полон — каждый extend фиксируется | `service.py:166-176` пишет запись при каждом вызове `extend_candidate()` | ✅ |

---

## 4. Верифицированные компоненты (факты из кода)

### 4.1 `IssuePromotionService.extend_candidate()` — `service.py:144-176`

✅ Реализован. Проверки:
- Валидирует `current.status == PROMOTED` через `_require_transition` — бросает `PromotionStateError` иначе
- `merged_story_ids = tuple(sorted(set(current.story_ids).union(set(additional_story_ids))))` — корректная дедупликация
- Создаёт новый `IssueCandidateRecord` с тем же `candidate_id` и статусом `PROMOTED`
- Сохраняет через `candidates.save()` → upsert по `candidate_id` во всех трёх бэкендах
- Пишет в `audit_log`: `actor="system"`, `rationale="cluster_growth_extend"`, `related_story_ids=additional_story_ids` (только новые — корректно)

### 4.2 `IssueCreateService.create_issue()` / `_extend_issue()` — `issue_create.py:122-261`

✅ Реализован create/extend split. Проверки:
- `find_promoted_by_cluster_id()` вызывается до любых side-effects
- `_extend_issue()` idempotent case (строки 202-215): early return без `extend_candidate()`, без записи в audit, без изменений в DB — score не перезаписывается
- `_extend_issue()` extend case: `additional_story_ids = requested - existing` (только новые), `save_issue_story_links` получает только `additional_story_ids` (не весь merged набор — это корректно, деду из DO NOTHING в store)
- Проекция перестраивается от `updated.story_ids` (полный набор после merge)

### 4.3 `find_promoted_by_cluster_id()` — все три бэкенда

| Backend | Реализация | Статус |
|---------|------------|--------|
| InMemory | `repositories.py:56-61`: итерация по dict, фильтр по `cluster_id` и `status == PROMOTED` | ✅ |
| SQLite | `db_sqlite.py:546-565`: `WHERE cluster_id = ? AND status = ? LIMIT 1` | ✅ |
| Supabase | `db_supabase.py:508-529`: GET с фильтрами `cluster_id` и `status=eq.PROMOTED`, `limit=1` | ✅ |

### 4.4 `save_issue_story_links()` — идемпотентность

| Backend | Семантика | Статус |
|---------|-----------|--------|
| SQLite | `db_sqlite.py:636-643`: `ON CONFLICT(issue_id, story_id) DO NOTHING` | ✅ соответствует req29 §7.3 |
| Supabase | `db_supabase.py:609-615`: `prefer="resolution=ignore-duplicates,return=minimal"` | ✅ |

### 4.5 `IssueCandidateStore.save()` — update semantics (для `extend_candidate`)

| Backend | Семантика | Статус |
|---------|-----------|--------|
| InMemory | `repositories.py:43-45`: `self._records[record.candidate_id] = record` — overwrite | ✅ |
| SQLite | `db_sqlite.py:500-523`: `ON CONFLICT(candidate_id) DO UPDATE SET status, story_ids_json, readiness_score, title, updated_at` | ✅ |
| Supabase | `db_supabase.py:466-470`: POST с `on_conflict: candidate_id` | ✅ |

### 4.6 `save_projection()` — idempotent upsert

SQLite `db_sqlite.py:436-457`: `ON CONFLICT(issue_id) DO UPDATE SET status, payload_json, policy_version, updated_at` ✅

Supabase — требует отдельной проверки (не показан фрагмент выше, но паттерн аналогичен).

### 4.7 CLUSTERED status update в extend path

`cluster_orchestrator.py:237-241`:
```python
for member_id in member_story_ids:
    self.story_repository.update_lifecycle_status(member_id, StoryLifecycleStatus.CLUSTERED)
```
Вызывается после `create_issue()` вне зависимости от того, был ли путь create или extend. `member_story_ids` — это только stories из текущего батча (batch 2), уже-CLUSTERED stories из batch 1 не входят в `list_stories_ready_for_clustering()`. Механизм корректный.

---

## 5. Выявленные GAP-ы

---

### GAP-29-01 — `save_projection_embedding()` использует DELETE+INSERT вместо upsert

**Тип:** `spec_deviation` | `minor_impl`  
**Где:** `db_sqlite.py:464-492`, `db_supabase.py:430-459`

**Факт (SQLite):**
```python
self.db.connection.execute("DELETE FROM doge_issue_embeddings WHERE issue_id = ?", (issue_id,))
self.db.connection.execute("INSERT INTO doge_issue_embeddings (...) VALUES (...)", ...)
```

**Факт (Supabase):**
```python
self.db._request(method="DELETE", path="/rest/v1/doge_issue_embeddings", params={"issue_id": ...})
self.db._request(method="POST", path="/rest/v1/doge_issue_embeddings", json_body=[...])
```

**Проблема:** req29 Section 7.2 требует idempotent upsert. Текущий паттерн DELETE+INSERT создаёт окно гонки: между DELETE и INSERT запись временно отсутствует. При concurrent read (SPA dashboard в процессе extend) embedding не будет найден. Также паттерн не атомарный — если INSERT упадёт, запись исчезнет.

**Решение:**
```sql
-- SQLite
INSERT INTO doge_issue_embeddings (issue_id, model_name, ...)
VALUES (?, ?, ...)
ON CONFLICT(issue_id) DO UPDATE SET
    model_name = excluded.model_name,
    embedding_vector_json = excluded.embedding_vector_json,
    source_checksum = excluded.source_checksum,
    embedding_policy_version = excluded.embedding_policy_version,
    created_at = excluded.created_at
```
Supabase: заменить двойной request на один POST с `prefer="resolution=merge-duplicates,return=minimal"` и `on_conflict=issue_id`.

#### Оценка сложности / важности

| Параметр | Значение |
|----------|---------|
| **Тип** | spec_deviation (ненарушение в демо, нарушение в prod) |
| **Файлов затронуто** | 2 (`db_sqlite.py`, `db_supabase.py`) |
| **Архитектурных слоёв** | 1 (только persistence) |
| **Production risk** | ⚠️ Средний — потеря embedding при concurrent access |
| **Demo risk** | Минимальный — single-process |
| **Требует migration** | Нет — изменение только SQL/HTTP |
| **LoC delta** | ~-6 / +4 строки на файл |
| **Трудоёмкость** | **XS** (15-20 мин оба файла) |
| **Важность** | **P2** — не блокирует AC, нарушает INV semantics |
| **Приоритет исправления** | До production, не срочно для demo |

---

### GAP-29-02 — E2E тест не проверяет `CLUSTERED` статус историй из обоих батчей (AC-29-6)

**Тип:** `test_coverage` | `AC gap`  
**Где:** `tests/test_e2e_story_cluster_issue_pipeline.py:220-264`

**Факт:** `test_e2e_living_issue_two_batches_reuses_issue_and_appends_stories` проверяет:
- ✅ `second_issue_ids == [issue_id]` (AC-29-1)
- ✅ `set(promoted.story_ids) == {"s1","s2","s3","s4"}` (AC-29-2)
- ✅ `audit[-1].rationale == "cluster_growth_extend"` (AC-29-3)

Не проверяет:
- ❌ `stories.get_story("s1").lifecycle_status == CLUSTERED` (AC-29-6 для batch 1)
- ❌ `stories.get_story("s3").lifecycle_status == CLUSTERED` (AC-29-6 для batch 2)

**Проблема:** AC-29-6 формально не покрыт тестовым assertion. Код выполняет update (`cluster_orchestrator.py:237-241`), но тест не верифицирует результат. Если в будущем CLUSTERED update сломается для extend path, тест этого не поймает.

**Решение:** Добавить в существующий тест:
```python
for sid in ("s1", "s2"):  # batch 1
    story = stories.get_story(sid)
    assert story is not None
    assert story.lifecycle_status is StoryLifecycleStatus.CLUSTERED

for sid in ("s3", "s4"):  # batch 2
    story = stories.get_story(sid)
    assert story is not None
    assert story.lifecycle_status is StoryLifecycleStatus.CLUSTERED
```

#### Оценка сложности / важности

| Параметр | Значение |
|----------|---------|
| **Тип** | test_coverage |
| **Файлов затронуто** | 1 (`test_e2e_story_cluster_issue_pipeline.py`) |
| **Архитектурных слоёв** | 0 (только тест, prod код не меняется) |
| **AC coverage** | AC-29-6 не закрыт без этого assert |
| **Regression risk** | ⚠️ Без теста изменение в orchestrator lifecycle update не будет обнаружено |
| **LoC delta** | ~+8 строк в тест |
| **Трудоёмкость** | **XS** (5-10 мин) |
| **Важность** | **P1** — прямое закрытие AC-29-6 |
| **Приоритет исправления** | Немедленно (дешёво + закрывает AC) |

---

### GAP-29-03 — Нет SQLite-backed теста для extend path (backend parity)

**Тип:** `test_coverage` | `backend_parity`  
**Где:** отсутствие в `tests/test_db_backed_pipeline_e2e.py` и любом DB-backed файле

**Факт:** Все три теста living issues (`test_e2e_living_issue_two_batches_reuses_issue_and_appends_stories`, `test_issue_create_service_create_then_extend_reuses_issue_id`, `test_issue_create_service_idempotent_extend_when_no_new_stories`) используют **только in-memory stores**. 

Непроверенные SQL-пути:
- `SqliteIssueCandidateStore.save()` UPDATE path (при extend story_ids_json обновляется в строке таблицы)
- `SqliteIssueCandidateStore.find_promoted_by_cluster_id()` — возвращает row с обновлённым story_ids_json  
- `SqliteReviewAuditLogRepository.append()` для rationale=`cluster_growth_extend`
- `SqliteIssueProjectionStore.save_projection()` — повторный upsert на том же issue_id

**Проблема:** SQLite-код looks correct (ON CONFLICT DO UPDATE SET), но его поведение в extend сценарии не протестировано. Баг в JSON serialization story_ids или off-by-one в SQL filter мог бы существовать незамеченным.

**Решение:** Добавить в `tests/test_db_backed_pipeline_e2e.py` тест:
```python
def test_sqlite_backed_extend_persists_merged_story_ids_and_audit(tmp_db):
    # create issue → extend issue → verify DB rows directly
    # check: issue_candidates.story_ids_json contains both batches
    # check: review_audit_log has cluster_growth_extend entry
    # check: doge_issues.payload_json reflects updated projection
```

#### Оценка сложности / важности

| Параметр | Значение |
|----------|---------|
| **Тип** | test_coverage / backend_parity |
| **Файлов затронуто** | 1 (добавить тест в `test_db_backed_pipeline_e2e.py` или новый файл) |
| **Архитектурных слоёв** | 0 prod, 1 test |
| **Coverage gap** | SQL UPDATE и round-trip fetch для extend path не проверены |
| **Risk** | Низкий — код выглядит корректно, но отсутствие теста снижает confidence |
| **LoC delta** | ~+40-60 строк нового теста |
| **Трудоёмкость** | **S** (30-45 мин, нужно настроить SQLite fixtures) |
| **Важность** | **P2** — не блокирует AC, но нужен для production confidence |
| **Приоритет исправления** | До production, желателен для beta |

---

### GAP-29-04 — INV-LI-04 (проекция после extend) не имеет content assertion

**Тип:** `test_coverage` | `invariant_gap`  
**Где:** `tests/test_issue_create_service.py:76-96`, `tests/test_e2e_story_cluster_issue_pipeline.py:244-264`

**Факт:** Оба теста подтверждают, что после extend:
- ✅ `first.issue_id == second.issue_id`
- ✅ `promoted.story_ids == tuple(sorted(...))`
- ✅ `audit[-1].rationale == "cluster_growth_extend"`

Но ни один тест не проверяет, что **projection_payload (description/aggregate_text) обновился** с учётом новых stories. INV-LI-04: "DOGEIssue всегда содержит aggregate_text от актуального набора story_ids."

**Конкретная проблема:** если `build_projection_input(story_ids=updated.story_ids)` в `_extend_issue()` тихо упал или вернул старый контент, тест не поймал бы это.

**Решение:**
```python
# в test_issue_create_service_create_then_extend_reuses_issue_id
# Verify INV-LI-04: projection description after extend reflects all stories
assert second.projection is not None
assert isinstance(second.projection.get("description"), str)
# After extend with story_3, description must differ from first result
# (3 stories vs 2 stories in aggregate_text)
assert second.projection["description"] != first.projection["description"]
```

Или, если `IssueProjectionStore` заполняется, проверить сохранённый payload:
```python
saved_projection = projection_store._rows[first.issue_id]
assert "description" in saved_projection  # and it reflects 3 stories
```

#### Оценка сложности / важности

| Параметр | Значение |
|----------|---------|
| **Тип** | test_coverage / invariant |
| **Файлов затронуто** | 1-2 тест-файла |
| **Регрессионный риск** | Низкий для detect, высокий для miss |
| **INV coverage** | INV-LI-04 не верифицируется ни одним тестом |
| **LoC delta** | ~+5 строк assertion |
| **Трудоёмкость** | **XS** (10-15 мин) |
| **Важность** | **P2** — не блокирует AC, но INV не имеет coverage |
| **Приоритет исправления** | Желательно перед release |

---

## 6. Сводная таблица гапов

| GAP-ID | Тип | Компонент | Важность | Сложность | AC/INV | Приоритет |
|--------|-----|-----------|----------|-----------|--------|-----------|
| GAP-29-01 | spec_deviation | `db_sqlite.py`, `db_supabase.py` (embedding store) | P2 | XS | INV-LI-04 semantics | До prod |
| GAP-29-02 | test_coverage | E2E тест (CLUSTERED assert) | **P1** | **XS** | **AC-29-6** | Немедленно |
| GAP-29-03 | test_coverage | SQLite extend path test | P2 | S | AC-29-1,2,3 (SQL) | До beta |
| GAP-29-04 | test_coverage | Projection content assert | P2 | XS | INV-LI-04 | До release |

---

## 7. Что реализовано полностью и корректно

Перечень без гапов — для передачи исполняющему агенту как «не трогать»:

- `IssuePromotionService.extend_candidate()` — implementation и unit tests ✅
- `IssueCreateService.create_issue()` create/extend routing ✅
- `IssueCreateService._extend_issue()` — полный extend path ✅
- `IssueCreateService._extend_issue()` — idempotent path (no new stories) ✅
- `find_promoted_by_cluster_id()` — все 3 бэкенда ✅
- `IssueCandidateStore.save()` update semantics — все 3 бэкенда ✅
- `save_issue_story_links()` DO NOTHING semantics — SQLite + Supabase ✅
- `save_projection()` upsert — SQLite ✅
- CLUSTERED lifecycle update в orchestrator для extend path ✅
- audit_log `cluster_growth_extend` entry ✅
- Тест AC-29-1: `second_issue_ids == [issue_id]` ✅
- Тест AC-29-2: `set(promoted.story_ids) == {"s1","s2","s3","s4"}` ✅
- Тест AC-29-3: `audit[-1].rationale == "cluster_growth_extend"` ✅
- Тест AC-29-5: idempotent — score не перезаписывается ✅

---

## 8. Рекомендуемый порядок исправления

```
1. GAP-29-02 — добавить 8 строк assert в существующий E2E тест (5 мин, закрывает AC-29-6)
2. GAP-29-04 — добавить content assert на projection после extend (10 мин, закрывает INV-LI-04)
3. GAP-29-01 — заменить DELETE+INSERT на ON CONFLICT DO UPDATE SET (20 мин, закрывает spec deviation)
4. GAP-29-03 — добавить SQLite-backed extend тест (45 мин, backend parity coverage)
```

Суммарная трудоёмкость всех 4 гапов: **S** (~80 мин).
