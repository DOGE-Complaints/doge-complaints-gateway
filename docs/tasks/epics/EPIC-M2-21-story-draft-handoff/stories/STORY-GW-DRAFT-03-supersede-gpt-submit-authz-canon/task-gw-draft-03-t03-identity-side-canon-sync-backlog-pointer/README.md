# task-gw-draft-03-t03-identity-side-canon-sync-backlog-pointer

## Meta
- **Story:** [STORY-GW-DRAFT-03](../STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000045
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
D-DRAFT-5 **D:** завести identity-side backlog-задачу на правку `04-security.md` §A + `09-gateway-expectations.md`; в gateway оставить указатель «канон identity рассинхронизирован».

## Code Facts
- Identity canon (не правим здесь) — [`04-security.md`](../../../../../../../../doge-identity-service/docs/runtime-docs/04-security.md) §A шаги 6–8
- Identity expectations — [`09-gateway-expectations.md`](../../../../../../../../doge-identity-service/docs/runtime-docs/09-gateway-expectations.md) L13–18 («GPT сам шлёт… напрямую в gateway»)
- Gateway browser-submit as-built — GW-DRAFT-02 commits + [`API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) §6.8
- Identity backlog root — [`doge-identity-service/docs/tasks/backlog-stories/INDEX.md`](../../../../../../../../doge-identity-service/docs/tasks/backlog-stories/INDEX.md)

## Acceptance / DoD
- Traces parent AC#4: identity-side задача заведена; gateway не редактирует чужой канон
- **Создать** `doge-identity-service/docs/tasks/backlog-stories/story-draft-handoff/STORY-IDS-DOC-DRAFT-05-browser-submit-security-canon-sync.md` — Meta, Scope (`04-security.md` §A + `09-gateway-expectations.md` submit block), AC, ссылка на GW-DRAFT-03 + D-DRAFT-5
- **Обновить** [`doge-identity-service/docs/tasks/backlog-stories/INDEX.md`](../../../../../../../../doge-identity-service/docs/tasks/backlog-stories/INDEX.md) — строка темы `story-draft-handoff/` + STORY-IDS-DOC-DRAFT-05
- **Gateway pointer** в [`security-env-api-access.md`](../../../../../../../docs/runtime-docs/security-env-api-access.md) или `architecture-and-layers-as-is.md`: «identity canon temporarily out of sync; see STORY-IDS-DOC-DRAFT-05»
- **Не редактировать** `04-security.md` / `09-gateway-expectations.md` в этой волне
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3)

## Where to change
- **Create:** `doge-identity-service/docs/tasks/backlog-stories/story-draft-handoff/STORY-IDS-DOC-DRAFT-05-browser-submit-security-canon-sync.md`
- **Update:** `doge-identity-service/docs/tasks/backlog-stories/INDEX.md`
- **Update (gateway pointer):** [`docs/runtime-docs/security-env-api-access.md`](../../../../../../../docs/runtime-docs/security-env-api-access.md) or [`architecture-and-layers-as-is.md`](../../../../../../../docs/runtime-docs/architecture-and-layers-as-is.md)

## Out of scope
- Правка identity `04-security.md` / `09-gateway-expectations.md` runtime-docs
- Удаление GAUTH code (GW-DRAFT-04)

## Verification commands
```bash
test -f doge-identity-service/docs/tasks/backlog-stories/story-draft-handoff/STORY-IDS-DOC-DRAFT-05-browser-submit-security-canon-sync.md
rg 'STORY-IDS-DOC-DRAFT-05|рассинхрон' doge-complaints-gateway/docs/runtime-docs/
rg 'DOC-DRAFT-05' doge-identity-service/docs/tasks/backlog-stories/INDEX.md
```
