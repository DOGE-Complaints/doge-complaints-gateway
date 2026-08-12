# task-gw-es-03-t01-emerging-signals-service

## Meta
- **Story:** [STORY-GW-ES-03](../STORY-GW-ES-03-public-emerging-l2-read.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000060
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-08-10T12:06:12Z

## Purpose
Реализовать `EmergingSignalsService` в `emerging_signals.py`: top-N label frequencies; exclude stories linked to **published** Issues; non-PII payload; **no** `EmergingSignal` table.

## Code Facts
- Labels port — [`contracts.py:158`](../../../../../../../../src/core/domain/contracts.py) `StoryLabelRepository`
- Published map — [`story_activity.py:13–23`](../../../../../../../../src/core/application/story_activity.py) `CABINET_STATUS_PUBLISHED` / `map_issue_status_to_cabinet`
- Link — [`issue_create.py:88`](../../../../../../../../src/core/application/issue_create.py) `get_issue_id_for_story`
- Pulse etalon (DI shape, not source) — [`network_pulse.py`](../../../../../../../../src/core/application/network_pulse.py)
- MVP rule — story §«MVP derivation rule» (labels source ≠ `list_projections`)

## Acceptance / DoD
- [ ] Traces AC: MVP rule (label freq; exclude published-linked); no EmergingSignal table; no PII keys
- [ ] Module `src/core/application/emerging_signals.py` with frozen dataclass deps per story §A
- [ ] `build_emerging(*, top_n=…)` implements skip-published + aggregate + top-N
- [ ] Does not use Issues list as emerging source
- [ ] BULLRUN phases complete
- [ ] `acceptance-verification-gw-es-03-t01.md` signed (Date post P3 verify only)

## Where to change
- `doge-complaints-gateway/src/core/application/emerging_signals.py` (new)
- Reuse helpers from `story_activity.py` / `canonicalize_status_on_read` — no new entity/migration

## Out of scope
- DI wiring (T02); HTTP route (T03); OpenAPI (T06); invent path

## Verification commands
```bash
rg -n 'class EmergingSignalsService|def build_emerging|EmergingSignal' doge-complaints-gateway/src/core/application/
rg -n 'CREATE TABLE.*emerging' doge-complaints-gateway/supabase/ || true
```
