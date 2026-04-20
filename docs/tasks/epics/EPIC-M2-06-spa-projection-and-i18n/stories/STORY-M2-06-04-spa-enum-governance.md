# STORY-M2-06-04: SPA enum governance checks

## Meta
- Key: `STORY-M2-06-04`
- Parent Epic: [`EPIC-M2-06-spa-projection-and-i18n.md`](../../EPIC-M2-06-spa-projection-and-i18n.md)
- Type: Technical Story
- Status: Done (Committed)
- Stream: M2 Projection
- Skill declared: `python-pro` (for runtime implementation phase)

## Story Goal
Ввести управляемые наборы `status`, `type`, `labels` и валидацию optional tx полей без фиктивных txid.

## AC / DoD
- [x] Невалидные enum значения отклоняются.
- [x] Очевидные placeholder txid отклоняются; пустые optional — omit/null семантика.
- [x] Unit tests на негативные кейсы.

## Task Artifacts
- Task workspace: [`../../../task-m2-06-04-spa-enum-governance/README.md`](../../../task-m2-06-04-spa-enum-governance/README.md)
- Task specification: [`../../../task-m2-06-04-spa-enum-governance/task-m2-06-04-spa-enum-governance.md`](../../../task-m2-06-04-spa-enum-governance/task-m2-06-04-spa-enum-governance.md)
- Phase log: [`../../../task-m2-06-04-spa-enum-governance/BULLRUN-PHASE-LOG.md`](../../../task-m2-06-04-spa-enum-governance/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-06-04-spa-enum-governance/acceptance-verification-STORY-M2-06-04.md`](../../../task-m2-06-04-spa-enum-governance/acceptance-verification-STORY-M2-06-04.md)
