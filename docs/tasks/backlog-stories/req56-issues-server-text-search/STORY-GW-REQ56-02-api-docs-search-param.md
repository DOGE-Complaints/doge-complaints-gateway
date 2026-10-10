# STORY-GW-REQ56-02 — Document `search` on GET /node/issues

## Meta
- **Key:** `STORY-GW-REQ56-02-api-docs-search-param`
- **Пакет:** [`req56-issues-server-text-search/`](./INDEX.md)
- **Status:** Draft (Todo)
- **Тип:** runtime / API docs
- **Parent REQ:** [`56-issues-server-text-search.md`](../../../requirements/56-issues-server-text-search.md)
- **Architecture:** [`TECH-ARCH-issues-server-text-search.md`](../../../architecture/TECH-ARCH-issues-server-text-search.md) §6.3
- **Skill declared:** `python-pro` · soft `code-documenter`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`  
  Soft: `.cursor/skills/sources/jeffallan-claude-skills/skills/code-documenter/SKILL.md`
- **Зависит от:** STORY-GW-REQ56-01
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Scaffolded:** 2026-10-10T15:30:33Z (backlog only; no pkg)

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
| Text param documented | **Absent** (pre-REQ56-01) |

## Target / AC

- [ ] **AC-GW-REQ5602-01:** API_REFERENCE documents `search` (optional string; D-S1 behavior summary; empty/absent = no text filter).
- [ ] **AC-GW-REQ5602-02:** `openapi.yaml` documents `search` on `GET /node/issues`.
- [ ] **AC-GW-REQ5602-03:** Docs do not claim comments search / separate search endpoint / invented index.

## Code touchpoints

- `docs/runtime-docs/api-reference/API_REFERENCE.md`
- `docs/runtime-docs/api-reference/openapi.yaml`

## Dependencies

- REQ56-01 Done (behavior exists before docs claim Ready).

## Nested tasks (planned — folders at P1.3 only; name ≠ create)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-gw-req56-02-t01-api-reference-search` | Todo | `API_REFERENCE.md`: optional `search`, D-S1 summary, empty→no-op; AC-5602-01 |
| **T02** | `task-gw-req56-02-t02-openapi-search-param` | Todo | `openapi.yaml` — param `search` на `GET /node/issues`; AC-5602-02 |
| **T03** | `task-gw-req56-02-t03-story-gate` | Todo | Gate AC-GW-REQ5602-01…03 (без claims comments / separate route / invent index) |
