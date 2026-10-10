# STORY-GW-REQ56-01 — Issues list text search filter (D-S1)

## Meta
- **Key:** `STORY-GW-REQ56-01-issues-list-search-filter`
- **Parent Epic:** [`../../../EPIC-req56-issues-server-text-search.md`](../../../EPIC-req56-issues-server-text-search.md)
- **Пакет:** [`req56-issues-server-text-search/`](../../../../backlog-stories/req56-issues-server-text-search/INDEX.md)
- **Status:** 🔵 Implemented (Waiting Acceptance) · P3 Done 2026-10-10T16:01:13Z · gate PASS
- **Тип:** API / projection read filter
- **source:** [`../../../../backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-01-issues-list-search-filter.md`](../../../../backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-01-issues-list-search-filter.md)
- **Parent REQ:** [`56-issues-server-text-search.md`](../../../../requirements/56-issues-server-text-search.md)
- **Architecture:** [`../../../../architecture/TECH-ARCH-issues-server-text-search.md`](../../../../architecture/TECH-ARCH-issues-server-text-search.md)
- **decision_ref:** backlog REQ56-01 · TECH-ARCH DP1–4 · param **`search`**
- **Siblings:** soft REQ56-02 (docs after Ready)
- **Skill declared:** `python-pro`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Operative package:** [`../../../../gateway-active-packages/pkg-000111-20261010-gw-req56-01-issues-list-search-filter.yaml`](../../../../gateway-active-packages/pkg-000111-20261010-gw-req56-01-issues-list-search-filter.yaml)
- **Git:** `dev`
- **Operator locks:** param **`search`**; D-S1 hybrid in-memory; no separate search route; no comments search; no SQL/FTS invent; DP1–4
- **Зависит от:** —
- **Blocks:** STORY-GW-REQ56-02
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../../.cursor/rules/analysis.mdc)
- **Scaffolded:** 2026-10-10T15:52:08Z
- **P3 Done:** 2026-10-10T16:01:13Z · [`run-summary`](../../../../run-reports/run-summary-20261010-1601-gw-req56-01-p3.md) · [`gate`](./task-gw-req56-01-t06-story-gate/story-acceptance-gate-STORY-GW-REQ56-01.md) PASS

## Nested tasks (pkg-000111)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req56-01-t01-d-s1-match-helper`](./task-gw-req56-01-t01-d-s1-match-helper/README.md) | 🟢 Done |
| T02 | [`task-gw-req56-01-t02-post-fetch-filter-compose`](./task-gw-req56-01-t02-post-fetch-filter-compose/README.md) | 🟢 Done |
| T03 | [`task-gw-req56-01-t03-asgi-handler-search-wire`](./task-gw-req56-01-t03-asgi-handler-search-wire/README.md) | 🟢 Done |
| T04 | [`task-gw-req56-01-t04-unit-match-and-compose`](./task-gw-req56-01-t04-unit-match-and-compose/README.md) | 🟢 Done |
| T05 | [`task-gw-req56-01-t05-asgi-handler-search-tests`](./task-gw-req56-01-t05-asgi-handler-search-tests/README.md) | 🟢 Done |
| T06 | [`task-gw-req56-01-t06-story-gate`](./task-gw-req56-01-t06-story-gate/README.md) | 🟢 Done |
| T07 | [`task-gw-req56-01-t07-audit-g1-as-of-done-ssot`](./task-gw-req56-01-t07-audit-g1-as-of-done-ssot/README.md) | 🟢 Done · G1 CLOSED |
| T08 | [`task-gw-req56-01-t08-audit-g3-ac02-structural-compose-test`](./task-gw-req56-01-t08-audit-g3-ac02-structural-compose-test/README.md) | 🟢 Done · G3 CLOSED |

---

## Scope

1. Accept optional query param **`search`** on `GET /node/issues` (REQ §3; TECH-ARCH DP1).
2. D-S1 match in-memory post-assemble (hybrid v1): trim; empty/absent → no text restrict; case-insensitive substring; haystack et+ru+en title+description (parity `issueSearchMatch.js`).
3. Compose with existing structural/geo filters; anonymous list remains valid.
4. Text filter must not widen exposure vs same request without `search` (status rules unchanged; board-parity consumer uses `status=PUBLISHED`).
5. Unit tests (match + compose) + ASGI/handler test that `search` affects production entry filtering.
6. No separate search endpoint; no comments search; no SQL/index DDL invent.

## Out of scope

- API_REFERENCE / OpenAPI wording (→ REQ56-02).
- SQL/FTS/index spike; SPA UI / DUI-Q12 enable; threads/comments; invent DRAFT status; product-root REQ.

## Verified current state (As-of-Done P3 2026-10-10T16:01:13Z)

| Fact | Path |
|------|------|
| Param `search` on list | `src/core/api/asgi_app.py` `issues_list` |
| Handler threads `search` | `src/core/api/handlers.py` `handle_issues_list` |
| Envelope `data.issues` | unchanged |
| D-S1 helper | `src/core/projection/issue_search_match.py` |
| Post-fetch + search AND | `src/core/projection/read_filters.py` `filter_projection_rows` |
| Store thread | InMemory / SQLite / Supabase `list_projections(search=)` |
| Offline suite | `tests/test_gw_req56_01_issues_list_search_filter.py` **10 passed** |
| Client D-S1 parity ref | `spa-app/src/router/issueSearchMatch.js` |

## Target / AC

- [x] **AC-GW-REQ5601-01 (S1):** anonymous `GET /node/issues` + non-empty `search` + `status=PUBLISHED` → only D-S1 substring matches.
- [x] **AC-GW-REQ5601-02 (S2):** `search` + ≥1 structural filter composes (AND).
- [x] **AC-GW-REQ5601-03 (S3):** with same other params, adding `search` does not return rows excluded without `search`.
- [x] **AC-GW-REQ5601-04 (S4):** no new search route; no comments corpus; envelope shape unchanged.
- [x] **AC-GW-REQ5601-05:** empty/absent/whitespace `search` → no text restriction.
- [x] **AC-GW-REQ5601-06:** unit match helper + ASGI/handler wiring test green.

## Code touchpoints (As-of-Done P3 — Present)

- `src/core/api/asgi_app.py` `issues_list` — Query param `search`
- `src/core/api/handlers.py` `handle_issues_list` — `search=` → `list_projections`
- `src/core/projection/issue_search_match.py` — D-S1 helper
- `src/core/projection/read_filters.py` — `filter_projection_rows(..., search=)`
- stores InMemory/SQLite/Supabase — `list_projections(search=)`

### Historical (scaffold / pre-P3)
- List/handler/filter without text; helper Absent; «implement in P3» obligation (closed).

## Dependencies

- TECH-ARCH locks DP1–4; REQ param **`search`** locked (PA.2 sync 2026-10-10T15:30:33Z).

## Related

- Backlog: [`../../../../backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-01-issues-list-search-filter.md`](../../../../backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-01-issues-list-search-filter.md)
- Successor docs: [`../../../../backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-02-api-docs-search-param.md`](../../../../backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-02-api-docs-search-param.md)
- Epic / INDEX: [`../../../EPIC-req56-issues-server-text-search.md`](../../../EPIC-req56-issues-server-text-search.md) · [`../../../../backlog-stories/req56-issues-server-text-search/INDEX.md`](../../../../backlog-stories/req56-issues-server-text-search/INDEX.md)
