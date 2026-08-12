# task-gw-draft-02-t07-story-acceptance-gate

## Meta
- **Story:** [STORY-GW-DRAFT-02](../STORY-GW-DRAFT-02-browser-submit-verification-gate.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000044
- **Skill declared:** python-pro
- **Depends on:** T01–T06

## Purpose
Story acceptance gate: all 6 parent AC verified; `POST /story-drafts/{draft_id}/submit` end-to-end with identity `/me` path.

## Code Facts
- Parent AC — [`STORY-GW-DRAFT-02-browser-submit-verification-gate.md`](../STORY-GW-DRAFT-02-browser-submit-verification-gate.md) §Acceptance Criteria
- Active pkg — [`pkg-000044-20260703-gw-draft-02-browser-submit-verification-gate.yaml`](../../../../../../gateway-active-packages/pkg-000044-20260703-gw-draft-02-browser-submit-verification-gate.yaml)
- Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)

## Acceptance / DoD
- All 6 parent AC PASS in `story-acceptance-gate-STORY-GW-DRAFT-02.md`
- `builder_resolve_queue --project gateway --verify` → ok 7 paths
- T01–T06 acceptance artifacts referenced in gate
- Full unit suite 0 failed (GW-DRAFT-01 audit precedent)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- `story-acceptance-gate-STORY-GW-DRAFT-02.md` (gate Date after live verify only)
- `bullrun-launch-index.md` story row

## Out of scope
EPIC-M2-21 epic closure; GW-DRAFT-03/04

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_draft_02_story_draft_submit_contract.py
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest --ignore=tests/integration --ignore=tests/smoke -q
```
