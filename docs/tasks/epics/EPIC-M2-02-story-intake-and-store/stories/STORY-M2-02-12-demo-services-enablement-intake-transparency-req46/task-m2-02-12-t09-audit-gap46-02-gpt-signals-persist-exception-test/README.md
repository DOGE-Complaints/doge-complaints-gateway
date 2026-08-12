## Task workspace — `task-m2-02-12-t09-audit-gap46-02-gpt-signals-persist-exception-test`

- Story: [`../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md`](../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md)
- Decision Ref: [`../../../../../../analysis/audit-req46-demo-services-intake-transparency-2026-06-02.md`](../../../../../../analysis/audit-req46-demo-services-intake-transparency-2026-06-02.md) §3 G2; REQ-46 §4 intake_notes (`gpt_signals_persisted: false` when persist fails)

---
**Priority:** P1  
**Complexity:** S  
**Estimate:** ~30 min  
**Status:** ready  
**Wave:** audit override (`run_mode=story02_12_audit_req46_followup`)  
---

## Task: tests — `save_signals` exception → `gpt_signals_persisted: false`

### Цель
Закрыть тестовый пробел: production-сбой из gap-report (exception при Supabase-записи) должен отражаться в `intake_notes` и логах так же, как `store is None`.

### Почему это важно (риск)
Реализация exception-ветки есть ([`services.py`](../../../../../../../src/core/application/services.py) L121–130), но единственный тест бьёт только `story_signal_store is None` ([`test_req46_intake_transparency.py`](../../../../../../../tests/test_req46_intake_transparency.py) L67–91). Регрессия exception-path не поймается CI.

### Факты из кода
1. [`services.py`](../../../../../../../src/core/application/services.py) L121–130 — `except` → `return False` + WARNING `intake.gpt_signals_persist_failed`.
2. [`test_req46_intake_transparency.py`](../../../../../../../tests/test_req46_intake_transparency.py) L67–91 — `test_intake_notes_gpt_signals_drop_when_store_missing` (store `None` only).
3. Audit [`audit-req46-demo-services-intake-transparency-2026-06-02.md`](../../../../../../analysis/audit-req46-demo-services-intake-transparency-2026-06-02.md) §3 G2 — prod failure class (exception on persist, не `store is None`).

### Gap / Проблема
**G2 (audit):** нет теста «store configured, `save_signals` raises».

### AC / DoD
- [ ] (P0) Тест с stub `StorySignalStore`: `save_signals` raises `RuntimeError` (или `OSError`); `create_story` → `gpt_signals_persisted is False`.
- [ ] (P0) В том же тесте (caplog WARNING): сообщение содержит `intake.gpt_signals_persist_failed`.
- [ ] (P0) Story record всё равно создаётся (202 path); только флаг сигналов `False`.
- [ ] (P1) `python3 -m pytest -q tests/test_req46_intake_transparency.py` — green.

### Рекомендуемая реализация (P3)
Минимальный frozen dataclass stub в [`test_req46_intake_transparency.py`](../../../../../../../tests/test_req46_intake_transparency.py) с `get_signals` → `None` и `save_signals` → raise.

### Где менять
- Только [`tests/test_req46_intake_transparency.py`](../../../../../../../tests/test_req46_intake_transparency.py) (предпочтительно).

### Out of scope
- Изменения `db_supabase.py` / live integration.
- T08/T10; T01–T07; новый `pkg-*.yaml`.

### Команды проверки
```bash
cd doge-complaints-gateway
python3 -m pytest -q tests/test_req46_intake_transparency.py
```
