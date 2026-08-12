# task-gw-draft-03-t01-gpt-submit-authz-superseded-index

## Meta
- **Story:** [STORY-GW-DRAFT-03](../STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000045
- **Skill declared:** python-pro
- **Depends on:** —

## Purpose
D-DRAFT-5 **A** + **B:** добавить блок «Superseded by story-draft-handoff» в [`gpt-submit-authz/INDEX.md`](../../../../../../backlog-stories/gpt-submit-authz/INDEX.md); развести осиротевшее (GAUTH-01, GPT-two-token) и переиспользуемое (GAUTH-03/04 → GW-DRAFT-02).

## Code Facts
- Старый канон two-token — [`gpt-submit-authz/INDEX.md`](../../../../../../backlog-stories/gpt-submit-authz/INDEX.md) L15–16 («GPT шлёт историю напрямую в gateway с двумя токенами»)
- GAUTH stories Done — pkg-000039..042 (история сохраняется, D-DRAFT-6)
- Реюз GAUTH-03/04 — [`verification_gate.py`](../../../../../../../src/core/identity/verification_gate.py), [`authoritative_submitter.py`](../../../../../../../src/core/identity/authoritative_submitter.py); GW-DRAFT-02 [`audit-gw-draft-02`](../../../../../../../analysis/audit-gw-draft-02-browser-submit-verification-gate-2026-07-03.md) §5
- Browser-submit SSOT — [`story-draft-handoff/INDEX.md`](../../../../../../backlog-stories/story-draft-handoff/INDEX.md)

## Acceptance / DoD
- Traces parent AC#1: `gpt-submit-authz/INDEX.md` явно помечает superseded-часть
- Traces parent AC#2: GAUTH-04 + verification_required-канон связаны с `story-draft-handoff/`
- Блок «Superseded» вверху INDEX: GAUTH-01 + GPT-two-token submit flow
- GAUTH-03/04 помечены «still valid, reused in GW-DRAFT-02»
- Ссылка на [`story-draft-handoff/INDEX.md`](../../../../../../backlog-stories/story-draft-handoff/INDEX.md)
- **Не удалять** строки pkg/аудитов/истории (D-DRAFT-6, AC#5)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3)

## Where to change
- [`docs/tasks/backlog-stories/gpt-submit-authz/INDEX.md`](../../../../../../backlog-stories/gpt-submit-authz/INDEX.md)

## Out of scope
- Правка individual GAUTH backlog stories (→ T04 при необходимости)
- Удаление EPIC-M2-20 pipeline stories / audit files
- Identity runtime-docs

## Verification commands
```bash
rg -i 'superseded|story-draft-handoff' doge-complaints-gateway/docs/tasks/backlog-stories/gpt-submit-authz/INDEX.md
```
