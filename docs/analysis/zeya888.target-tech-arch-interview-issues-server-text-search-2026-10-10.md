# Target tech-arch interview — issues-server-text-search

| Field | Value |
|-------|--------|
| **utc_now** | 2026-10-10T14:52:31Z |
| **utc_date** | 2026-10-10 |
| **builder_project** | gateway |
| **focusFolder** | doge-complaints-gateway |
| **Slug** | `issues-server-text-search` |
| **Arch root** | [`../architecture/TECH-ARCH-issues-server-text-search.md`](../architecture/TECH-ARCH-issues-server-text-search.md) |
| **REQ** | [`../requirements/56-issues-server-text-search.md`](../requirements/56-issues-server-text-search.md) |

---

## 1) Inputs + use case

| Input | Path |
|-------|------|
| `$requirementDoc` | `doge-complaints-gateway/docs/requirements/56-issues-server-text-search.md` |
| `$storyPackageDir` | — |
| `$storyList` | — |

**Story scope:** none (0 STORY files read).

**Use case:** Target technical architecture for server-side D-S1 text filter on `GET /node/issues` (gateway-local REQ-56) — not new backlog stories, not code.

---

## 2) Level classify

| Level | Evidence | Implication |
|-------|----------|-------------|
| Mixed functional+tech | REQ §1–3 product locks + §4 as-is paths + §7 Open (param name, index) | Extract tech into arch doc; keep REQ product-facing |

---

## 3) Verbatim decision log

### DP1 — HTTP query-param name

- **Question:** Literal name of the text query parameter on `GET /node/issues` (REQ §3 / §7.1 Open).
- **Options summary:** A `search` (SPA board URL key) · B `q` · C defer / Unknown in arch.
- **Agent recommendation:** A `search`.
- **Operator decision:** **accepted** — A.
- **Answer (verbatim):** `A`

### DP2 — Filter placement

- **Question:** Where D-S1 match runs (in-memory post-assemble vs SQL pushdown vs hybrid).
- **Options summary:** A in-memory only · B SQL/PostgREST pushdown · C hybrid (v1 in-memory; SQL/index later spike).
- **Agent recommendation:** C hybrid.
- **Operator decision:** **accepted** — C.
- **Answer (verbatim):** `C`

### DP3 — Public safety / anti-DRAFT

- **Question:** How status / “anti-DRAFT” interacts with text search (AC S3; REQ §7.3).
- **Options summary:** A contract caller + `status=PUBLISHED` (no new hard gate; no invent DRAFT) · B fail-closed when `search` present · C leave Unknown / PA.2 only.
- **Agent recommendation:** A.
- **Operator decision:** **accepted** — A.
- **Answer (verbatim):** `A`

### DP4 — Verify surfaces

- **Question:** Minimum verify named in target-arch (REQ §2 Tests).
- **Options summary:** A unit match+compose only · B unit + ASGI/handler wiring · C docs-only later.
- **Agent recommendation:** B.
- **Operator decision:** **accepted** — B.
- **Answer (verbatim):** `B`

---

## 4) Open Unknowns

1. Corpus size threshold for SQL/index/FTS spike.  
2. Exact module path for match helper (implement detail).  
3. Concrete API_REFERENCE/OpenAPI edit location — after Ready implement.

---

## 5) Link matrix

| Artifact | Path |
|----------|------|
| REQ | `docs/requirements/56-issues-server-text-search.md` |
| Arch root | `docs/architecture/TECH-ARCH-issues-server-text-search.md` |
| This report | `docs/analysis/zeya888.target-tech-arch-interview-issues-server-text-search-2026-10-10.md` |
| Stories | none |

---

## 6) Method notes

- **inputs (REQ and/or stories) ≠ target tech arch ≠ new work items**
- **packaging N/A** (no Git-owned non-src start / deployability-gap for this focus)
- **recommendation advisory; operator decides**
