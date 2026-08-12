# task-gw-cab-02-t08-first-wins-set-owner-semantics

## Meta
- **Story:** [STORY-GW-CAB-02](../STORY-GW-CAB-02-current-draft-discovery.md)
- **Type:** implement (audit follow-up)
- **Status:** 🟢 Done
- **Package:** pkg-000053 (audit follow-up; **run_mode override**, no pkg change)
- **Skill declared:** python-pro
- **Audit report:** [`docs/analysis/audit-gw-cab-02-current-draft-discovery-2026-07-14.md`](../../../../../../analysis/audit-gw-cab-02-current-draft-discovery-2026-07-14.md)
- **Gap ID:** G1 (MEDIUM)
- **Decision:** first-wins в коде (align D-CAB02-1 / backlog privacy «первый читатель = владелец»)

## Purpose
**Исторический gap (закрыт T08):** `DraftOwnerRepository.set_owner` был **last-writer-wins**; приведён к **first-wins** — первый authenticated reader фиксирует `draft_id→sub`, последующие read другими `sub` не перезаписывают owner. **Текущий код (verified):** DO NOTHING / `setdefault` / `ignore-duplicates`. Capability-модель (нет owner-gate на GET) — отдельно: [DOC-TASK-DRAFT-OWNERSHIP-01](../../../../../../backlog-stories/cabinet-api/DOC-TASK-DRAFT-OWNERSHIP-01-clarify-capability-model.md).

## Code Facts (pre-fix snapshot — superseded by Done)
- sqlite было `ON CONFLICT … DO UPDATE` → сейчас `DO NOTHING`
- in-memory было unconditional assign → сейчас `setdefault`
- supabase было `merge-duplicates` → сейчас `ignore-duplicates`

## Gap
- **G1 (MEDIUM):** ownership-hijack при утечке `draft_id` — last-wins против документированной модели.

## AC/DoD
- [x] sqlite: `ON CONFLICT(draft_id) DO NOTHING` (или эквивалент first-wins)
- [x] in-memory: `setdefault` / guard — не перезаписывать существующего owner
- [x] supabase: `prefer=resolution=ignore-duplicates,return=minimal`
- [x] Optional: docstring `DraftOwnerRepository.set_owner` в [`contracts.py`](../../../../../../../../src/core/domain/contracts.py) — first-wins idempotent
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-cab-02-t08.md`](./acceptance-verification-gw-cab-02-t08.md) signed (Date post live-run only)

## Where to change
- [`src/core/infrastructure/db_sqlite.py`](../../../../../../../../src/core/infrastructure/db_sqlite.py) — `SqliteDraftOwnerRepository.set_owner`
- [`src/core/infrastructure/repositories.py`](../../../../../../../../src/core/infrastructure/repositories.py) — `InMemoryDraftOwnerRepository.set_owner`
- [`src/core/infrastructure/db_supabase.py`](../../../../../../../../src/core/infrastructure/db_supabase.py) — `SupabaseDraftOwnerRepository.set_owner`
- (optional) [`src/core/domain/contracts.py`](../../../../../../../../src/core/domain/contracts.py)

## Out of scope
- Owner-gated read on `GET /story-drafts/{id}` (наследие GW-DRAFT-02)
- Новые routes / миграции схемы (PK `draft_id` уже unique)

## Verification commands (post live-run only)
```bash
rg -n "DO NOTHING|setdefault|ignore-duplicates" doge-complaints-gateway/src/core/infrastructure/
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_cab_02_current_draft_discovery.py -m "not live_integration"
```
