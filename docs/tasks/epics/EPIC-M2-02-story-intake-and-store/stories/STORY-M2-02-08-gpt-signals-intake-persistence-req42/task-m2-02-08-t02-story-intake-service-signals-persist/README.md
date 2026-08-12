## Task workspace — `task-m2-02-08-t02-story-intake-service-signals-persist`

- Story: [`../STORY-M2-02-08-gpt-signals-intake-persistence-req42.md`](../STORY-M2-02-08-gpt-signals-intake-persistence-req42.md)
- Decision Ref: [`../../../../../../requirements/42-gpt-signals-story-intake-extension.md`](../../../../../../requirements/42-gpt-signals-story-intake-extension.md) §2.2, §3.2, §3.3

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000022`  
---

## Task: implement — persist gpt_signals via StoryIntakeService

### Цель
После успешного `save_story`, при `request.gpt_signals is not None`, записать signals в `story_signals` с policy `gpt.story_classifier.v1`.

### Факты из кода
1. [`src/core/application/services.py`](../../../../../../../src/core/application/services.py) L68–74 — `StoryIntakeService` без `story_signal_store`; есть `story_embedding_store`.
2. [`src/core/infrastructure/service_factory.py`](../../../../../../../src/core/infrastructure/service_factory.py) L59, L65–72 — `story_signal_store` на factory, не передаётся в `get_story_intake_service()`.
3. [`src/core/infrastructure/db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py) L906–917 — `SqliteStorySignalStore.save_signals` upsert по `(story_id, extraction_policy)`.
4. [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) L931–945 — `SupabaseStorySignalStore.save_signals` с `on_conflict`.
5. [`src/core/application/cluster_orchestrator.py`](../../../../../../../src/core/application/cluster_orchestrator.py) L57 — пример вызова `save_signals(story_id, policy, signals)`.

### Gap / Проблема
Intake принимает story, но GPT classifier signals не персистируются — таблица `story_signals` пуста для policy `gpt.story_classifier.v1`.

### AC/DoD
- [ ] (P0) `GPT_CLASSIFIER_POLICY_VERSION = "gpt.story_classifier.v1"` в `services.py` (рядом с embedding policy constant).
- [ ] (P0) `StoryIntakeService` получает optional `story_signal_store: StorySignalStore | None`.
- [ ] (P0) В `create_story()` после успешного `save_story`: если `request.gpt_signals is not None`, build `signals_json` dict с keys severity/impact_estimation/problem_status/source=`gpt_intake_v1` (None для отсутствующих полей).
- [ ] (P0) Не создавать запись, если `gpt_signals` блок отсутствует в request.
- [ ] (P0) Ошибка `save_signals` — log exception, не raise (intake 202 сохраняется).
- [ ] (P0) `DefaultServiceFactory.get_story_intake_service()` передаёт `self.story_signal_store`.
- [ ] (P1) Не добавлять дублирующий `save_story_signals()` — использовать Protocol `save_signals`.

### Где менять код
- [`src/core/application/services.py`](../../../../../../../src/core/application/services.py)
- [`src/core/infrastructure/service_factory.py`](../../../../../../../src/core/infrastructure/service_factory.py)

### Out of scope
- Новые SQL migrations (таблица есть, REQ-34).
- Транзакционный merge commit с `save_story` (document: best-effort post-save).

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gpt_signals_intake.py -q
```
