# DOGE Complaints Gateway: Security Audit

## Method

Static audit of source/config focused on:
- AuthN/AuthZ controls
- Secret handling
- Data exposure and logging
- External integration safety
- DB access model and Supabase security posture

No dynamic penetration testing was performed in this pass.

## Executive Summary

Current implementation has multiple high-risk issues around authorization, secret handling, and unsafe default runtime behavior. The highest impact concern is broad write capability through service-role access exposed via public API routes without user-level authorization controls.

## Findings

## Critical

### SEC-01: Unauthenticated public write surface with privileged DB credentials
- Evidence:
  - Public routes in `submit_complaint.py` accept requests without auth checks.
  - `app/db.py` initializes Supabase client with `SUPABASE_SERVICE_ROLE`.
- Risk:
  - Any caller reaching API can trigger privileged DB writes and downstream side effects.
- Recommendation:
  - Enforce authentication and authorization at API boundary.
  - Remove service-role usage from user-facing request path.
  - Apply least-privilege credentials and RLS-backed identity model.

### SEC-02: Missing RLS policy definitions for exposed schema
- Evidence:
  - `supabase/config.toml` exposes `public` schema via API.
  - No policy SQL is present in repository.
- Risk:
  - If table grants are permissive, unauthorized read/write is possible via Data API.
- Recommendation:
  - Enable RLS on all exposed tables and define explicit policies per access pattern.

## High

### SEC-03: Sensitive secret material and tokens printed to logs
- Evidence:
  - `app/utils/ai_helper.py` prints JWT secret context and authorization headers.
  - `app/services/dogeparty.py` logs private-key-derived bytes and signed payloads.
  - Multiple modules print full request/response payloads including complaint data.
- Risk:
  - Secret leakage and PII exposure through logs, APM, or console history.
- Recommendation:
  - Remove secret-bearing logs.
  - Introduce structured logging with redaction.
  - Classify and mask PII fields.

### SEC-04: Flask debug mode enabled in runtime entrypoint
- Evidence:
  - `run.py` starts app with `debug=True`.
- Risk:
  - Debug stack traces and interactive tooling can expose internals in production misconfigurations.
- Recommendation:
  - Enforce `debug=False` outside local development and gate by environment.

### SEC-05: OAuth callback validation and route wiring weaknesses
- Evidence:
  - `oauth_processers.py` uses `callback_url.startswith(CHAT_GPT_URL)` before null checks.
  - OAuth blueprint is not registered in app.
- Risk:
  - Runtime exceptions or bypass opportunities in callback processing.
  - Security logic present but not reliably active due to missing route registration.
- Recommendation:
  - Register OAuth routes explicitly.
  - Validate required params before using string methods.
  - Enforce strict allowlist parsing for callback hosts.

## Medium

### SEC-06: No timeout/retry strategy for external network calls
- Evidence:
  - `requests.post/get` calls in multiple modules do not set explicit timeouts.
- Risk:
  - Request hangs and resource exhaustion can become availability/security incidents.
- Recommendation:
  - Set bounded timeouts and retry/backoff policy per integration.

### SEC-07: Weak integrity guarantees in multi-step complaint workflow
- Evidence:
  - Multi-table writes and external side effects occur without DB transaction boundary.
- Risk:
  - Partial states can be weaponized or degrade trust in system records.
- Recommendation:
  - Wrap persistence in transaction.
  - Move non-critical side effects to async jobs with retry + dead-letter handling.

### SEC-08: Inconsistent schema/code can create unsafe failure modes
- Evidence:
  - `db.sql` references non-existent `complaints.location_id`.
  - Session insert flow conflicts with `NOT NULL` `complaint_id`.
  - `geocoding.py` targets `address_directory` table absent in schema.
- Risk:
  - Unexpected runtime errors, partial writes, and undefined operational behavior.
- Recommendation:
  - Align schema and code through migrations and CI schema checks.

## Low

### SEC-09: Legacy helper scripts and env naming inconsistencies
- Evidence:
  - `supabase-jwt.py` uses `SUPABASE_JWT_SECRET1` and prints generated tokens.
  - README and `.env.example` differ on key naming (`SUPABASE_KEY` vs `SUPABASE_SERVICE_ROLE`).
- Risk:
  - Operator mistakes can lead to insecure deployments.
- Recommendation:
  - Decommission or isolate helper scripts.
  - Standardize environment contract and validate at startup.

## Remediation Plan

## Immediate (0-7 days)
- Enforce auth on all public write endpoints.
- Remove sensitive logging and disable debug mode.
- Register and harden OAuth callback path.
- Add RLS policies for all exposed `public` tables.

## Near-term (1-3 weeks)
- Replace service-role in request path with scoped model.
- Implement transaction-safe complaint intake and async side effects.
- Add timeout/retry policy for all external integrations.

## Medium-term (3-6 weeks)
- Introduce migration-based schema governance and CI checks.
- Add automated security tests:
  - authz regression tests
  - RLS policy verification tests
  - secret scanning and dependency checks
