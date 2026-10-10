# STORY-GW-REQ56-01 — Issues list text search filter (D-S1)

## Meta
- **Key:** `STORY-GW-REQ56-01-issues-list-search-filter`
- **Пакет:** [`req56-issues-server-text-search/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) · P3 2026-10-10T16:01:13Z · gate PASS · backlog kept
- **Тип:** API / projection read filter
- **Parent REQ:** [`56-issues-server-text-search.md`](../../../requirements/56-issues-server-text-search.md)
- **Architecture:** [`TECH-ARCH-issues-server-text-search.md`](../../../architecture/TECH-ARCH-issues-server-text-search.md)
- **Siblings:** none (spa = consumer after Ready; threads OOS)
- **Skill declared:** `python-pro`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Зависит от:** —
- **Blocks:** STORY-GW-REQ56-02
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Scaffolded:** 2026-10-10T15:30:33Z (backlog) · **P1 APPLY:** 2026-10-10T15:52:08Z · **P3 Done:** 2026-10-10T16:01:13Z

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
| Envelope `data.issues` | `handlers.py` unchanged |
| D-S1 helper | `src/core/projection/issue_search_match.py` |
| Post-fetch + search AND | `src/core/projection/read_filters.py` `filter_projection_rows` |
| Statuses NEW/IN_REVIEW/PUBLISHED | `src/core/projection/enums.py` |
| Client D-S1 parity ref | `spa-app/src/router/issueSearchMatch.js` |
| Offline suite | `tests/test_gw_req56_01_issues_list_search_filter.py` **10 passed** |

## Target / AC

- [x] **AC-GW-REQ5601-01 (S1):** anonymous `GET /node/issues` + non-empty `search` + `status=PUBLISHED` → only D-S1 substring matches.
- [x] **AC-GW-REQ5601-02 (S2):** `search` + ≥1 structural filter composes (AND).
- [x] **AC-GW-REQ5601-03 (S3):** with same other params, adding `search` does not return rows excluded without `search`.
- [x] **AC-GW-REQ5601-04 (S4):** no new search route; no comments corpus; envelope shape unchanged.
- [x] **AC-GW-REQ5601-05:** empty/absent/whitespace `search` → no text restriction.
- [x] **AC-GW-REQ5601-06:** unit match helper + ASGI/handler wiring test green.

## Code touchpoints

- `src/core/api/asgi_app.py` `issues_list`
- `src/core/api/handlers.py` `handle_issues_list`
- `src/core/projection/read_filters.py` (+ optional dedicated match helper module — implement choice)
- store `list_projections` signatures if text must thread through (InMemory/SQLite/Supabase)

## Dependencies

- TECH-ARCH locks DP1–4; REQ param **`search`** locked (PA.2 sync 2026-10-10T15:30:33Z).

## Nested tasks (pipeline Present — pkg-000111)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | [`task-gw-req56-01-t01-d-s1-match-helper`](../../epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/task-gw-req56-01-t01-d-s1-match-helper/README.md) | Done | Helper D-S1; parity `issueSearchMatch.js` |
| **T02** | [`task-gw-req56-01-t02-post-fetch-filter-compose`](../../epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/task-gw-req56-01-t02-post-fetch-filter-compose/README.md) | Done | Post-fetch compose AND; hybrid v1 |
| **T03** | [`task-gw-req56-01-t03-asgi-handler-search-wire`](../../epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/task-gw-req56-01-t03-asgi-handler-search-wire/README.md) | Done | Wire param **`search`**; DP1 |
| **T04** | [`task-gw-req56-01-t04-unit-match-and-compose`](../../epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/task-gw-req56-01-t04-unit-match-and-compose/README.md) | Done | Unit match + compose |
| **T05** | [`task-gw-req56-01-t05-asgi-handler-search-tests`](../../epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/task-gw-req56-01-t05-asgi-handler-search-tests/README.md) | Done | ASGI/handler production-entry |
| **T06** | [`task-gw-req56-01-t06-story-gate`](../../epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/task-gw-req56-01-t06-story-gate/README.md) | Done | Gate AC-GW-REQ5601-01…06 PASS |
