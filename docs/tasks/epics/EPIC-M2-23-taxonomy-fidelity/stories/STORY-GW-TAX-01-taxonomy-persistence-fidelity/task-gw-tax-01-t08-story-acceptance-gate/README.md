# task-gw-tax-01-t08-story-acceptance-gate

## Meta
- **Story:** [STORY-GW-TAX-01](../STORY-GW-TAX-01-taxonomy-persistence-fidelity.md)
- **Type:** gate
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000054
- **Skill declared:** python-pro
- **Depends on:** T01–T07

## Purpose
Story acceptance gate: live verify all AC (including AC-5 offline suite), grep-инвариант «ось не пере-угадывается для per-axis payload», sign [`story-acceptance-gate-STORY-GW-TAX-01.md`](./story-acceptance-gate-STORY-GW-TAX-01.md), update bullrun story row.

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Parent AC verbatim — pipeline story §Acceptance Criteria
- pkg — `pkg-000054-20260714-gw-tax-01-taxonomy-persistence-fidelity.yaml`

## Acceptance / DoD
- [ ] All AC-1..AC-5 PASS in gate doc with evidence
- [ ] grep invariant: per-axis payload axis not re-guessed via dictionaries
- [ ] `--verify --check-dates` ok for pkg-000054
- [ ] Offline pytest green
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-tax-01-t08.md`](./acceptance-verification-gw-tax-01-t08.md) signed (Date post live-run only)

## Where to change
- [`story-acceptance-gate-STORY-GW-TAX-01.md`](./story-acceptance-gate-STORY-GW-TAX-01.md)
- [`bullrun-launch-index.md`](../../../../bullrun-launch-index.md) — story row Done

## Verification commands (post live-run only)
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"
rg -n "infer_signals_from_canonical" doge-complaints-gateway/src/core --glob '*.py'
```
