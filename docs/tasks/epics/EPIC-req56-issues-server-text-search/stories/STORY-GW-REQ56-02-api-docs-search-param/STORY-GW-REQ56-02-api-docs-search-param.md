# STORY-GW-REQ56-02 — Document `search` on GET /node/issues

## Meta
- **Key:** `STORY-GW-REQ56-02-api-docs-search-param`
- **Parent Epic:** [`../../../EPIC-req56-issues-server-text-search.md`](../../../EPIC-req56-issues-server-text-search.md)
- **Пакет:** [`req56-issues-server-text-search/`](../../../../backlog-stories/req56-issues-server-text-search/INDEX.md)
- **Status:** 🟢 Done (P3 gate PASS · P6 G1/G3 CLOSED 2026-10-10T16:50:05Z pkg-000112) · docs-only
- **Тип:** runtime / API docs
- **source:** [`../../../../backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-02-api-docs-search-param.md`](../../../../backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-02-api-docs-search-param.md)
- **Parent REQ:** [`56-issues-server-text-search.md`](../../../../requirements/56-issues-server-text-search.md)
- **Architecture:** [`../../../../architecture/TECH-ARCH-issues-server-text-search.md`](../../../../architecture/TECH-ARCH-issues-server-text-search.md) §6.3
- **decision_ref:** backlog REQ56-02 · TECH-ARCH §6.3 · param **`search`**
- **Siblings:** soft REQ56-01 Done (behavior Present)
- **Skill declared:** `python-pro` · soft `code-documenter`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`  
  Soft: `.cursor/skills/sources/jeffallan-claude-skills/skills/code-documenter/SKILL.md`
- **Operative package:** [`../../../../gateway-active-packages/pkg-000112-20261010-gw-req56-02-api-docs-search-param.yaml`](../../../../gateway-active-packages/pkg-000112-20261010-gw-req56-02-api-docs-search-param.yaml)
- **Git:** `dev`
- **Operator locks:** docs-only API_REFERENCE + openapi; no runtime filter invent; no comments/separate route/index claims
- **Зависит от:** STORY-GW-REQ56-01 Done
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../../.cursor/rules/analysis.mdc)
- **Scaffolded:** 2026-10-10T16:25:31Z
- **Done:** 2026-10-10T16:30:12Z

## Nested tasks (pkg-000112)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req56-02-t01-api-reference-search`](./task-gw-req56-02-t01-api-reference-search/README.md) | 🟢 Done |
| T02 | [`task-gw-req56-02-t02-openapi-search-param`](./task-gw-req56-02-t02-openapi-search-param/README.md) | 🟢 Done |
| T03 | [`task-gw-req56-02-t03-story-gate`](./task-gw-req56-02-t03-story-gate/README.md) | 🟢 Done |
| T04 | [`task-gw-req56-02-t04-audit-g1-status-enum-ssot`](./task-gw-req56-02-t04-audit-g1-status-enum-ssot/README.md) | 🟢 Done · G1 CLOSED |
| T05 | [`task-gw-req56-02-t05-audit-g3-binding-line-refs`](./task-gw-req56-02-t05-audit-g3-binding-line-refs/README.md) | 🟢 Done · G3 CLOSED |

---

## Scope

1. Document query param **`search`** on `GET /node/issues` in `docs/runtime-docs/api-reference/API_REFERENCE.md` (section `### GET /node/issues`).
2. Update `docs/runtime-docs/api-reference/openapi.yaml` list parameters for the same endpoint.
3. Align wording with D-S1 + empty→no-op + compose with existing filters; anonymous; no separate search route.

## Out of scope

- Runtime filter implementation (→ REQ56-01).
- SPA docs / DUI-Q12; SQL index docs; invent new OpenAPI package tree outside existing `openapi.yaml`.

## Verified current state (as of Done P3 2026-10-10T16:30:12Z)

| Fact | Path |
|------|------|
| API_REFERENCE `search` | Present — `docs/runtime-docs/api-reference/API_REFERENCE.md` |
| OpenAPI `search` | Present — `docs/runtime-docs/api-reference/openapi.yaml` |
| Runtime `search` behavior | Present via REQ56-01 |

## Target / AC

- [x] **AC-GW-REQ5602-01:** API_REFERENCE documents `search` (optional string; D-S1 behavior summary; empty/absent = no text filter).
- [x] **AC-GW-REQ5602-02:** `openapi.yaml` documents `search` on `GET /node/issues`.
- [x] **AC-GW-REQ5602-03:** Docs do not claim comments search / separate search endpoint / invented index.

## Code touchpoints

- `docs/runtime-docs/api-reference/API_REFERENCE.md`
- `docs/runtime-docs/api-reference/openapi.yaml`

## Dependencies

- REQ56-01 Done (behavior exists before docs claim Ready).

## Related

- Backlog: [`../../../../backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-02-api-docs-search-param.md`](../../../../backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-02-api-docs-search-param.md)
- Gate: [`./task-gw-req56-02-t03-story-gate/story-acceptance-gate-STORY-GW-REQ56-02.md`](./task-gw-req56-02-t03-story-gate/story-acceptance-gate-STORY-GW-REQ56-02.md)
- Run summary: [`../../../../run-reports/run-summary-20261010-1630-gw-req56-02-p3.md`](../../../../run-reports/run-summary-20261010-1630-gw-req56-02-p3.md)
- Predecessor: [`../STORY-GW-REQ56-01-issues-list-search-filter/STORY-GW-REQ56-01-issues-list-search-filter.md`](../STORY-GW-REQ56-01-issues-list-search-filter/STORY-GW-REQ56-01-issues-list-search-filter.md)
- Epic / INDEX: [`../../../EPIC-req56-issues-server-text-search.md`](../../../EPIC-req56-issues-server-text-search.md) · [`../../../../backlog-stories/req56-issues-server-text-search/INDEX.md`](../../../../backlog-stories/req56-issues-server-text-search/INDEX.md)
