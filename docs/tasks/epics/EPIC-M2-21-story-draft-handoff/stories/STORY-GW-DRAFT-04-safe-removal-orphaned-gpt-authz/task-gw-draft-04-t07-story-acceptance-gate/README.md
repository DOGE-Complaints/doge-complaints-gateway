# task-gw-draft-04-t07-story-acceptance-gate

## Meta
- **Story:** [STORY-GW-DRAFT-04](../STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000046
- **Skill declared:** python-pro
- **Depends on:** T01–T06

## Purpose
Backlog T05 (story gate): verified «мёртвого кода нет, живое работает, история цела» — grep orphans = 0; full unit suite green; audits/pkg preserved; GW-DRAFT-02 contract tests pass.

## Code Facts
- History preserve — `docs/analysis/audit-gw-gauth-*`, `pkg-000039..042` (D-DRAFT-6)
- Orphan grep targets — same as T01 symbols in `src/`
- Gate template — [`story-acceptance-gate-STORY-GW-DRAFT-03.md`](../../STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon/task-gw-draft-03-t05-story-acceptance-gate/story-acceptance-gate-STORY-GW-DRAFT-03.md)

## Acceptance / DoD
- All 6 parent AC checkboxes signed in [`story-acceptance-gate-STORY-GW-DRAFT-04.md`](./story-acceptance-gate-STORY-GW-DRAFT-04.md)
- `rg` orphans = 0 in `src/` for removed symbols
- Full unit suite green (baseline was 574)
- `test -f` audits + pkg-000039..042 exist
- `--verify --check-dates` ok for pkg-000046
- BULLRUN phases complete
- Gate Date only after live verify in P3

## Where to change
- [`story-acceptance-gate-STORY-GW-DRAFT-04.md`](./story-acceptance-gate-STORY-GW-DRAFT-04.md)
- [`acceptance-verification-gw-draft-04-t07.md`](./acceptance-verification-gw-draft-04-t07.md)

## Out of scope
New features; identity 04-security sync

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && rg 'IdentityIntrospectionClient|require_user_token|IDENTITY_INTROSPECT_URL' src/ || test $? -eq 1
cd doge-complaints-gateway && pytest -q
ls docs/analysis/audit-gw-gauth-*.md docs/tasks/gateway-active-packages/pkg-000039*.yaml docs/tasks/gateway-active-packages/pkg-000042*.yaml
```
