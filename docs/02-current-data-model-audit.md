# DOGE Complaints Gateway: Current Data Model Audit

## Scope and Inputs

This document reflects the data model as inferred from:
- `db.sql` (declared schema)
- Python write/read paths in `app/services/` and `app/utils/`
- payload examples in `complaint-input-demo.json`
- action contract in `gpt-actions.yaml`

## Declared Relational Model (`db.sql`)

## Core entities
- `oauth_users`
  - External user mapping by `oauth_provider_user_id + oauth_provider`
- `complaints`
  - Main complaint facts (reporter name, description, severity, impact, status, geo point, metadata)
- `session_complaints`
  - Session-to-complaint binding with optional `user_id`
- `complaint_time`
  - Flexible time representation (exact/date/range variants)

## Dictionary and relation entities
- `dictionary_problem_categories`
- `complaint_problem_categories`
- `dictionary_related_events`
- `complaint_related_events`

## Embedding entities
- `problem_category_embeddings` with `VECTOR(384)`
- `related_event_embeddings` with `VECTOR(384)`

## Location cache
- `location_directory`
  - Declared as unique by `location_details`

## Key integrity observations

### 1) Invalid index definition in schema
- `db.sql` creates `idx_complaints_location_id` on `complaints(location_id)`.
- `complaints` has no `location_id` column.
- Effect: schema bootstrap can fail or drift from expected state.

### 2) Session table constraints conflict with route behavior
- `session_complaints.complaint_id` is `NOT NULL`.
- `/generate-session` inserts only `session_id`.
- Effect: route can fail under strict schema.

### 3) Missing uniqueness constraints on relation tables
- No composite unique keys on:
  - `complaint_problem_categories (complaint_id, category_id)`
  - `complaint_related_events (complaint_id, event_id)`
- Effect: duplicate edges are possible.

### 4) No explicit uniqueness on `session_id`
- `session_complaints.session_id` is indexed but not unique.
- Effect: duplicate sessions can exist and break one-to-one assumptions in code.

### 5) Enum governance is application-only
- Severity, impact, status, time type are not DB enums/check constraints.
- Effect: mixed value formats can enter DB (`high` vs `High`, `pending_review` vs `Pending Review`).

## Runtime Model (As Used by Code)

## Complaint intake path
`submit_complaint.py` writes:
1. `complaints`
2. `complaint_time`
3. dictionary table upsert-like behavior for categories/events
4. embeddings for newly created dictionary rows
5. many-to-many rows
6. session link (conditionally)

## Mismatch hotspots
- `complaint-input-demo.json` uses `time.type = exact_date` which is not handled by `ComplaintTimeType`.
- `setComplaintTime()` logic checks for `time_interval` and `approx_period` using fallback branches unrelated to `type` value.
- `geocoding.py` writes to `address_directory`, but declared table is `location_directory`.

## Conceptual ER (Current Intent)

- One `oauth_user` -> many `session_complaints`
- One `complaint` -> one `complaint_time` (intended, not enforced)
- One `complaint` <-> many `problem_categories`
- One `complaint` <-> many `related_events`
- One dictionary category/event -> one embedding row (intended, not enforced by unique key)

## Data Quality Risks

### High
- Schema/code divergence can block inserts at runtime (`session_complaints` and bad index).
- Inconsistent enum casing/values reduces analytics quality and filter reliability.

### Medium
- Duplicate bridge rows inflate counts and distort reporting.
- Missing idempotency on session/complaint links causes ambiguous ownership mapping.

### Medium
- Location caching path is incomplete/inconsistent, reducing lookup hit rate and increasing external geocoding calls.

## Recommended Model Hardening

## P0
- Fix broken index (`idx_complaints_location_id`) or add intended `location_id` relation.
- Align `session_complaints` schema with `/generate-session` flow.
- Add unique key on `session_complaints.session_id` if session is intended to be unique.

## P1
- Add composite unique constraints for relation tables.
- Add check constraints or enum types for severity/impact/status/time type.
- Add foreign key strategy for normalized location storage if `location_directory` is intended as source of truth.

## P2
- Add migration-first process (instead of ad-hoc SQL file drift).
- Add data dictionary document with canonical field semantics and allowed values.
- Add model-level tests for payload-to-DB mapping consistency.
