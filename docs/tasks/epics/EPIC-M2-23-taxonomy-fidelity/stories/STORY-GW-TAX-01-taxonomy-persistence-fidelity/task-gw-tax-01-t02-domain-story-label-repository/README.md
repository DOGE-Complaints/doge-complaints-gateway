# task-gw-tax-01-t02-domain-story-label-repository

## Meta
- **Story:** [STORY-GW-TAX-01](../STORY-GW-TAX-01-taxonomy-persistence-fidelity.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000054
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Домен (D-TAX-2/3): `StoryLabel` value-object (`story_id, axis, label, disposition`) + порт `StoryLabelRepository` (`save_labels`/`list_by_story`/`list_by_axis`).

## Code Facts
- `StoryRecord.narrative_canonical_labels` flat tuple — [`contracts.py:61`](../../../../../../../../src/core/domain/contracts.py#L61)
- `StoryLabel` / `StoryLabelRepository` — **отсутствует** в `src/core/domain/`
- Target schema: `story_labels(story_id, axis, label, disposition)` (backlog §2)

## Acceptance / DoD
- [ ] Traces parent AC-2: all dispositions persistable via repository contract
- [ ] Scope trace: backlog §2 domain D-TAX-2/3
- [ ] `StoryLabel` VO + `StoryLabelRepository` Protocol in [`contracts.py`](../../../../../../../../src/core/domain/contracts.py)
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-tax-01-t02.md`](./acceptance-verification-gw-tax-01-t02.md) signed (Date post live-run only)

## Where to change
- [`src/core/domain/contracts.py`](../../../../../../../../src/core/domain/contracts.py)
- [`src/core/domain/__init__.py`](../../../../../../../../src/core/domain/__init__.py) (exports)

## Out of scope
- Adapters / migration (T03)
- Intake parsing (T01)

## Verification commands (post live-run only)
```bash
rg -n "StoryLabel|StoryLabelRepository" doge-complaints-gateway/src/core/domain/contracts.py
```
