# task-gw-draft-03-t04-grep-doc-consistency-no-dual-truth

## Meta
- **Story:** [STORY-GW-DRAFT-03](../STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000045
- **Skill declared:** python-pro
- **Depends on:** T02, T03

## Purpose
Grep-верификация «нет двух истин»: пройти ссылки на «GPT сам сабмитит» / `X-User-Token` в gateway runtime-docs; привести к browser-submit или пометить superseded/legacy.

## Code Facts
- Known hits — [`simulation-runner-manual.md`](../../../../../../../docs/runtime-docs/testing/simulation-runner-manual.md): `X-User-Token` для `/intake/stories` (legacy GPT direct path, still valid for that route)
- [`seed-demo-data-runbook-ru.md`](../../../../../../../docs/runtime-docs/manuals/seed-demo-data-runbook-ru.md): двухслойная auth на `/intake/stories`
- [`security-env-api-access.md`](../../../../../../../docs/runtime-docs/security-env-api-access.md) L100: contrast note GPT path vs browser path (GW-DRAFT-02)
- **Exclude** — `docs/tasks/epics/EPIC-M2-20-*`, `docs/analysis/audit-gw-gauth-*` (D-DRAFT-6)

## Acceptance / DoD
- Traces parent AC#3 (вторая половина): нет gateway runtime-docs с «GPT сам сабмитит» без пометки
- Inventory в `acceptance-verification-gw-draft-03-t04.md` или task acceptance: file → action (updated / already OK / excluded)
- `simulation-runner-manual.md` + `seed-demo-data-runbook-ru.md`: legacy GPT `/intake/stories` path помечен; browser-submit = primary user submit
- GAUTH-01/02 backlog stories: superseded banner при необходимости (если grep находит misleading phrasing)
- **Не трогать** EPIC-M2-20 pipeline / audit-gw-gauth-* (AC#5)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3)

## Where to change
- `doge-complaints-gateway/docs/runtime-docs/**` (grep-driven)
- Опционально: [`gpt-submit-authz/STORY-GW-GAUTH-01-two-layer-auth-on-submit.md`](../../../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-01-two-layer-auth-on-submit.md), [`STORY-GW-GAUTH-02-user-token-introspection.md`](../../../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-02-user-token-introspection.md)

## Out of scope
- `src/` changes; identity runtime-docs
- EPIC-M2-20 epic pipeline stories; audit files

## Verification commands
```bash
rg -i 'GPT сам|GPT шлёт.*напрямую|two.token|два токен' doge-complaints-gateway/docs/runtime-docs/
rg -l 'X-User-Token' doge-complaints-gateway/docs/runtime-docs/
```
