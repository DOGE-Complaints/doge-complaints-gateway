# Acceptance verification — task-gw-draft-05-t03-intake-v2-fixtures-stash-payload

- **Task:** T03 intake v2 fixtures stash payload
- **Status:** PASS
- **Date:** 2026-07-11T07:52:43Z

## Checklist

- [x] `valid_v2_stash_payload()` in `tests/intake_v2_fixtures.py` (no submitter key)

## Evidence

```
python3 -c "from tests.intake_v2_fixtures import valid_v2_stash_payload; assert 'submitter' not in valid_v2_stash_payload()" → ok
```
