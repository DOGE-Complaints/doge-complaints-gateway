# Acceptance verification — task-gw-draft-06-t03-simulation-runner-story-drafts-stash

- **Task:** T03 simulation runner story-drafts stash
- **Status:** PASS
- **Date:** 2026-07-11T10:15:42Z

## Checklist

- [x] Runner uses `/story-drafts`, not `/intake/stories`
- [x] Stash payload without submitter; success = 201 + `draft_id`
- [x] Manual doc updated; SEED-01 follow-up noted

## Evidence

```
cd doge-complaints-gateway && rg '/intake/stories' tests/simulation_runner.py || test $? -eq 1 → ok
cd doge-complaints-gateway && rg '/story-drafts' tests/simulation_runner.py → POST target + 201 branch
```
