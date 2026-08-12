# task-gw-cab-02-t01-domain-updated-at-and-draft-owner-repository

## Meta
- **Story:** [STORY-GW-CAB-02](../STORY-GW-CAB-02-current-draft-discovery.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000053
- **Skill declared:** python-pro
- **Depends on:** —

## Purpose
Домен: добавить `updated_at` на `StoryDraftRecord` (D-CAB02-2) и новый порт `DraftOwnerRepository` с `set_owner` / `get_current_draft` (backlog A.1–A.2). Блокирует T02–T04.

## Code Facts
- `StoryDraftRecord` без `updated_at` и owner — [`contracts.py:113-120`](../../../../../../../../src/core/domain/contracts.py#L113)
- `StoryDraftRepository` protocol — [`contracts.py:122-134`](../../../../../../../../src/core/domain/contracts.py#L122)
- `draft_owner` / `DraftOwnerRepository` — **отсутствует** в `src/`

## Acceptance / DoD
- [x] Traces parent AC-5: `updated_at` на `StoryDraftRecord`
- [x] Traces parent AC-1..4: `DraftOwnerRepository` protocol с `set_owner(draft_id, sub)` и `get_current_draft(sub) -> StoryDraftRecord | None`
- [x] Scope trace: backlog §A.1–A.2 (D-CAB02-2, D-CAB02-3 query contract)
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-cab-02-t01.md`](./acceptance-verification-gw-cab-02-t01.md) signed

## Where to change
- [`src/core/domain/contracts.py`](../../../../../../../../src/core/domain/contracts.py) — `StoryDraftRecord.updated_at`, `DraftOwnerRepository`

## Out of scope
- Persistence adapters (T02)
- HTTP handlers/routes (T03–T04)

## Verification commands
```bash
rg 'DraftOwnerRepository|updated_at' doge-complaints-gateway/src/core/domain/contracts.py
```
