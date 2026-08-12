## Task workspace — `task-m2-02-12-t04-handlers-wire-intake-notes-flags`

- Story: [`../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md`](../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md)
- Decision Ref: [`../../../../../../requirements/46-demo-services-enablement-and-response-transparency.md`](../../../../../../requirements/46-demo-services-enablement-and-response-transparency.md) §2.3C

---
**Priority:** P0  
**Complexity:** S  
**Estimate:** ~30 min  
**Status:** ready  
**Wave:** `pkg-000026`  
**Depends on:** T02, T03  
---

## Task: implement — wire `StoryIntakeResult` → `build_story_intake_response`

### Цель
В `handle_story_intake` передать `geo_resolved` и `gpt_signals_persisted` из `StoryIntakeResult` в response builder.

### Факты из кода
- REQ §2.3C — handler returns 202 with flags from `result.story`, `result.geo_resolved`, `result.gpt_signals_persisted`.
- [`src/core/api/handlers.py`](../../../../../../../src/core/api/handlers.py) — `handle_story_intake` (coordinate with T02 return type).

### AC/DoD
- [ ] (P0) Handler uses `StoryIntakeResult` from `create_story()`.
- [ ] (P0) `build_story_intake_response(..., geo_resolved=..., gpt_signals_persisted=...)` called with result fields.
- [ ] (P0) HTTP status remains 202 on success path.
- [ ] (P1) Idempotency replay path returns consistent `intake_notes` (define expected behavior in test T06).

### Где менять код
- [`src/core/api/handlers.py`](../../../../../../../src/core/api/handlers.py)

### Out of scope
- Contract/OpenAPI (T03, T05).

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_http_intake_endpoint.py
```
