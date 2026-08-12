# task-gw-tax-01-t06-legacy-flat-labels-fallback-compat

## Meta
- **Story:** [STORY-GW-TAX-01](../STORY-GW-TAX-01-taxonomy-persistence-fidelity.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000054
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Legacy-совместимость (backlog §5): плоские `narrative_canonical_labels` → fallback axis-маппинг через `infer_signals_from_canonical`; старые истории не ломаются.

## Code Facts
- Axis re-guess via dictionaries — [`enrichment.py:37-79`](../../../../../../../../src/core/profile/enrichment.py#L37) `infer_signals_from_canonical`
- Flat storage on record — [`contracts.py:61`](../../../../../../../../src/core/domain/contracts.py#L61) `narrative_canonical_labels`
- ~8 axes → `unknown` when vocab miss (backlog §33)

## Acceptance / DoD
- [ ] Traces parent AC-4: legacy flat-label stories remain readable
- [ ] Scope trace: backlog §5 compatibility
- [ ] Per-axis payload does not re-guess axis via dictionaries (invariant for T08 grep)
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-tax-01-t06.md`](./acceptance-verification-gw-tax-01-t06.md) signed (Date post live-run only)

## Where to change
- [`src/core/profile/enrichment.py`](../../../../../../../../src/core/profile/enrichment.py)
- (coordination) intake legacy path in T01

## Out of scope
- GW-TAX-02 signal source switch to `story_labels`
- Breaking removal of `narrative_canonical_labels`

## Verification commands (post live-run only)
```bash
rg -n "infer_signals_from_canonical" doge-complaints-gateway/src/core/profile/enrichment.py
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_tax_01_* -m "not live_integration" -k legacy
```
