# task-gw-draft-01-t09-story-gate-full-unit-suite

## Meta
- **Story:** [STORY-GW-DRAFT-01](../STORY-GW-DRAFT-01-story-draft-stash.md)
- **Type:** process (gate / docs)
- **Status:** 🟢 Done
- **Package:** audit override (not in pkg-000043)
- **Skill declared:** python-pro
- **Wave:** audit override (`run_mode=gw_draft_01_audit_followup`)
- **Depends on:** T08 (full unit green prerequisite)
- **Audit ref:** [`audit-gw-draft-01-story-draft-stash-2026-07-03`](../../../../../../analysis/audit-gw-draft-01-story-draft-stash-2026-07-03.md) **R2**

## Purpose
Ужесточить post-audit verification: structural stories (DI constructor changes) требуют full unit suite в story gate; переподписать gate после закрытия R1.

## Code Facts
- T07 gate commands — только `test_gw_draft_01_story_draft_stash_contract.py` — [`story-acceptance-gate-STORY-GW-DRAFT-01.md`](../task-gw-draft-01-t07-story-acceptance-gate/story-acceptance-gate-STORY-GW-DRAFT-01.md)
- Audit R2: full unit **551 passed / 10 failed** при gate PASS (draft contract only)
- T07 README verification scope superseded для structural regression — ссылка на этот таск

## Acceptance / DoD
- Обновить **Commands** в [`story-acceptance-gate-STORY-GW-DRAFT-01.md`](../task-gw-draft-01-t07-story-acceptance-gate/story-acceptance-gate-STORY-GW-DRAFT-01.md): добавить full unit (`PYTHONPATH=src:. python3 -m pytest -q` по конвенции gateway, исключая smoke/integration если применимо)
- Gate `Result: PASS` только при **0 failed** unit после T08
- `Date:` в gate — только post live-run (`--print-utc-now`)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P6)

## Where to change
- [`task-gw-draft-01-t07-story-acceptance-gate/story-acceptance-gate-STORY-GW-DRAFT-01.md`](../task-gw-draft-01-t07-story-acceptance-gate/story-acceptance-gate-STORY-GW-DRAFT-01.md)
- Опционально: примечание в [`task-gw-draft-01-t07-story-acceptance-gate/README.md`](../task-gw-draft-01-t07-story-acceptance-gate/README.md) — verification scope superseded by T09

## Out of scope
Правка тестового кода (T08); GW-DRAFT-02 user-auth (G1)

## Verification commands
```bash
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```
