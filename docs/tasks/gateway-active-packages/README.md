# Gateway Active Packages

Immutable queue snapshots for Gateway Story Builder.

- Add new package as `pkg-<NNNNNN>-<YYYYMMDD>-<slug>.yaml`.
- Do not edit existing package files after creation.
- Update `../gateway-active-package.current.yaml` to switch active wave.

## Active package (SSOT)

Current: [`../gateway-active-package.current.yaml`](../gateway-active-package.current.yaml) → `pkg-000043-20260703-gw-draft-01-story-draft-stash.yaml` (7 paths, GW-DRAFT-01 T01–T07 scaffolded).

Verify from workspace root:

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```

## `run_mode` overrides (вне active pkg)

Исполняются **только** по явной метке оператора; **не** меняют `gateway-active-package.current.yaml`. SSOT путей — [`Gateway_builder.plan.md`](../../../../.cursor/plans/Gateway_builder.plan.md) §safe-override (если секция есть) или строки ниже.

| `run_mode` | README path (1) |
|------------|-----------------|
| `gw_gauth_02_audit_cf1_followup` | `doge-complaints-gateway/docs/tasks/epics/EPIC-M2-20-gpt-submit-authz/stories/STORY-GW-GAUTH-02-user-token-introspection/task-gw-gauth-02-t07-audit-cf1-hosted-seed-identity-env-docs/README.md` |

GW-GAUTH-03 audit follow-up: **activation none** (0 impl gap) — см. [`audit-gw-gauth-03-verification-gate-403-2026-06-25.md`](../../analysis/audit-gw-gauth-03-verification-gate-403-2026-06-25.md).

GW-GAUTH-04 audit follow-up: **activation none** (0 impl gap) — см. [`audit-gw-gauth-04-authoritative-author-from-introspection-2026-06-25.md`](../../analysis/audit-gw-gauth-04-authoritative-author-from-introspection-2026-06-25.md).
