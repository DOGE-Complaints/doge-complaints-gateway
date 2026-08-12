# task-gw-draft-03-t06-gauth-reused-discoverability-banners

## Meta
- **Story:** [STORY-GW-DRAFT-03](../STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** audit override (not in pkg-000045)
- **Skill declared:** python-pro
- **Wave:** audit override (`run_mode=gw_draft_03_audit_followup`)
- **Depends on:** T01 (INDEX reused table), T04 (GAUTH-01/02 superseded banners)
- **Audit ref:** [`audit-gw-draft-03-supersede-gpt-submit-authz-canon-2026-07-03`](../../../../../../analysis/audit-gw-draft-03-supersede-gpt-submit-authz-canon-2026-07-03.md) **G2**

## Purpose
Закрыть audit G2: [`gpt-submit-authz/INDEX.md`](../../../../../../backlog-stories/gpt-submit-authz/INDEX.md) уже разводит GAUTH-03/04 как «reused», но сами backlog-стори без шапочного указателя — читатель, попавший прямо на GAUTH-03/04, не видит reuse-контекст. Добавить discoverability-баннер «↔ reused by GW-DRAFT-02» (не superseded — стори валидны).

## Code Facts
- INDEX reused table — [`gpt-submit-authz/INDEX.md:14-17`](../../../../../../backlog-stories/gpt-submit-authz/INDEX.md) GAUTH-03/04 «Still valid — reused»
- GAUTH-01 superseded banner (образец) — [`STORY-GW-GAUTH-01-two-layer-auth-on-submit.md:3`](../../../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-01-two-layer-auth-on-submit.md)
- GAUTH-03 без баннера — [`STORY-GW-GAUTH-03-verification-gate-403.md`](../../../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-03-verification-gate-403.md) L1 сразу `# STORY-GW-GAUTH-03`
- GAUTH-04 без баннера — [`STORY-GW-GAUTH-04-authoritative-author-from-introspection.md`](../../../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-04-authoritative-author-from-introspection.md)
- Reuse в коде — GW-DRAFT-02: `evaluate_verification_gate` (GAUTH-03), `authoritative_submitter_from_introspection` (GAUTH-04) на `POST /story-drafts/{id}/submit`

## Acceptance / DoD
- GAUTH-03: blockquote «↔ Reused (browser submit)» в шапке (после title или перед Meta), ссылка на GW-DRAFT-02 + INDEX
- GAUTH-04: аналогичный reuse-баннер (формулировка под authoritative author)
- **Не** ставить superseded-баннер (GAUTH-03/04 валидны)
- Баннеры согласованы с INDEX «Still valid — reused»
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P6)

## Where to change
- [`docs/tasks/backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-03-verification-gate-403.md`](../../../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-03-verification-gate-403.md)
- [`docs/tasks/backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-04-authoritative-author-from-introspection.md`](../../../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-04-authoritative-author-from-introspection.md)

## Banner template (P6)

GAUTH-03:
```markdown
> **↔ Reused (browser submit):** `evaluate_verification_gate` на `POST /story-drafts/{id}/submit` ([GW-DRAFT-02](../../story-draft-handoff/STORY-GW-DRAFT-02-browser-submit-verification-gate.md)). Разведение: [`gpt-submit-authz/INDEX.md`](./INDEX.md).
```

GAUTH-04:
```markdown
> **↔ Reused (browser submit):** authoritative author (`submitter=sub`) на `POST /story-drafts/{id}/submit` ([GW-DRAFT-02](../../story-draft-handoff/STORY-GW-DRAFT-02-browser-submit-verification-gate.md)). Разведение: [`gpt-submit-authz/INDEX.md`](./INDEX.md).
```

## Out of scope
- Правка [`gpt-submit-authz/INDEX.md`](../../../../../../backlog-stories/gpt-submit-authz/INDEX.md) (уже покрывает reused)
- Identity runtime-docs (G1 → STORY-IDS-DOC-DRAFT-05, `activation: none`)
- Prod-код; pytest

## Verification commands
```bash
rg -i 'Reused \\(browser submit\\)|GW-DRAFT-02' \
  doge-complaints-gateway/docs/tasks/backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-03-verification-gate-403.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-04-authoritative-author-from-introspection.md
```
