## Task workspace — `task-m2-02-12-t03-intake-notes-contract-response-builder`

- Story: [`../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md`](../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md)
- Decision Ref: [`../../../../../../requirements/46-demo-services-enablement-and-response-transparency.md`](../../../../../../requirements/46-demo-services-enablement-and-response-transparency.md) §2.3A

---
**Priority:** P0  
**Complexity:** S  
**Estimate:** ~1 h  
**Status:** ready  
**Wave:** `pkg-000026`  
---

## Task: implement — `IntakeNotes` + `build_story_intake_response` flags

### Цель
Добавить `IntakeNotes` (`geo_resolved`, `gpt_signals_persisted`) в success envelope data для POST `/intake/stories` 202.

### Факты из кода
1. [`contracts.py`](../../../../../../../src/core/intake/contracts.py) L99–105 — `StoryIntakeResponse` без `intake_notes`.
2. [`contracts.py`](../../../../../../../src/core/intake/contracts.py) L358–369 — `build_story_intake_response(story_id, status, trace_id)` only.
3. REQ §2.3A — `IntakeNotes.as_dict()`, optional field on response.

### AC/DoD (REQ-46 §4 intake_notes)
- [ ] (P0) `IntakeNotes` frozen dataclass + `as_dict()`.
- [ ] (P0) `StoryIntakeResponse` includes `intake_notes: IntakeNotes | None`.
- [ ] (P0) `build_story_intake_response(..., geo_resolved=..., gpt_signals_persisted=...)` embeds notes in envelope `data`.
- [ ] (P0) Default `gpt_signals_persisted=True` when arg omitted (REQ §2.3A).
- [ ] (P1) Backward-compatible: existing tests updated in T06 (field additive).

### Где менять код
- [`src/core/intake/contracts.py`](../../../../../../../src/core/intake/contracts.py)

### Out of scope
- Handler wiring (T04).
- OpenAPI schema (T05).

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_http_intake_endpoint.py -k intake
```
