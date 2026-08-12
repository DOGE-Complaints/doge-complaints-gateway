# task-gw-tax-01-t04-persist-labels-on-story-intake-submit

## Meta
- **Story:** [STORY-GW-TAX-01](../STORY-GW-TAX-01-taxonomy-persistence-fidelity.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000054
- **Skill declared:** python-pro
- **Depends on:** T03

## Purpose
Persist на submit (D-TAX-3): все метки с disposition в `story_labels` — change-propagation в `handle_story_intake` submit-bridge.

## Code Facts
- Submit bridge — [`handlers.py:149`](../../../../../../../../src/core/api/handlers.py#L149) `handle_story_intake`
- Current intake logging uses flat labels — [`handlers.py:218`](../../../../../../../../src/core/api/handlers.py) `canonical_labels_count`
- `StoryLabelRepository` wired after T03 — not yet in handlers

## Acceptance / DoD
- [ ] Traces parent AC-2: all dispositions (canonical/metadata_only/internal/…) persisted on submit
- [ ] Scope trace: backlog §2 persist D-TAX-3
- [ ] `handle_story_intake` calls `StoryLabelRepository.save_labels` for per-axis + legacy-derived labels
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-tax-01-t04.md`](./acceptance-verification-gw-tax-01-t04.md) signed (Date post live-run only)

## Where to change
- [`src/core/api/handlers.py`](../../../../../../../../src/core/api/handlers.py) — `handle_story_intake`

## Out of scope
- Public read-filter (T05)
- Clustering signal source (GW-TAX-02)

## Verification commands (post live-run only)
```bash
rg -n "save_labels|story_label" doge-complaints-gateway/src/core/api/handlers.py
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_tax_01_* -m "not live_integration" -k persist
```
