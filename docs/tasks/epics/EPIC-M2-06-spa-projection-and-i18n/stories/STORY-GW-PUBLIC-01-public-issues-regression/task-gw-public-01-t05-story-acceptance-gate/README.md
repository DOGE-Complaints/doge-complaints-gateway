# task-gw-public-01-t05

## Meta
- **Story:** [STORY-GW-PUBLIC-01](../STORY-GW-PUBLIC-01-public-issues-regression.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000048
- **Skill declared:** python-pro
- **Depends on:** T01–T04

## Purpose
Story acceptance gate: all parent AC verified; M-5 regression guard in offline suite.

## Code Facts
- Parent AC — [`STORY-GW-PUBLIC-01-public-issues-regression.md`](../STORY-GW-PUBLIC-01-public-issues-regression.md) §Acceptance Criteria
- Active pkg — [`pkg-000048-20260710-gw-public-01-public-issues-regression.yaml`](../../../../../../gateway-active-packages/pkg-000048-20260710-gw-public-01-public-issues-regression.yaml)
- Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Test module — [`tests/test_gw_public_01_public_issues_regression.py`](../../../../../../../../tests/test_gw_public_01_public_issues_regression.py)

## Acceptance / DoD
- [ ] All 3 parent AC PASS in [`story-acceptance-gate-STORY-GW-PUBLIC-01.md`](./story-acceptance-gate-STORY-GW-PUBLIC-01.md)
- [ ] T01–T04 acceptance artifacts referenced in gate
- [ ] `builder_resolve_queue --project gateway --verify` → ok 5 paths
- [ ] Offline pytest suite green
- [ ] Gate Date only after verify in P3/P6

## Where to change
- `story-acceptance-gate-STORY-GW-PUBLIC-01.md` (gate Date after verify only)
- `bullrun-launch-index.md` story row

## Out of scope
- Hosted E2E
- `src/core/` changes

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_public_01_public_issues_regression.py
cd doge-complaints-gateway && python3 -m pytest -q
```
