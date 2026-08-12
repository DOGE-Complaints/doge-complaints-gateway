# task-gw-gauth-04-t06

## Meta
- **Story:** [STORY-GW-GAUTH-04](../STORY-GW-GAUTH-04-authoritative-author-from-introspection.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000042
- **Skill declared:** python-pro
- **Depends on:** T01–T05

## Purpose
Story acceptance gate: all parent AC verified; authoritative author from introspection wired on verify-gated intake.

## Code Facts
- Parent AC — [`STORY-GW-GAUTH-04-authoritative-author-from-introspection.md`](../STORY-GW-GAUTH-04-authoritative-author-from-introspection.md) §Acceptance Criteria
- Active pkg — [`pkg-000042-20260625-gw-gauth-04-authoritative-author-introspection.yaml`](../../../../../../gateway-active-packages/pkg-000042-20260625-gw-gauth-04-authoritative-author-introspection.yaml)
- Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- req-19 §5 — [`19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md`](../../../../../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md)

## Acceptance / DoD
- All 4 parent AC PASS in [`story-acceptance-gate-STORY-GW-GAUTH-04.md`](./story-acceptance-gate-STORY-GW-GAUTH-04.md)
- `builder_resolve_queue --project gateway --verify` → ok 6 paths
- T01–T05 acceptance artifacts referenced in gate
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- `story-acceptance-gate-STORY-GW-GAUTH-04.md` (gate Date after live verify only)
- `bullrun-launch-index.md` story row

## Out of scope
- EPIC-M2-20 epic closure
- GPT Actions OpenAPI update

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_gauth_04_authoritative_author_contract.py
```
