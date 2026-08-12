# task-gw-draft-05-t08-story-acceptance-gate

## Meta
- **Story:** [STORY-GW-DRAFT-05](../STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000049
- **Skill declared:** python-pro
- **Depends on:** T01–T07

## Purpose
Backlog T08 (story gate): verify dual-contract refactor complete — honest AC1 grep; contract tests for stash/submit; all parent AC signed.

## Code Facts
- Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Honest AC1 — audit G1 closed in T09; legacy literal only in [`contracts.py`](../../../../../../../src/core/intake/contracts.py) tolerant-read
- Contract evidence — `tests/test_gw_draft_01_*`, `tests/test_gw_draft_02_*`, `tests/test_story_intake_contract.py`

## Acceptance / DoD
- [x] All 6 parent AC checkboxes signed in [`story-acceptance-gate-STORY-GW-DRAFT-05.md`](./story-acceptance-gate-STORY-GW-DRAFT-05.md)
- [x] `rg 'STASH_PENDING|require_submitter|\bstash_pending\b' src/ tests/` = 0; legacy literal scoped to tolerant-read only
- [x] Contract tests: POST `/story-drafts` without submitter → 201; submit → 202 + authoritative author (GW-DRAFT-01/02)
- [x] `--verify --check-dates` ok for pkg-000049
- [x] BULLRUN phases complete
- [x] Gate Date only after live verify in P6

## Where to change
- [`story-acceptance-gate-STORY-GW-DRAFT-05.md`](./story-acceptance-gate-STORY-GW-DRAFT-05.md)
- [`acceptance-verification-gw-draft-05-t08.md`](./acceptance-verification-gw-draft-05-t08.md)

## Out of scope
- GW-DRAFT-06 legacy route removal; new features

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && rg 'STASH_PENDING|require_submitter|\bstash_pending\b' src/ tests/ || test $? -eq 1
cd doge-complaints-gateway && rg '__stash_pending_author__' src/core/intake/contracts.py
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_draft_01_story_draft_stash_contract.py tests/test_gw_draft_02_story_draft_submit_contract.py tests/test_story_intake_contract.py
```
