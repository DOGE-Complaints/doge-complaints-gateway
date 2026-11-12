# Taxonomy cycle run artifacts

Per-cycle folder layout for [`Taxonomy_builder.plan.md`](../../../../.cursor/plans/Taxonomy_builder.plan.md) (TC0–TC7).

## Path

```
doge-complaints-gateway/docs/tasks/run-reports/taxonomy-cycles/cycle-<YYYYMMDD>/
```

`<YYYYMMDD>` = `cycle_id` (same as `run_mode=taxonomy_cycle_<YYYYMMDD>`).

## Files

| File | Phase | Description |
|------|-------|-------------|
| `misses-ranked.json` | TC1 | Output of `taxonomy_fetch_misses.py` — `{ fetched_at, rows[] }` |
| `taxonomy-decisions.yaml` | TC2–TC3 | Draft from classify; finalized after operator interview |
| `reproject-dry-run.log` | TC6a | Stdout from `reproject_issue_i18n.py --dry-run` |
| `run-summary-taxonomy-cycle-<YYYYMMDD>.md` | TC7 | Session summary; linked from bullrun Run Reports Registry |

## Schema

Decision manifest schema: [`taxonomy-decisions-schema.md`](../../../runtime-docs/appendix/taxonomy-decisions-schema.md).

## Commit policy

Do **not** commit `cycle-*` folders unless the operator explicitly requests it (builder plan hard rule).

## Bullrun status

Cycle status tracked in **Taxonomy Cycles** section of [`bullrun-launch-index.md`](../../bullrun-launch-index.md):

| S | Cycle | Status | Notes |
|---|-------|--------|-------|
| ⚪/🟡/🟢 | taxonomy-YYYYMMDD | ready / in_progress / done | manifest link, gateway+spa commits pending |
