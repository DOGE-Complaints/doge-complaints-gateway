# DOGE Complaints Gateway: Technical Architecture and Layering Audit

## Scope

This audit covers the current `dev` branch implementation of:
- Flask API entrypoint and route registration
- Service and utility modules under `app/`
- Supabase local project setup under `supabase/`
- SQL schema in `db.sql`
- Action contract in `gpt-actions.yaml`

## Current Architecture (As Implemented)

### Layer 1: Interface / Ingress
- `gpt-actions.yaml` exposes HTTP action contract for `/submit-complaint`.
- Flask app boots in `run.py` and binds to `0.0.0.0:5001` with `debug=True`.
- Only one blueprint is mounted in `app/__init__.py`: `submit_complaint_bp` under `/api/v1/`.

### Layer 2: Application Services
- `app/services/submit_complaint.py` orchestrates the end-to-end complaint flow:
  - request validation (partial)
  - complaint insert
  - complaint time/category/event linking
  - geocoding and embedding enrichment
  - Pinata upload
  - Dogeparty token issuance
- `app/services/oauth_processers.py` contains OAuth callback logic and session linking helper.
- `app/services/dogeparty.py` handles token issuance and low-level request/sign/send flow.

### Layer 3: Domain/Utility Modules
- `app/utils/enumerators.py` stores enum-like constants.
- `app/utils/geocoding.py` resolves coordinates from cache/OpenCage/Nominatim.
- `app/utils/ai_helper.py` handles edge-function vectorization and Anthropic-based summarization.
- `app/utils/pinatauploader.py` uploads complaint JSON to IPFS via Pinata.
- `app/utils/githubuploader.py` has a draft uploader (currently not operational).

### Layer 4: Data and Platform
- Supabase is consumed via Python client in `app/db.py` using service role credentials.
- Primary schema is defined in `db.sql` (complaints, dictionaries, join tables, embeddings).
- Supabase Edge Functions:
  - `supabase/functions/vectorize` for embeddings
  - `supabase/functions/summary` for AI output (currently mismatched with name/intent)
- Supabase config in `supabase/config.toml` enables Auth, Storage, Realtime, and Edge runtime.

## Layering Quality Assessment

## Strengths
- Clear top-level separation between API entrypoint, services, and utilities.
- Main complaint flow is centralized in one orchestrator route.
- Core data entities are normalized in SQL (dictionary tables + many-to-many relation tables).
- Embedding storage pattern exists and is linked to dictionary entities.

## Gaps and Architectural Debt

### 1) Partial route graph and dead code path
- OAuth blueprint exists but is not registered in Flask app.
- Result: callback endpoint cannot be reached in runtime.

### 2) Overloaded orchestration service
- `submit_complaint()` performs validation, persistence, enrichment, external IO, and token minting in one synchronous call.
- This creates high coupling, long request latency, and weak failure isolation.

### 3) Weak transaction boundaries
- Multi-step writes are not wrapped in a DB transaction.
- A failure after complaint insert can leave partial state (complaint exists, related records missing or inconsistent).

### 4) Ambiguous source of truth for contracts
- Input model is distributed across:
  - `gpt-actions.yaml`
  - `complaint-input-demo.json`
  - runtime validations in `submit_complaint.py`
  - table shape in `db.sql`
- These artifacts are not fully consistent.

### 5) Missing explicit domain layer
- Business invariants are embedded in controller/service functions instead of dedicated domain model/use-case boundaries.
- This makes testing and future evolution harder.

### 6) Operational concerns in request path
- External calls (OpenCage, Supabase function, Pinata, Dogeparty, Anthropic) are in the hot path with no retry policy, no timeout policy, and no async queue.

## Recommended Target Layering

### Proposed boundaries
- **API Layer**: request parsing + schema validation + response mapping only.
- **Use Case Layer**: complaint intake workflow with explicit step orchestration.
- **Domain Layer**: complaint/session/category/event/time rules and invariants.
- **Infrastructure Layer**: Supabase repositories, external API adapters, message/queue adapters.

### Suggested decomposition of current `submit_complaint()` flow
1. Validate and normalize payload.
2. Persist complaint graph transactionally.
3. Emit async jobs:
   - vectorize categories/events
   - upload complaint artifact
   - mint Dogeparty token
4. Update status fields for downstream job outcomes.

## Priority Refactor Roadmap

### P0 (stability)
- Register all required blueprints or remove dead routes.
- Split sync write path from long-running external integrations.
- Add transaction-safe persistence strategy for complaint graph writes.

### P1 (maintainability)
- Introduce request/response schemas as single source of truth.
- Add repository adapters for each table group.
- Add structured logging and correlation IDs.

### P2 (scalability)
- Move enrichment/tokenization to background workers.
- Add idempotency keys on intake endpoint.
- Add metrics for step latency and failure rates.
