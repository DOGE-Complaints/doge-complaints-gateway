# task-gw-draft-01-t07-story-acceptance-gate

## Meta
- **Story:** [STORY-GW-DRAFT-01](../STORY-GW-DRAFT-01-story-draft-stash.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000043
- **Skill declared:** python-pro
- **Depends on:** T01–T06

## Purpose
Story acceptance gate: all 6 parent AC verified; separate `StoryDraftRepository`; draft stash end-to-end.

## Code Facts
- Parent AC — [`STORY-GW-DRAFT-01-story-draft-stash.md`](../STORY-GW-DRAFT-01-story-draft-stash.md) §Acceptance Criteria
- Active pkg — [`pkg-000043-20260703-gw-draft-01-story-draft-stash.yaml`](../../../../../../gateway-active-packages/pkg-000043-20260703-gw-draft-01-story-draft-stash.yaml)
- Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)

## Acceptance / DoD
- All 6 parent AC PASS in `story-acceptance-gate-STORY-GW-DRAFT-01.md`
- `builder_resolve_queue --project gateway --verify` → ok 7 paths
- T01–T06 acceptance artifacts referenced in gate
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- `story-acceptance-gate-STORY-GW-DRAFT-01.md` (gate Date after live verify only)
- `bullrun-launch-index.md` story row

## Out of scope
EPIC-M2-21 epic closure; GW-DRAFT-02

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_draft_01_story_draft_stash_contract.py
```

> **Note (T09):** structural regression scope superseded — full unit suite in [`story-acceptance-gate-STORY-GW-DRAFT-01.md`](./story-acceptance-gate-STORY-GW-DRAFT-01.md) (561 passed, 2026-07-03).
