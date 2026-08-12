## Task workspace — `task-m2-02-12-t08-audit-gap46-01-idempotency-gpt-signals-replay-flag`

- Story: [`../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md`](../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md)
- Decision Ref: [`../../../../../../analysis/audit-req46-demo-services-intake-transparency-2026-06-02.md`](../../../../../../analysis/audit-req46-demo-services-intake-transparency-2026-06-02.md) §3 G1; [`../../../../../../requirements/46-demo-services-enablement-and-response-transparency.md`](../../../../../../requirements/46-demo-services-enablement-and-response-transparency.md) §2.3 (intake_notes semantics)

---
**Priority:** P1  
**Complexity:** S  
**Estimate:** ~45 min  
**Status:** ready  
**Wave:** audit override (`run_mode=story02_12_audit_req46_followup`)  
---

## Task: fix — idempotent replay `gpt_signals_persisted` reflects stored state

### Цель
На idempotent hit HTTP intake возвращать достоверный `data.intake_notes.gpt_signals_persisted`: `False` только когда сигналы не были сохранены, а не когда в повторном запросе снова присутствует блок `gpt_signals`.

### Почему это важно (риск)
Сейчас при replay с `gpt_signals` в теле API отдаёт `gpt_signals_persisted: false`, хотя запись могла быть успешно создана при первом приёме — GPT-оркестратор получает ложный сигнал о потере данных (audit G1, story `d295ed9f` class of issues).

### Факты из кода
1. [`services.py`](../../../../../../../src/core/application/services.py) L163–167 — idempotent return: `gpt_signals_persisted=request.gpt_signals is None`.
2. [`contracts.py`](../../../../../../../src/core/domain/contracts.py) L131–138 — `StorySignalStore.get_signals(story_id, policy) -> Mapping | None`.
3. [`repositories.py`](../../../../../../../src/core/infrastructure/repositories.py) — `InMemoryStorySignalStore.get_signals` для unit tests.
4. [`services.py`](../../../../../../../src/core/application/services.py) L69–70 — `GPT_CLASSIFIER_POLICY_VERSION = "gpt.story_classifier.v1"`.

### Gap / Проблема
**G1 (audit):** replay-path не различает «нечего сохранять в этом вызове» и «сигналы уже в store с первого create».

### AC / DoD
- [ ] (P0) Idempotent replay с тем же `idempotency_key`, когда при первом create `gpt_signals` были сохранены: `gpt_signals_persisted` is `True` (при наличии store и записи для `story_id` + policy).
- [ ] (P0) Idempotent replay при `story_signal_store is None` и `gpt_signals` в запросе: `gpt_signals_persisted` is `False` (как сейчас для primary path drop).
- [ ] (P0) Первичный create без `gpt_signals`: `gpt_signals_persisted` is `True` (без регрессии).
- [ ] (P1) Unit test: два вызова `create_story` с одним `idempotency_key`, второй с `gpt_signals` в payload — assert `gpt_signals_persisted` на втором результате.
- [ ] (P1) `python3 -m pytest -q tests/test_story_intake_idempotency.py tests/test_req46_intake_transparency.py` — green.

### Рекомендуемая реализация (P3)
На idempotent hit, если `request.gpt_signals is None` → `True`. Иначе, если `story_signal_store is None` → `False`. Иначе → `get_signals(story_id, GPT_CLASSIFIER_POLICY_VERSION) is not None`.

Альтернатива (только по решению PM): задокументировать per-call семантику в [`API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) §6.6 — не предпочтительно для audit G1.

### Где менять
- [`src/core/application/services.py`](../../../../../../../src/core/application/services.py) — idempotent branch L163–167.
- Tests: [`tests/test_story_intake_idempotency.py`](../../../../../../../tests/test_story_intake_idempotency.py) и/или [`tests/test_req46_intake_transparency.py`](../../../../../../../tests/test_req46_intake_transparency.py).

### Out of scope
- T01–T07 повторная реализация; T07 SQL cleanup.
- Новый/изменённый `pkg-*.yaml`; `gateway-active-package.current.yaml`.
- G5 double geo-resolve; G2/G3 (отдельные таски T09/T10).

### Команды проверки
```bash
cd doge-complaints-gateway
python3 -m pytest -q tests/test_story_intake_idempotency.py tests/test_req46_intake_transparency.py
```
