# task-gw-draft-06-t03-simulation-runner-story-drafts-stash

## Meta
- **Story:** [STORY-GW-DRAFT-06](../STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md)
- **Type:** fix
- **Status:** ⚪ Todo
- **Package:** pkg-000050
- **Skill declared:** python-pro
- **Depends on:** T01 (route may still exist during dev; target state stash-only)

## Purpose
Backlog T03: migrate [`simulation_runner.py`](../../../../../../../../tests/simulation_runner.py) from `POST /intake/stories` to `POST /story-drafts` with **stash-only** payload (no submitter, GW-DRAFT-05); expect **201** + `draft_id`. Update [`simulation-runner-manual.md`](../../../../../../../runtime-docs/testing/simulation-runner-manual.md). Full submit/cluster → [GW-SEED-01](../../../../../../backlog-stories/demo-data-seeding/STORY-GW-SEED-01-loader-and-hosted-readiness.md).

## Code Facts
- Current target URL — [`simulation_runner.py:207`](../../../../../../../../tests/simulation_runner.py) `{gateway_url}/intake/stories`
- Payload includes submitter — [`simulation_runner.py:99`](../../../../../../../../tests/simulation_runner.py) `_scenario_to_payload`
- Stash fixture pattern — [`intake_v2_fixtures.py`](../../../../../../../../tests/intake_v2_fixtures.py) `valid_v2_stash_payload()`
- Success today expects 202 + story_id — [`simulation_runner.py:211`](../../../../../../../../tests/simulation_runner.py)

## Acceptance / DoD
- [ ] Traces parent AC #2: runner uses `/story-drafts`, not `/intake/stories`
- [ ] Stash payload without submitter; success = 201 + `draft_id`
- [ ] Manual doc updated; SEED-01 follow-up noted for submit/cluster
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-draft-06-t03.md`](./acceptance-verification-gw-draft-06-t03.md) signed (Date post P3 verify only)

## Where to change
- `doge-complaints-gateway/tests/simulation_runner.py`
- `doge-complaints-gateway/docs/runtime-docs/testing/simulation-runner-manual.md`

## Out of scope
- Browser submit flow in runner (SEED-01)
- Route removal (T01); bulk test migration (T05)

## Verification commands
```bash
cd doge-complaints-gateway && rg '/intake/stories' tests/simulation_runner.py || test $? -eq 1
cd doge-complaints-gateway && rg '/story-drafts' tests/simulation_runner.py
```
