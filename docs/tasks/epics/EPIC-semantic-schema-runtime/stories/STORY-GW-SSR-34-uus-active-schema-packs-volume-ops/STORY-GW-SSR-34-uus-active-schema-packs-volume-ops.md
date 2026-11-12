# STORY-GW-SSR-34 — uus active: local warehouse + Railway Volume ops

## Meta
- **Key:** `STORY-GW-SSR-34-uus-active-schema-packs-volume-ops`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** P1 — D-SSR-12 Volume / local warehouse (sequence **34**)
- **Тип:** docs / env / gitignore / node activation
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-34-uus-active-schema-packs-volume-ops.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-34-uus-active-schema-packs-volume-ops.md)
- **Architecture:** D-SSR-12 · REQ4 §5.3
- **Parent REQ:** 51 · REQ4
- **decision_ref:** backlog SSR-34
- **Skill declared:** code-documenter (soft python-pro for `.gitignore` / `.env*.example`)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000091-20260907-gw-ssr-34-uus-active-schema-packs-volume-ops.yaml`](../../../../gateway-active-packages/pkg-000091-20260907-gw-ssr-34-uus-active-schema-packs-volume-ops.yaml)
- **Git:** только `semantic-schema-runtime`
- **Зависит от:** SSR-16 Done; loadable nested uus pack (вне story)
- **Scaffolded:** 2026-09-07T08:28:33Z
- **G34:** PASS 2026-09-07T08:32:02Z · [`gate`](./task-gw-ssr-34-t06-story-acceptance-gate/story-acceptance-gate-STORY-GW-SSR-34.md) · [`run-summary`](../../../../run-reports/run-summary-20260907-0832-gw-ssr-34-p3.md)
- **P6 G1:** CLOSED 2026-09-07T08:38:47Z · `run_mode=gw_ssr_34_audit_followup` · [`run-summary-audit`](../../../../run-reports/run-summary-20260907-0838-gw-ssr-34-audit-p6.md)

## Nested tasks (pkg-000091)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-ssr-34-t01-server-env-local-railway-playbook`](./task-gw-ssr-34-t01-server-env-local-railway-playbook/README.md) | Done (Awaiting Commits) |
| T02 | [`task-gw-ssr-34-t02-warehouse-model-manual-d-ssr-12`](./task-gw-ssr-34-t02-warehouse-model-manual-d-ssr-12/README.md) | Done (Awaiting Commits) |
| T03 | [`task-gw-ssr-34-t03-gitignore-node-packs`](./task-gw-ssr-34-t03-gitignore-node-packs/README.md) | Done (Awaiting Commits) |
| T04 | [`task-gw-ssr-34-t04-env-examples-node-schema-inventory`](./task-gw-ssr-34-t04-env-examples-node-schema-inventory/README.md) | Done (Awaiting Commits) |
| T05 | [`task-gw-ssr-34-t05-sibling-gpt-schema-binding-note`](./task-gw-ssr-34-t05-sibling-gpt-schema-binding-note/README.md) | Done (Awaiting Commits) |
| T06 | [`task-gw-ssr-34-t06-story-acceptance-gate`](./task-gw-ssr-34-t06-story-acceptance-gate/README.md) | Done (Awaiting Commits) · G34 PASS |
| T07 | [`task-gw-ssr-34-t07-audit-g1-as-of-done-ssot`](./task-gw-ssr-34-t07-audit-g1-as-of-done-ssot/README.md) | Done (Awaiting Commits) · G1 CLOSED |

## Scope / Out of scope

**In:** Local + Railway playbooks; warehouse model D-SSR-12; gitignore node packs; env inventory; GPT binding sibling note; G34.  
**Out:** SCHEMA_ROOT_URL fetch (SSR-35); pack content repair; Railway UI clicks; §Актуальная точка rewrite.

## Target / AC

- [x] **AC-GW-SSR34-01…06** — G34 PASS 2026-09-07T08:32:02Z
