# Issues server text search on GET /node/issues — target technical architecture

| Field | Value |
|-------|--------|
| **Focus** | D-S1 text filter on existing public issues list |
| **Parent REQ** | [`../requirements/56-issues-server-text-search.md`](../requirements/56-issues-server-text-search.md) |
| **Story scope** | none (0 STORY files) |
| **Interview** | [`../analysis/zeya888.target-tech-arch-interview-issues-server-text-search-2026-10-10.md`](../analysis/zeya888.target-tech-arch-interview-issues-server-text-search-2026-10-10.md) |
| **Recorded** | 2026-10-10T14:52:31Z |
| **Mode** | Target technical architecture of the focus — **not** implementation tasks / STORY / pkg |
| **Slug** | `issues-server-text-search` |
| **Layout** | single file (`archDocMode=auto`) |

**Levels:** functional = REQ `56` · this doc = how the focus is realized in `doge-complaints-gateway` · work items = backlog / P1.3 elsewhere.

---

## 1) Context & inputs (functional vs tech)

| Layer | Lives in | Content |
|-------|----------|---------|
| Functional / product | REQ `56` | Goal, OOS, operator locks, AC S1–S4, Open questions |
| Target tech (this doc) | `docs/architecture/TECH-ARCH-issues-server-text-search.md` | Components, flows, contracts, verify, coexistence |
| Work items | backlog STORY / pkg (other prompts) | **Not here** |

**Use case:** Enable anonymous callers to pass a text query on the same `GET /node/issues` list so the server applies D-S1 substring match on multilingual title+description, composed with existing structural/geo filters — without a separate search endpoint, comments, or product-root/spa REQ.

**Packaging:** N/A (extends existing ASGI route; Git ownership ≠ image packaging not in scope).

---

## 2) Operator locks (Architect Studio interview 2026-10-10)

| # | Topic | Decision | Rec. vs op |
|---|--------|----------|------------|
| DP1 | HTTP query-param name | **`search`** | accepted |
| DP2 | Filter placement | **Hybrid:** v1 in-memory post-assemble; SQL/index/FTS = later spike (no invent DDL here) | accepted |
| DP3 | Public safety / “anti-DRAFT” | Text filter does **not** change status rules; board-parity consumer sends `status=PUBLISHED`; do **not** invent issue status `DRAFT` | accepted |
| DP4 | Verify surfaces | Unit (D-S1 match + compose with ≥1 structural filter) **+** ASGI/handler test that `search` participates on production entry | accepted |

Product locks already in REQ §3 (corpus issues-only; D-S1; extend list; anonymous) remain SSOT.

---

## 3) Target technical architecture

### 3.1 Components & boundaries

| Component | Responsibility | Must not |
|-----------|----------------|----------|
| ASGI `GET /node/issues` | Accept optional query param **`search`** alongside existing structural/geo params | Invent a separate search route |
| `handle_issues_list` | Pass `search` into the projection list path | Change success envelope shape |
| Issue projection read store | Continue fetch/assemble of public issue rows | Own invent SQL text DDL in v1 |
| Post-fetch filter layer | Apply existing structural/geo filters **and** D-S1 text match when `search` non-empty after trim | Widen status exposure vs list without `search` |
| SPA (out of this REQ) | Consumer of Ready API; may map board URL `search` 1:1 | Sibling spa/product-root REQ under this focus |

### 3.2 Primary flow (logical)

```text
Anonymous client
  → GET /node/issues?search=<text>&status=PUBLISHED&…structural/geo…
  → ASGI issues_list (param search)
  → handle_issues_list
  → issue_projection_read_store.list_projections(… + text intent)
  → assemble public issue payloads
  → post-fetch filters:
        structural / geo (as today)
        + D-S1 text if search trimmed non-empty
  → build_success_envelope { issues: [...] }
```

Empty / absent / whitespace-only `search` → **no** text restriction (D-S1 / REQ §3).

### 3.3 Match contract (D-S1 parity)

Parity target: `spa-app/src/router/issueSearchMatch.js` (`issueMatchesSearchQuery`).

| Rule | Behavior |
|------|----------|
| Normalize | `trim` on query string |
| Empty after trim | Match all (no text filter) |
| Compare | Case-insensitive substring (`haystack.includes(needle)`) |
| Haystack | Concatenate non-empty `et`+`ru`+`en` string values from `title` and `description` (locale set as SPA `LOCALE_CODES`) |
| Compose | AND with existing structural/geo filters when those are present (AC S2) |

### 3.4 Public safety / status

- As-is: status filter applies only when the caller passes `status` (see coexistence paths below).
- Target: adding `search` must **not** return rows that the same request without `search` would exclude under the same status/structural/geo args (AC S3).
- Board-parity public consumer: include `status=PUBLISHED`.
- Do **not** invent a `DRAFT` value in `DOGEIssueStatus` for this focus.

### 3.5 Ownership / contracts

| Artifact class | Owner | Notes |
|----------------|-------|-------|
| Wire param `search` on list | Gateway | Document in API_REFERENCE / OpenAPI after Ready (REQ AC) |
| D-S1 match semantics | Gateway (server); SPA remains reference for parity | Client filter may remain until FE enables live search (DUI-Q12) |
| Index / SQL pushdown | Later spike | Not v1; name ≠ create for DDL |
| SPA UI / toolbar enable | spa-app packages (not this REQ) | After gateway Ready |

---

## 4) Runtime / packaging / env / deploy-residual

| Theme | Target |
|-------|--------|
| Runtime topology | Existing gateway ASGI app (uvicorn / current start ritual) |
| Packaging seam | **N/A** |
| New env vars | None claimed |
| Deploy residual | No new deploy contract; verify locally via unit + ASGI/handler tests named above |

---

## 5) Coexistence with as-is (verified)

| Fact | Evidence |
|------|----------|
| List query params today: status/type/labels/institution/dates/geo only | `src/core/api/asgi_app.py:528–546` |
| Handler → `list_projections(...)` without text | `src/core/api/handlers.py:535–573` |
| Success envelope `data.issues` | `src/core/api/handlers.py:574–576` |
| Supabase path: fetch rows → assemble → `filter_projection_rows` | `src/core/infrastructure/db_supabase.py:976–1037` |
| Status filter only if caller passed status | `src/core/projection/read_filters.py:340–350` |
| Governed statuses: NEW / IN_REVIEW / PUBLISHED (no DRAFT) | `src/core/projection/enums.py:6–11` |
| Projection text columns | `supabase/bootstrap/000_full_init.sql:122–124` (`title_json` / `description_json`) |
| Client D-S1 reference | `spa-app/src/router/issueSearchMatch.js:39–43` |
| SPA board URL key `search` | `spa-app/src/router/boardQuery.js:68`, `103–104` |

---

## 6) Verify surfaces (named)

1. **Unit:** D-S1 match helper (trim / empty / case / locales haystack) + compose with at least one structural filter.  
2. **Production entry:** ASGI or handler-level test that query param **`search`** affects `GET /node/issues` filtering (wiring, not only an orphan helper).  
3. **Docs (after Ready):** API_REFERENCE / OpenAPI document `search` on the list endpoint.

---

## 7) Open questions (residual)

1. When corpus size justifies SQL/index/FTS spike (threshold Unknown — measure later).  
2. Exact Python module placement of the match helper (implement detail; must remain on post-fetch path for v1).  
3. Exact API_REFERENCE/OpenAPI file edit — after implement wave.

---

## 8) Explicit not in this doc

- NEW STORY keys, pkg YAML, P3 tasks, or product code  
- Threads/comments search; scope flag; separate search endpoint  
- SPA UI redesign / sibling spa REQ / product-root REQ  
- Invented index DDL or invent issue status `DRAFT`
