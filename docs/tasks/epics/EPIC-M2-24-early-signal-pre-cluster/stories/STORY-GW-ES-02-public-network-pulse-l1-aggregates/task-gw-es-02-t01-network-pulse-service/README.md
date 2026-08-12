# task-gw-es-02-t01-network-pulse-service

## Meta
- **Story:** [STORY-GW-ES-02](../STORY-GW-ES-02-public-network-pulse-l1-aggregates.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000059
- **Skill declared:** python-pro
- **Depends on:** — (soft: T00 for final payload key names; MVP dims OK without path)
- **decision_ref:** backlog ES-02 §A + MVP product defaults

## Purpose
Реализовать `NetworkPulseService.build_pulse()` — `stories_collected` + languages/areas/topics/recent_7d; только non-PII aggregates; public scope (без submitter filter).

## Code Facts
- Etalon aggregate — [`story_activity.py:27-72`](../../../../../../../../src/core/application/story_activity.py) `StoryActivityService`
- `StoryRepository.list_stories` — [`contracts.py:79-81`](../../../../../../../../src/core/domain/contracts.py)
- Languages/geo — [`contracts.py:51-62`](../../../../../../../../src/core/domain/contracts.py) `narrative_language`, `StoryGeoSnapshot.admin_*`
- Topics — [`contracts.py:158-169`](../../../../../../../../src/core/domain/contracts.py) `StoryLabelRepository`
- Opaque author keys — [`contracts.py:48-49`](../../../../../../../../src/core/domain/contracts.py)

## Acceptance / DoD
- [x] Traces parent AC: `NetworkPulseService` exists; `stories_collected` = `len(list_stories())`
- [x] MVP dims: languages / areas / topics / recent_stories_7d (or explicit omit only if T00 payload narrower — then update story AC)
- [x] No `submitter_*`, narrative text, contacts in payload
- [x] Module `src/core/application/network_pulse.py`; `@dataclass(frozen=True)` with `story_repository` + optional `story_label_repository`
- [x] SQL/`count` RPC not required (out of first DoD)
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-es-02-t01.md` signed (Date post P3 verify only)

## Where to change
- New: `doge-complaints-gateway/src/core/application/network_pulse.py`
- Optional export from `core.application` package `__init__` if pattern requires

## Out of scope
- DI wire (T02); HTTP path (T03); invent path; Voices; Issues changes

## Verification commands
```bash
rg -n 'class NetworkPulseService|def build_pulse' doge-complaints-gateway/src/core/application/network_pulse.py
rg -n 'submitter_|narrative' doge-complaints-gateway/src/core/application/network_pulse.py || true
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_es_02_* -k pulse_service --collect-only 2>/dev/null | head
```
