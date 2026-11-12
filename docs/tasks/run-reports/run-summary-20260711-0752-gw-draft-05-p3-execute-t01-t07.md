# run-summary-20260711-0752-gw-draft-05-p3-execute-t01-t07

**Date:** 2026-07-11  
**Story:** STORY-GW-DRAFT-05 dual intake contract (stash vs submit)  
**Package:** pkg-000049 (immutable YAML; build window flat 1–7)  
**Result:** PASS (T01–T07); T08 story gate **pending** (outside build window slice)

## Summary

Dual-contract refactor: GPT stash uses `StoryDraftStashRequest` (no submitter); browser submit bridges to `StoryIntakeRequest` with authoritative author from identity `/me`. Removed `STASH_PENDING_EXTERNAL_USER_ID`, `require_submitter`, and `stash_pending` handler branch. Legacy placeholder drafts: tolerant read on submit (T02 decision).

## Tasks closed

| Task | Deliverable |
|------|-------------|
| T01 | Domain: `StoryDraftStashRequest`, `_parse_story_envelope_body`, bridge, cleanup exports |
| T02 | Handlers wired; backward-compat decision = tolerant read |
| T03 | `valid_v2_stash_payload()` fixture |
| T04 | Contract + GW-DRAFT-01/02/get-auth regression tests updated |
| T05 | Runtime OpenAPI `StoryDraftStashRequest` on POST/GET draft |
| T06 | API_REFERENCE §6.8, security §1.1, architecture, persistence model |
| T07 | INDEX row + GW-DRAFT-01 cross-ref verified |

## Verification

```
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify → ok 8 paths
cd doge-complaints-gateway && rg 'STASH_PENDING|require_submitter|__stash_pending' src/ tests/ || test $? -eq 1 → ok
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration" → 569 passed, 12 skipped
```

## Next

- **T08** story acceptance gate: hosted smoke `POST /story-drafts` without submitter → 201; browser submit → 202; sign story gate + `--verify --check-dates`
