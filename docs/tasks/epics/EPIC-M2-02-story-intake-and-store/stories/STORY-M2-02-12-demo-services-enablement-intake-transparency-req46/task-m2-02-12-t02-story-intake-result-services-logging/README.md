## Task workspace — `task-m2-02-12-t02-story-intake-result-services-logging`

- Story: [`../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md`](../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md)
- Decision Ref: [`../../../../../../requirements/46-demo-services-enablement-and-response-transparency.md`](../../../../../../requirements/46-demo-services-enablement-and-response-transparency.md) §2.2, §2.3B

---
**Priority:** P0  
**Complexity:** M  
**Estimate:** ~2 h  
**Status:** ready  
**Wave:** `pkg-000026`  
---

## Task: implement — `StoryIntakeResult`, geo INFO log, gpt_signals WARNING

### Цель
Вернуть из `create_story()` флаги `geo_resolved` и `gpt_signals_persisted`; промоутить geo miss в INFO; логировать silent gpt_signals drop как WARNING.

### Почему это важно (риск)
Сейчас `create_story()` → `StoryRecord` only ([`services.py`](../../../../../../../src/core/application/services.py) L114–116); `_persist_gpt_classifier_signals` silent return при `store is None` ([L96–97](../../../../../../../src/core/application/services.py)).

### Факты из кода
1. [`services.py`](../../../../../../../src/core/application/services.py) L93–112 — `_persist_gpt_classifier_signals`; no return value for persist ok/fail.
2. REQ §2.3B — `StoryIntakeResult` dataclass; `create_story()` returns it.
3. REQ §2.2 — geo miss INFO vs empty query DEBUG.

### Gap / Проблема
Handler не может построить `intake_notes` без service-layer flags (T04 blocked until this task).

### AC/DoD (REQ-46 §4)
- [ ] (P0) `StoryIntakeResult(story, geo_resolved, gpt_signals_persisted)` defined in `services.py`.
- [ ] (P0) `create_story()` returns `StoryIntakeResult` (update all internal callers in same PR wave).
- [ ] (P0) Non-empty `location_query` + geo miss → log `intake.geo_not_resolved` at INFO (REQ §2.2A).
- [ ] (P0) Empty `location_query` → remains DEBUG `intake.geo_skip`.
- [ ] (P0) `story_signal_store is None` + gpt_signals present → WARNING `intake.gpt_signals_drop reason=signal_store_not_configured`.
- [ ] (P0) Exception on persist → `gpt_signals_persisted=False` (existing warning path).
- [ ] (P1) No `gpt_signals` in request → `gpt_signals_persisted=True` (nothing to persist).

### Где менять код
- [`src/core/application/services.py`](../../../../../../../src/core/application/services.py)
- Call sites: handlers (T04), tests (T06).

### Out of scope
- `IntakeNotes` dataclass (T03).
- OpenAPI (T05).

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_http_intake_endpoint.py tests/test_gpt_signals_intake.py
```
