# task-gw-draft-06-t08-audit-g2-stale-intake-comment-cleanup

## Meta
- **Story:** [STORY-GW-DRAFT-06](../STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md)
- **Type:** fix
- **Status:** 🟢 Done
- **Package:** audit override (not in pkg-000050)
- **Skill declared:** python-pro
- **Wave:** audit override (`run_mode=gw_draft_06_audit_followup`)
- **Depends on:** T01–T06 (P3 Done)
- **Audit ref:** [`audit-gw-draft-06-remove-legacy-intake-stories-route-2026-07-11`](../../../../../../analysis/audit-gw-draft-06-remove-legacy-intake-stories-route-2026-07-11.md) **G2**

## Purpose
Заменить устаревший текст про `POST /intake/stories` в комментарии live-integration теста на актуальный: stash-only runner / `InMemoryStoryRepository` не пишет в Supabase.

## Code Facts
- Stale comment — [`test_supabase_dotenv_connectivity.py:68-70`](../../../../../../../tests/integration/supabase/test_supabase_dotenv_connectivity.py) mentions `POST /intake/stories`
- Legacy route removed — P3 T01; public GPT write = `POST /story-drafts`
- Ignore — [`tests/smoke/TODO.md`](../../../../../../../tests/smoke/TODO.md) (temporary working doc, out of scope)

## Acceptance / DoD
- [x] Comment text no longer references `POST /intake/stories` or `"/intake/stories"`
- [x] Wording reflects stash-only / in_memory persistence semantics
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-draft-06-t08.md`](./acceptance-verification-gw-draft-06-t08.md) signed (Date post P6 verify only)

## Where to change
- `doge-complaints-gateway/tests/integration/supabase/test_supabase_dotenv_connectivity.py` — lines 68–70

## Out of scope
- [`tests/smoke/TODO.md`](../../../../../../../tests/smoke/TODO.md)
- Runtime-docs manuals/bootstrap stale mentions (P3 follow-up list)
- Hosted smoke

## Verification commands
```bash
cd doge-complaints-gateway && rg '"/intake/stories"|POST /intake/stories' tests/integration/supabase/test_supabase_dotenv_connectivity.py || test $? -eq 1
cd doge-complaints-gateway && python3 -m pytest -q tests/integration/supabase/test_supabase_dotenv_connectivity.py -m live_integration
# live_integration optional offline; grep = 0 required
```
