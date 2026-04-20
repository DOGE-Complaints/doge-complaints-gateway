# STORY-M2-06-02: i18n projection policy

## Meta
- Key: `STORY-M2-06-02`
- Parent Epic: [`EPIC-M2-06-spa-projection-and-i18n.md`](../../EPIC-M2-06-spa-projection-and-i18n.md)
- Type: Technical Story
- Status: Done (Committed)
- Stream: M2 Projection
- Skill declared: `python-pro` (for runtime implementation phase)

## Story Goal
Реализовать `I18nText` и политику fallback `summary` ← `title` по локалям.

## AC / DoD
- [x] Обязательные локали `et`, `ru`, `en` для текстовых полей.
- [x] Пустые строки в summary заменяются title для соответствующей локали.
- [x] Версия политики зафиксирована (`PROJECTION_POLICY_VERSION`).

## Task Artifacts
- Task workspace: [`../../../task-m2-06-02-i18n-projection-policy/README.md`](../../../task-m2-06-02-i18n-projection-policy/README.md)
- Task specification: [`../../../task-m2-06-02-i18n-projection-policy/task-m2-06-02-i18n-projection-policy.md`](../../../task-m2-06-02-i18n-projection-policy/task-m2-06-02-i18n-projection-policy.md)
- Phase log: [`../../../task-m2-06-02-i18n-projection-policy/BULLRUN-PHASE-LOG.md`](../../../task-m2-06-02-i18n-projection-policy/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-06-02-i18n-projection-policy/acceptance-verification-STORY-M2-06-02.md`](../../../task-m2-06-02-i18n-projection-policy/acceptance-verification-STORY-M2-06-02.md)
