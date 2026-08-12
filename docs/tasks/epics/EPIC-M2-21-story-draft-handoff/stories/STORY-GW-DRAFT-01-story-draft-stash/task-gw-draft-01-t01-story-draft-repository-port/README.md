# task-gw-draft-01-t01-story-draft-repository-port

## Meta
- **Story:** [STORY-GW-DRAFT-01](../STORY-GW-DRAFT-01-story-draft-stash.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000043
- **Skill declared:** python-pro
- **Depends on:** —

## Purpose
Добавить доменный порт `StoryDraftRepository` и модель `StoryDraftRecord` (draft_id, payload, created_at, expires_at) в domain layer (D-DRAFT-2 C).

## Code Facts
- `StoryRepository` pattern — [`domain/contracts.py:70-81`](../../../../../../../src/core/domain/contracts.py)
- `StoryDraftRepository` — **отсутствует** (grep=0)
- `StoryRecord` dataclass — [`domain/contracts.py`](../../../../../../../src/core/domain/contracts.py)

## Acceptance / DoD
- Traces parent AC #6: отдельный порт, не смешан со story-store
- Protocol: `save_draft(record) -> draft_id`, `get_draft(draft_id) -> StoryDraftRecord | None` with TTL semantics documented
- `StoryDraftRecord` frozen dataclass with `expires_at`
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py)

## Out of scope
Adapter implementations (T02); HTTP routes (T03/T04)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'StoryDraftRepository|StoryDraftRecord' src/core/domain/
```
