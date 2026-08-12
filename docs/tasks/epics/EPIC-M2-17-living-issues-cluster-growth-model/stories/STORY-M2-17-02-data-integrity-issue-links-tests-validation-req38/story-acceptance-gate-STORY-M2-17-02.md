# Story acceptance gate — STORY-M2-17-02

- **Story:** Data integrity — issue story links, tests, validation (REQ-38)
- **Package:** `pkg-000017-20260517-req38-data-integrity-issue-links.yaml`
- **Result:** PASS
- **Date:** 2026-05-17

## AC checklist (REQ-38 §5)

| AC | Status | Evidence |
|----|--------|----------|
| G-10: `test_living_issues_extend_existing.py` in_memory | PASS | `test_extend_flow_process_story_story_count_three_and_labels_union` |
| G-10: story_count = 3 after extend | PASS | assert `len(promoted_after.story_ids) == 3` |
| G-10: labels union | PASS | `canonical_labels_from_cluster` + projection `payload["labels"]` |
| G-11: table in bootstrap | PASS | pre-existing + index added T02 |
| G-11: lookup via `issue_story_links` | PASS | T03 sqlite/supabase `find_promoted_by_cluster_id` |
| G-12: `validate_arweave_txid` true/false cases | PASS | `test_req38_data_integrity.py` |
| `gateway_resolve_queue.py --verify` ok 5 paths | PASS | pkg-000017 |

## Runtime files

- `tests/test_living_issues_extend_existing.py`
- `tests/test_req38_data_integrity.py`
- `supabase/bootstrap/000_full_init.sql`, `supabase/migrations/20260517_1200_issue_story_links_story_idx.sql`
- `src/core/infrastructure/db_sqlite.py`, `src/core/infrastructure/db_supabase.py`
- `src/core/projection/validation.py`

## Commands

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest -q
```
