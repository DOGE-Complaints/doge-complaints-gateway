# task-gw-tax-01-t01-intake-per-axis-taxonomy-contract

## Meta
- **Story:** [STORY-GW-TAX-01](../STORY-GW-TAX-01-taxonomy-persistence-fidelity.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000054
- **Skill declared:** python-pro
- **Depends on:** —

## Purpose
Intake-контракт (D-TAX-1): приём `narrative.taxonomy = {axis:[{label,disposition}]}` per-axis; legacy flat `canonical_labels` fallback через словари; валидация axis/disposition enum.

## Code Facts
- Плоский `canonical_labels` only — [`intake/contracts.py:294-318`](../../../../../../../../src/core/intake/contracts.py#L294)
- `Narrative` model — [`intake/contracts.py`](../../../../../../../../src/core/intake/contracts.py) — поля `taxonomy` **отсутствует**
- disposition enum (target): `canonical | metadata_only | needs_clarification | rejected | internal` (backlog §3)

## Acceptance / DoD
- [ ] Traces parent AC-1: per-axis taxonomy accepted; axis from contract, not guessed
- [ ] Scope trace: backlog §1 Intake D-TAX-1
- [ ] Legacy flat `canonical_labels` still accepted (backward compat)
- [ ] axis/disposition enum validation
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-tax-01-t01.md`](./acceptance-verification-gw-tax-01-t01.md) signed (Date post live-run only)

## Where to change
- [`src/core/intake/contracts.py`](../../../../../../../../src/core/intake/contracts.py)

## Out of scope
- Domain `StoryLabel` / repository (T02)
- Persist on submit (T04)
- GPT-TAX-01 producer contract (GPT UI)

## Verification commands (post live-run only)
```bash
rg -n "taxonomy|disposition" doge-complaints-gateway/src/core/intake/contracts.py
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_tax_01_* -m "not live_integration" -k intake
```
