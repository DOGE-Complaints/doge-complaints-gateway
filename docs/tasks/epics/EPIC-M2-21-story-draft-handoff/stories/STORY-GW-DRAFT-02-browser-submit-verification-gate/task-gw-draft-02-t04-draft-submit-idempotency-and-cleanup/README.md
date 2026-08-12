# task-gw-draft-02-t04-draft-submit-idempotency-and-cleanup

## Meta
- **Story:** [STORY-GW-DRAFT-02](../STORY-GW-DRAFT-02-browser-submit-verification-gate.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000044
- **Skill declared:** python-pro
- **Depends on:** T03

## Purpose
Идемпотентность по `draft_id` + удаление/пометка черновика после успешного submit (не переиспользовать протухший). Реюз `IdempotencyRepository`; ключ ← `draft_id`.

## Code Facts
- Idempotency — [`services.py:164+`](../../../../../../../src/core/application/services.py), [`contracts.py:99+`](../../../../../../../src/core/domain/contracts.py) `IdempotencyRepository`
- Draft port — [`contracts.py:119-126`](../../../../../../../src/core/domain/contracts.py) — only `save_draft` / `get_draft` (no delete yet)
- Adapters — [`repositories.py`](../../../../../../../src/core/infrastructure/repositories.py), [`db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py), [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py)

## Acceptance / DoD
- Traces parent AC #4: repeat submit same `draft_id` → same story, no duplicates
- Traces parent AC #5: expired/unknown draft → **404** on submit
- After successful first submit, draft not reusable (delete or equivalent)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py) — optional `delete_draft` on port
- Draft adapters (in_memory/sqlite/supabase)
- [`src/core/api/handlers.py`](../../../../../../../src/core/api/handlers.py) — idempotency_key=`draft_id`

## Out of scope
Contract test file (T05); runtime docs (T06)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'idempotency_key|delete_draft' src/core/
```
