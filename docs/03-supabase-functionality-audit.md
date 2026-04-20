# DOGE Complaints Gateway: Supabase Functionality Audit

## Scope

This audit reviews how Supabase is configured and used across:
- DB access from Python (`app/db.py`, service modules)
- Supabase SQL model (`db.sql`)
- Supabase Edge Functions (`supabase/functions/*`)
- Supabase local project config (`supabase/config.toml`)

## Active Supabase Features in This Repository

## Database/API usage
- Python client uses `create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)`.
- Application reads/writes via PostgREST-style table operations (`.table(...).insert/select/update/delete`).
- Heavy write path centers around `complaints`, dictionary tables, relation tables, and embedding tables.

## Postgres extensions implied by schema
- `GEOGRAPHY(POINT)` implies PostGIS dependency.
- `VECTOR(384)` implies `pgvector` dependency.

## Edge Functions
- `vectorize` function:
  - uses `Supabase.ai.Session('gte-small')`
  - accepts `{ input }`
  - returns `{ embedding }`
- `summary` function:
  - accepts `{ description }`
  - also uses `Supabase.ai.Session('gte-small')`
  - returns `summary` output that is generated through embedding-like call, not a textual summary model.

## Platform config highlights (`config.toml`)
- API exposed schemas: `public`, `graphql_public`
- Realtime enabled
- Storage enabled
- Auth enabled
- Edge runtime enabled

## Functional Alignment Findings

### 1) DB schema and runtime writes are not fully aligned
- Invalid index in `db.sql` targets non-existent `complaints.location_id`.
- Session creation route writes row shape incompatible with declared `session_complaints` constraints.

### 2) Supabase Auth is configured but bypassed for API access pattern
- Flask backend uses service role for all DB operations.
- Public endpoint behavior does not rely on end-user Supabase auth identity.

### 3) Edge Function auth strategy is custom and fragile
- Python code signs custom JWT using project secret and static subject.
- This can work technically but weakens identity granularity and auditability.

### 4) Missing Supabase migration workflow
- Repository has `db.sql` but no migration history under `supabase/migrations`.
- This increases schema drift risk between environments.

### 5) Security controls for exposed schema are not declared
- No RLS policy definitions in repository SQL.
- With `public` exposed through API, defense-in-depth appears incomplete.

## Capability Map: Used vs Declared

## Used in code
- Supabase Postgres tables via Python client
- Supabase Edge Functions for embeddings
- pgvector columns

## Declared in config but not materially integrated in backend code
- Realtime
- Storage (Supabase Storage not used in app code; Pinata is used instead)
- GraphQL public schema
- Most Auth provider flows

## Key Risks for Supabase Operations

### High
- Service-role-first architecture broadens blast radius if API is abused.
- Missing migration discipline risks inconsistent DB state per environment.

### High
- No repository-level evidence of RLS policies on exposed data tables.

### Medium
- Edge function naming/behavior mismatch (`summary`) can create integration bugs and inaccurate assumptions.

### Medium
- Environment variable naming in docs and code is not fully consistent (`SUPABASE_KEY` vs `SUPABASE_SERVICE_ROLE`).

## Recommended Supabase Hardening Plan

## P0
- Introduce migration-based schema management in `supabase/migrations`.
- Add explicit RLS policies for all exposed tables in `public`.
- Restrict direct service-role usage to internal/admin workflows only.

## P1
- Introduce user-scoped access model for intake and session resources.
- Align edge function auth with short-lived, properly scoped tokens.
- Add function-specific settings in config (including JWT verification intent).

## P2
- Clarify ownership of summarization:
  - use LLM summarization endpoint if text summary is required
  - keep embedding function purpose strictly semantic vectorization
- Add Supabase operational runbook:
  - schema rollout
  - rollback
  - secret rotation
  - policy verification checks
