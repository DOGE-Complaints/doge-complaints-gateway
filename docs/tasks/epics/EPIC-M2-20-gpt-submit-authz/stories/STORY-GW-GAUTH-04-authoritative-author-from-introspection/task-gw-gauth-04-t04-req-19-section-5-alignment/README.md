# task-gw-gauth-04-t04

## Meta
- **Story:** [STORY-GW-GAUTH-04](../STORY-GW-GAUTH-04-authoritative-author-from-introspection.md)
- **Type:** docs
- **Status:** 🔵 Done
- **Package:** pkg-000042
- **Skill declared:** python-pro
- **Depends on:** T01 (mapping policy stable)

## Purpose
Согласовать формулировку авторства с [`req-19 §5`](../../../../../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md): при gateway introspection авторитетен проверенный `sub`, не параллельная модель; уточнение §5.3 без дублирования всего req-19.

## Code Facts
- Current §5.3 «нет подделки с клиента» — [`19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md`](../../../../../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md) §5.3
- Backlog requirement — pipeline story §Требование / целевое состояние

## Acceptance / DoD
- Traces parent AC #3: req-19 §5 states introspected `sub` is authoritative author when gateway introspection succeeds
- Single authorship model (no parallel «payload author» vs «verified author» in product contract)
- **Docs only** — no application code changes in this task
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- [`docs/requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md`](../../../../../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md) — §5 / §5.3 additive clarification

## Out of scope
- Full req-19 rewrite
- OpenAPI schema changes
- GPT Actions update

## Verification commands
```bash
cd doge-complaints-gateway && rg 'introspection|authoritative|sub' docs/requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md -n
```
