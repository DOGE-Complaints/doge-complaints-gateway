# acceptance-verification — GW-SSR-17 t06

- **Result:** PASS
- **Date:** 2026-08-30T14:51:13Z
- **Package:** pkg-000074 / `run_mode=gw_ssr_17_audit_followup`

## Evidence

G1 CLOSED: persistent SSOT As-of-Done vs Historical.

- Backlog §Verified: required binding 4xx (`contracts.py:227–241,480–482`); match+validate active pack (`services.py:249–271`); Historical civic-optional kept.
- Pipeline §Verified synced (same split).
- Epic PS: **As-of-Done (SSR-17 pkg-000074)**; **Next (D-SSR-8):** SSR-18 Todo.
- Dashboard Last change / Status: SSR-17 Done; SSR-18 Todo.

G2 WAIVED: `sed -n '17,20p'` still EPIC-M2-24 / ES-03. `current.yaml` stays pkg-000074. No `src/` / ClusterLens / GPT UI.

## Commands

```bash
rg -n 'Binding optional|Validate только если binding is not None|Civic HTTP без binding зелёный' \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-17-intake-active-schema-gate.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-17-intake-active-schema-gate/STORY-GW-SSR-17-intake-active-schema-gate.md
# → only Historical rows
rg -n 'As-of-Done \(SSR-17' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-17-intake-active-schema-gate.md
sed -n '17,20p' doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
# → EPIC-M2-24 / ES-03
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
# → ok 5 paths (pkg-000074); ok date-check
```
