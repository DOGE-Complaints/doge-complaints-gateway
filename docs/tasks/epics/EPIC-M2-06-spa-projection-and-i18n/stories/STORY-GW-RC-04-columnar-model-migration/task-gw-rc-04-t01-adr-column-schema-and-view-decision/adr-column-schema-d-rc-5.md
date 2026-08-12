# ADR: D-RC-5 columnar schema for `doge_issues`

**Status:** Accepted  
**Story:** STORY-GW-RC-04  
**Date:** 2026-06-19  

## Context

`doge_issues` stores identity columns (`issue_id`, `status`, `created_at`, …) alongside a monolithic `payload_json` blob that duplicates the same facts. Read-path already treats columns as truth for `id`/`status`/`created_at` (GW-RC-01). D-RC-5 removes the blob and assigns each contract field a single storage home.

## Decision

### Scalar columns

| Column | Type | Maps to contract |
|--------|------|------------------|
| `issue_id` | text PK | `id` (read only) |
| `status` | text NOT NULL | `status` |
| `policy_version` | text NOT NULL | internal |
| `created_at` / `updated_at` | timestamptz | `created_at` (read) |
| `issue_type` | text NOT NULL | `type` (canonical on read) |
| `arweave_txid` | text NULL | optional |
| `image_txid` | text NULL | optional |
| `image_hash` | text NULL | optional |

### JSONB / TEXT json columns (not explode)

| Column | Type | Maps to contract |
|--------|------|------------------|
| `labels_json` | jsonb NOT NULL DEFAULT `[]` | `labels` |
| `title_json` | jsonb NOT NULL DEFAULT `{}` | `title` |
| `summary_json` | jsonb NOT NULL DEFAULT `{}` | `summary` |
| `description_json` | jsonb NOT NULL DEFAULT `{}` | `description` |
| `institution_json` | jsonb NULL | `institution` |
| `geo_json` | jsonb NULL | `geo` |
| `original_locale_json` | jsonb NOT NULL DEFAULT `[]` | `original_locale` |

**i18n:** keep locale maps as jsonb columns (`title_json`, …). Do **not** explode to `_et/_ru/_en` scalars — contract is open-ended locale keys; jsonb matches `DOGEIssue.to_public_dict()` and existing filter logic.

**geo:** single `geo_json` jsonb column. Admin sub-fields stay inside the object (same shape as today). No duplicate admin scalar columns on `doge_issues` (stories table already has geo admin columns for intake; projection geo is a denormalized snapshot).

### Drop `payload_json`

After backfill migration (T07), `payload_json` is **dropped**. Write-path (T03+) never writes it.

### View `issues_dashboard`

**Keep** the view for SPA direct-read (anon/authenticated grant). **Rewrite** on columnar sources:

- `type` ← `issue_type`
- `title_en/et/ru` ← `title_json->>'en'` etc.
- `labels_json` ← `labels_json` column (not nested in blob)
- Remove trailing `payload_json` column from view output

Source table: `public.doge_issues` (post REQ-27 rename).

## Consequences

- External API shape unchanged (`dto.py` contract).
- Three backends share mapping via `core.projection.columnar_storage`.
- `parse_payload_json` retained only for legacy backfill / tests until T07 completes.
- `scripts/reproject_issue_i18n.py` writes via `save_projection` → columnar columns automatically.

## Alternatives rejected

| Option | Why rejected |
|--------|----------------|
| Explode i18n to `_et/_ru/_en` scalars | Fixed locale set; harder to extend; duplicates jsonb elsewhere in gateway |
| Geo admin scalar columns on `doge_issues` | Partial overlap with `geo_json`; two sources of truth |
| Drop `issues_dashboard` | SPA still uses direct Supabase read; view is cheap projection for dashboard |
