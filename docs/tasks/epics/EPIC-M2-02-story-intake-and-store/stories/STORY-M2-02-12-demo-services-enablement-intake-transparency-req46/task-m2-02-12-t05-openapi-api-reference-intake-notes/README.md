## Task workspace — `task-m2-02-12-t05-openapi-api-reference-intake-notes`

- Story: [`../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md`](../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md)
- Decision Ref: [`../../../../../../requirements/46-demo-services-enablement-and-response-transparency.md`](../../../../../../requirements/46-demo-services-enablement-and-response-transparency.md) §2.3D, §4 intake_notes

---
**Priority:** P1  
**Complexity:** S  
**Estimate:** ~45 min  
**Status:** ready  
**Wave:** `pkg-000026`  
**Depends on:** T03 (runtime shape stable)  
---

## Task: docs — OpenAPI + API_REFERENCE `intake_notes`

### Цель
Задокументировать `data.intake_notes.geo_resolved` и `data.intake_notes.gpt_signals_persisted` в runtime contract docs (lockstep с кодом T03–T04).

### AC/DoD
- [ ] (P0) [`openapi.yaml`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) — `intake_notes` object under `StoryIntakeResponseData` / success envelope data.
- [ ] (P0) [`API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) §6.6 — описание полей и семантики boolean flags.
- [ ] (P1) Cross-ref REQ-46 §2.3 в story gate evidence.
- [ ] (P1) No drift vs actual JSON from T06 tests.

### Где менять
- [`docs/runtime-docs/api-reference/openapi.yaml`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml)
- [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md)

### Out of scope
- GPT UI OpenAPI copy (REQ-47).
- `status` enum (STORY-M2-02-11 separate override).

### Команды проверки
```bash
# Manual: diff schema vs sample 202 from pytest caplog or fixture JSON
cd doge-complaints-gateway && python3 -m pytest -q tests/test_req46_intake_transparency.py 2>/dev/null || true
```
