# task-gw-req56-01-t01-d-s1-match-helper

## Task: implement — D-S1 match helper (T01)

## Meta
- **Story:** [STORY-GW-REQ56-01](../STORY-GW-REQ56-01-issues-list-search-filter.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000111
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-10-10T15:52:08Z
- **Done:** 2026-10-10T16:01:13Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-01-issues-list-search-filter.md`

## Purpose
Helper D-S1: trim; empty→no-op; case-insensitive substring; haystack et+ru+en title+description; parity `issueSearchMatch.js`; TECH-ARCH §3.3. Scope #2 · **AC-GW-REQ5601-05** (+ match rules for AC-01).

## Code Facts
### As-of-Done (P3 2026-10-10T16:01:13Z)
1. D-S1 helper Present — `src/core/projection/issue_search_match.py` (`issue_matches_search_query`, et+ru+en haystack).
2. Client parity ref Present — `spa-app/src/router/issueSearchMatch.js`.
3. TECH-ARCH §3.3 match contract locked.

### Historical (pre-P3 / scaffold)
1. Gateway text match helper Absent.
2. Gap text: «No D-S1 server helper yet».

## Gap
**G1 residual closed by T07:** Code Facts flipped As-of-Done vs Historical (helper Present).

## Acceptance / DoD
- [x] Helper implements trim / empty→match-all / case-insensitive substring
- [x] Haystack = et+ru+en title+description (SPA locale parity)
- [x] No LLM; no invent SQL/FTS; no comments corpus
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req56-01-t01.md` signed (P3)

## Where to change
- New helper module under `src/core/projection/` (or extend `read_filters.py` — implement choice)

## Out of scope
Post-fetch compose (T02); ASGI wire (T03); tests (T04/T05); gate (T06); OpenAPI (REQ56-02).

## Verification commands
```bash
rg -n "issueMatchesSearchQuery|LOCALE_CODES" spa-app/src/router/issueSearchMatch.js | head -20
```
