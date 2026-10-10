# STORY-GW-REQ56-02 — Document `search` on GET /node/issues

## Meta
- **Key:** `STORY-GW-REQ56-02-api-docs-search-param`
- **Пакет:** [`req56-issues-server-text-search/`](./INDEX.md)
- **Status:** 🟢 Done (P3 gate PASS · P6 G1/G3 CLOSED 2026-10-10T16:50:05Z) · backlog kept
- **Тип:** runtime / API docs
- **Parent REQ:** [`56-issues-server-text-search.md`](../../../requirements/56-issues-server-text-search.md)
- **Architecture:** [`TECH-ARCH-issues-server-text-search.md`](../../../architecture/TECH-ARCH-issues-server-text-search.md) §6.3
- **Skill declared:** `python-pro` · soft `code-documenter`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`  
  Soft: `.cursor/skills/sources/jeffallan-claude-skills/skills/code-documenter/SKILL.md`
- **Зависит от:** STORY-GW-REQ56-01
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Scaffolded:** 2026-10-10T15:30:33Z (backlog) · **P1 APPLY:** 2026-10-10T16:25:31Z · **Done:** 2026-10-10T16:30:12Z

---

## Scope

1. Document query param **`search`** on `GET /node/issues` in `docs/runtime-docs/api-reference/API_REFERENCE.md` (section `### GET /node/issues`).
2. Update `docs/runtime-docs/api-reference/openapi.yaml` list parameters for the same endpoint.
3. Align wording with D-S1 + empty→no-op + compose with existing filters; anonymous; no separate search route.

## Out of scope

- Runtime filter implementation (→ REQ56-01).
- SPA docs / DUI-Q12; SQL index docs; invent new OpenAPI package tree outside existing `openapi.yaml`.

## Verified current state

| Fact | Path |
|------|------|
| API_REFERENCE list section | `docs/runtime-docs/api-reference/API_REFERENCE.md` (`GET /node/issues` ~L630) |
| Mentions multi-parameter filter API | same file ~L817 |
| OpenAPI present | `docs/runtime-docs/api-reference/openapi.yaml` |
| Text param documented | **Present** (P3 2026-10-10T16:30:12Z) |

## Target / AC

- [x] **AC-GW-REQ5602-01:** API_REFERENCE documents `search` (optional string; D-S1 behavior summary; empty/absent = no text filter).
- [x] **AC-GW-REQ5602-02:** `openapi.yaml` documents `search` on `GET /node/issues`.
- [x] **AC-GW-REQ5602-03:** Docs do not claim comments search / separate search endpoint / invented index.

## Code touchpoints

- `docs/runtime-docs/api-reference/API_REFERENCE.md`
- `docs/runtime-docs/api-reference/openapi.yaml`

## Dependencies

- REQ56-01 Done (behavior exists before docs claim Ready).

## Nested tasks (pipeline Present — pkg-000112)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | [`task-gw-req56-02-t01-api-reference-search`](../../epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-02-api-docs-search-param/task-gw-req56-02-t01-api-reference-search/README.md) | Done | `API_REFERENCE.md`: optional `search`; AC-5602-01 |
| **T02** | [`task-gw-req56-02-t02-openapi-search-param`](../../epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-02-api-docs-search-param/task-gw-req56-02-t02-openapi-search-param/README.md) | Done | `openapi.yaml` param `search`; AC-5602-02 |
| **T03** | [`task-gw-req56-02-t03-story-gate`](../../epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-02-api-docs-search-param/task-gw-req56-02-t03-story-gate/README.md) | Done | Gate AC-GW-REQ5602-01…03 PASS |
| **T04** | [`task-gw-req56-02-t04-audit-g1-status-enum-ssot`](../../epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-02-api-docs-search-param/task-gw-req56-02-t04-audit-g1-status-enum-ssot/README.md) | Done | audit G1 CLOSED — status enum SSOT |
| **T05** | [`task-gw-req56-02-t05-audit-g3-binding-line-refs`](../../epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-02-api-docs-search-param/task-gw-req56-02-t05-audit-g3-binding-line-refs/README.md) | Done | audit G3 CLOSED — binding symbols |
