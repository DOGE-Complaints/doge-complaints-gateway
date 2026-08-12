# Acceptance verification — task-gw-draft-05-t09-audit-g1-honest-legacy-placeholder-ac

- **Task:** T09 audit G1 honest legacy placeholder + AC1 sync
- **Status:** PASS
- **Date:** 2026-07-11

## Checklist

- [x] `_LEGACY_STASH_PLACEHOLDER_EXTERNAL_USER_ID` — explicit literal (no `"".join`)
- [x] `rg 'STASH_PENDING|require_submitter|\bstash_pending\b'` = 0 in `src/` `tests/` (legacy value not counted as active `stash_pending` token)
- [x] Legacy literal scoped to tolerant-read only (`contracts.py:18` constant; `_normalize_stored_draft_payload` uses constant)
- [x] AC1 / T08 gate grep criteria updated (honest wording)
- [x] Unit test legacy placeholder strip passes (`test_parse_stored_draft_stash_request_strips_legacy_placeholder_submitter`)
- [x] Audit G1 traceability noted ([`audit-gw-draft-05-...`](../../../../../../analysis/audit-gw-draft-05-dual-intake-contract-stash-vs-submit-2026-07-11.md) §G1)

## Live verification (2026-07-11)

```bash
cd doge-complaints-gateway && rg 'STASH_PENDING|require_submitter|\bstash_pending\b' src/ tests/ || test $? -eq 1
cd doge-complaints-gateway && rg '__stash_pending_author__' src/core/intake/contracts.py
cd doge-complaints-gateway && python3 -m pytest -q tests/test_story_intake_contract.py -k legacy
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"
```

→ grep active tokens = 0; legacy literal 1 hit (constant); legacy test 1 passed; **570 passed**, 12 skipped
