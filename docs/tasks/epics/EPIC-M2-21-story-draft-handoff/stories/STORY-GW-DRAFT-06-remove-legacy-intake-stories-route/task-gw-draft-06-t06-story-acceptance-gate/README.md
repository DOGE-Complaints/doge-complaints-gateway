# task-gw-draft-06-t06-story-acceptance-gate

## Meta
- **Story:** [STORY-GW-DRAFT-06](../STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md)
- **Type:** tests
- **Status:** ⚪ Todo
- **Package:** pkg-000050
- **Skill declared:** python-pro
- **Depends on:** T01–T05

## Purpose
Backlog T05 (story gate): verify legacy public intake route removed; runner on story-drafts; internal intake only; OpenAPI clean; GW-DRAFT-01/02 + full pytest green.

## Code Facts
- Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Parent AC — 5 bullets verbatim in pipeline story
- Contract evidence — `tests/test_gw_draft_01_*`, `tests/test_gw_draft_02_*`

## Acceptance / DoD
- [ ] All 5 parent AC signed in [`story-acceptance-gate-STORY-GW-DRAFT-06.md`](./story-acceptance-gate-STORY-GW-DRAFT-06.md)
- [ ] `rg 'POST /intake/stories|"/intake/stories"' src/` = 0
- [ ] `rg '"/intake/stories"' tests/` = 0
- [ ] `--verify --check-dates` ok for pkg-000050
- [ ] BULLRUN phases complete
- [ ] Gate Date only after live verify in P3

## Where to change
- [`story-acceptance-gate-STORY-GW-DRAFT-06.md`](./story-acceptance-gate-STORY-GW-DRAFT-06.md)
- [`acceptance-verification-gw-draft-06-t06.md`](./acceptance-verification-gw-draft-06-t06.md)

## Out of scope
- GW-SEED-01 runner submit/cluster path
- 410 Gone redirect on removed route

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && rg 'POST /intake/stories|"/intake/stories"' src/ || test $? -eq 1
cd doge-complaints-gateway && rg '"/intake/stories"' tests/ || test $? -eq 1
cd doge-complaints-gateway && rg '/intake/stories' tests/simulation_runner.py || test $? -eq 1
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_draft_01_story_draft_stash_contract.py tests/test_gw_draft_02_story_draft_submit_contract.py
```
