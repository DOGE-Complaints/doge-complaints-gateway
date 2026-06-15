# DOGE Complaints Gateway API Reference

## 1. Overview

This reference describes the runtime API surface for `doge-complaints-gateway` with explicit state separation:

- **As-is**: behavior implemented in `FastAPI` transport routes (`src/core/api/asgi_app.py`) backed by handler functions.
- **Planned**: extended endpoint surfaces not yet wired in the runtime transport layer.

The canonical machine-readable contract is:

- `docs/runtime-docs/api-reference/openapi.yaml`

## 2. Runtime Boundary

Current runtime is **ASGI/FastAPI-driven** under `src/core/api/asgi_app.py`.

This means:

1. Operational behaviors (`health`, `ready`, `protected`, `metrics`) are implemented and routable over HTTP.
2. Intake (`POST /intake/stories`) and issues (`GET /tallinn/issues`, `GET /tallinn/issues/{issue_id}`, `POST /tallinn/issues`) are implemented and routable.
3. Public/protected policy is declared in route definitions and validated by transport smoke tests.
4. Demo static routes are also active in the same ASGI process:
   - `GET /demo/auth-page`
   - `GET /demo/auth-page/`
   - `GET /demo/auth-page/styles.css`

## 3. Authentication Model

### As-is

Service-to-service authentication is implemented via:

- `Authorization: Bearer <SERVICE_API_TOKEN>`
- `X-Service-Token: <SERVICE_API_TOKEN>`

Implementation sources:

- `src/core/api/security.py`
- `src/core/api/asgi_app.py` (route dependency policy)
- `src/core/api/handlers.py` (defense-in-depth auth checks)

If `SERVICE_API_TOKEN` is unset, auth is disabled by design in demo runtime mode.
For pilot profile, config loading now fails fast when `SERVICE_API_TOKEN` is missing.

### Planned

- Formal key lifecycle policy (rotation/revocation/audit procedures).
- Optional multi-key/keyset strategy for higher-assurance environments.

## 4. Envelope and Error Contract

All operations are expected to return a unified envelope:

- Success: `{ "data": { ... }, "trace_id": "..." }`
- Error: `{ "error": { code, type, message, details }, "trace_id": "..." }`

Error mapping is implemented in:

- `src/core/api/envelope.py`

Validated in:

- `tests/test_error_envelope_contract.py`
- `tests/test_trace_propagation.py`

## 5. Ops Endpoints (as-is behavior, active HTTP binding)

### `GET /health`

- **As-is implementation**: `GET /health` in `asgi_app` -> `handle_health`
- **Purpose**: liveness status from `HealthService`
- **Success example**:

```json
{
  "data": {
    "status": "ok"
  },
  "trace_id": "trace-health-1"
}
```

### `GET /ready`

- **As-is implementation**: `GET /ready` in `asgi_app` -> `handle_readiness`
- **Purpose**: readiness signal for runtime checks
- **Success example**:

```json
{
  "data": {
    "status": "ready",
    "db": {
      "backend": "supabase",
      "ready": true,
      "checks": {
        "connectivity": true,
        "schema": true,
        "policy_probe": true
      }
    }
  },
  "trace_id": "trace-ready-1"
}
```

### `GET /protected/status`

- **As-is implementation**: `GET /protected/status` in `asgi_app` -> `handle_protected_status`
- **Purpose**: verify service-token gate behavior
- **Auth required**: Bearer token or `X-Service-Token` when auth is enabled
- **Unauthorized example**:

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "type": "auth",
    "message": "Missing service API token.",
    "details": {}
  },
  "trace_id": "trace-protected-err-1"
}
```

### `GET /metrics`

- **As-is implementation**: `GET /metrics` in `asgi_app` -> `handle_metrics`
- **Purpose**: in-process counters (`health_requests`, `readiness_requests`, `protected_requests`, `metrics_requests`, `auth_failures`)
- **Auth required**: Bearer token or `X-Service-Token` when auth is enabled

## 6. Intake Endpoint (implemented HTTP binding)

### `POST /intake/stories`

- **Contract**: `src/core/intake/contracts.py`, `src/core/application/services.py`
- **HTTP binding**: `asgi_app.py:394-409` → `handle_story_intake` (`handlers.py:124-280`)
- **HTTP status on success**: `202 Accepted`
- **Request Content-Type**: `application/json`

---

### 6.1 Request Headers

| Header | Required | Notes |
|--------|----------|-------|
| `Content-Type` | yes | Must be `application/json` |
| `X-Trace-Id` | no | Propagated into response `trace_id`; generated if absent |
| `Idempotency-Key` | no | If absent, SHA-256 of raw request body bytes is used as key |

**Idempotency semantics**: if the key matches an existing record, the original story is returned without creating a duplicate. The key must be a non-empty string after `.strip()`.

---

### 6.2 Request body schema

```json
{
  "schema_version": "m2.story_intake_envelope.v2",
  "submitter": {
    "external_user_id": "<string>",
    "identity_issuer": "<string>"
  },
  "narrative": {
    "original_text": "<string>",
    "language": "et | ru | en",
    "session_language": "et | ru | en",
    "title": { "et": "<string>", "ru": "<string>", "en": "<string>" },
    "description": { "et": "<string>", "ru": "<string>", "en": "<string>" },
    "summary": { "et": "<string>", "ru": "<string>", "en": "<string>" },
    "location_query": "<string>",
    "canonical_type": "<string>",
    "canonical_labels": ["<string>", "..."]
  },
  "origin": {
    "source": "<string>",
    "conversation_id": "<string>",
    "tool_call_id": "<string>"
  },
  "privacy": {
    "contains_pii": false,
    "redaction_requested": false
  },
  "live_story_context": {
    "consistency_notes": "<string>"
  },
  "gpt_signals": {
    "severity": "HIGH",
    "impact_estimation": "DISTRICT",
    "problem_status": "ONGOING"
  }
}
```

Optional `gpt_signals` is persisted to `story_signals` with `extraction_policy = "gpt.story_classifier.v1"`; it is **not** copied into `StoryRecord`.

---

### 6.3 Field reference

#### `schema_version` — string, **required**

Exact value: `"m2.story_intake_envelope.v2"`

`"m2.story_intake_envelope.v1"` is explicitly rejected with a 400 and a migration message. Any other value is also rejected.

Source: `contracts.py:14-15`, `parse_story_intake_request:113-123`

---

#### `submitter` — object, **required**

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| `external_user_id` | string | **yes** | Non-empty after `.strip()` |
| `identity_issuer` | string | **yes** | Non-empty after `.strip()` |

Both fields must be present and non-empty strings. Missing or empty → `400 IntakeValidationError`.

Mapped to `StoryRecord.submitter_external_user_id` and `StoryRecord.submitter_identity_issuer`.

Source: `contracts.py:24-27`, `parse_story_intake_request:125-133`

---

#### `narrative` — object, **required**

| Field | Type | Required | Validation | Normalization |
|-------|------|----------|-----------|--------------|
| `original_text` | string | **yes** | Non-empty after `.strip()` | stored as-is (stripped) |
| `language` | string | **yes** | One of `et`, `ru`, `en` | lowercased |
| `session_language` | string | **yes** | One of `et`, `ru`, `en` | lowercased |
| `title` | object | **yes** | All three keys `et`, `ru`, `en` must be non-empty strings | each value stripped |
| `description` | object | **yes** | All three keys `et`, `ru`, `en` must be non-empty strings | each value stripped |
| `summary` | object | no | If present: must have all three `et`, `ru`, `en` non-empty strings | each value stripped |
| `institution` | object | no | If present: must have all three `et`, `ru`, `en` non-empty strings | each value stripped; persisted as `stories.institution_json` |
| `location_query` | string | no | Empty/whitespace-only string → stored as `None` | stripped |
| `canonical_type` | string | no | Empty/whitespace-only → stored as `None`; no enum validation at intake | stripped |
| `canonical_labels` | string[] | no | If present: must be a JSON array; each element a non-empty string | `.strip().lower()`; deduplicated preserving first-occurrence order |

**`language` vs `session_language`**: `language` is the language of `original_text`; `session_language` is the language the user is interacting in (may differ if GPT translated the story). Both validated against `I18N_LANGS = ("et", "ru", "en")`.

**`canonical_type`** — semantics from GPT taxonomy (no enum enforcement at intake):
- `"complaint"` — actionable civic complaint
- `"observation"` — observation without explicit ask
- `"system_bug"` — digital/system malfunction
- `"absurdity"` — absurd bureaucratic situation

Only stories with `canonical_type` in `{"complaint", "system_bug"}` pass the promotion gate for issue creation (REQ-34). All values accepted at intake; absent `canonical_type` reduces the story's `alpha_score` by 12 points.

**`canonical_labels`** — free-form tag strings produced by GPT. Normalized: `.strip().lower()`, deduped preserving order. Drive cluster key derivation for civic lenses.

Source: `contracts.py:30-40`, `narrative_i18n.py`, `parse_story_intake_request:135-196`

---

#### `origin` — object, optional

If present, must be a JSON object (even with all inner fields absent).

| Field | Type | Normalization |
|-------|------|--------------|
| `source` | string | stripped; empty/whitespace → `None` |
| `conversation_id` | string | stripped; empty/whitespace → `None` |
| `tool_call_id` | string | stripped; empty/whitespace → `None` |

Mapped to `StoryRecord.origin_source`, `.origin_conversation_id`, `.origin_tool_call_id`.

Source: `contracts.py:44-47`, `parse_story_intake_request:198-216`

---

#### `privacy` — object, optional

If present, must be a JSON object.

| Field | Type | Default | Validation |
|-------|------|---------|-----------|
| `contains_pii` | boolean | `false` | Must be a JSON boolean; non-boolean → `400` |
| `redaction_requested` | boolean | `false` | Must be a JSON boolean; non-boolean → `400` |

If `contains_pii=true`, the first 50 chars of `original_text` are redacted in logs.

Mapped to `StoryRecord.privacy_contains_pii`, `.privacy_redaction_requested`.

Source: `contracts.py:51-53`, `parse_story_intake_request:218-234`, `services.py:79-83`

---

#### `live_story_context` — object, optional

| Field | Type | Normalization |
|-------|------|--------------|
| `consistency_notes` | string | stripped; empty/whitespace → `None` |

Mapped to `StoryRecord.narrative_consistency_notes`.

Source: `contracts.py:56-58`, `parse_story_intake_request:236-246`

---

#### `gpt_signals` — object, optional (REQ-42)

If the key is **absent**, no `story_signals` row is written for policy `gpt.story_classifier.v1`.

If the key is **present** (including `{}`), each supplied field is validated and persisted via `StorySignalStore.save_signals()` after the story is saved. Invalid enum values → `400 IntakeValidationError`.

| Field | Type | Required when block present | Allowed values |
|-------|------|----------------------------|----------------|
| `severity` | string | no | `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` (case-insensitive input, stored uppercase) |
| `impact_estimation` | string | no | `LOCAL`, `DISTRICT`, `CITY`, `NATIONAL` |
| `problem_status` | string | no | `ONGOING`, `RESOLVED`, `RECURRING`, `UNKNOWN` |

Persisted `signals_json` always includes `"source": "gpt_intake_v1"`. A failure to persist signals is logged and does **not** change HTTP `202` for the intake.

Source: `contracts.py` (`GptSignalsBlock`, `parse_story_intake_request`), `services.py` (`GPT_CLASSIFIER_POLICY_VERSION`, `_persist_gpt_classifier_signals`)

---

### 6.4 Full request example

```json
{
  "schema_version": "m2.story_intake_envelope.v2",
  "submitter": {
    "external_user_id": "telegram:123456789",
    "identity_issuer": "telegram"
  },
  "narrative": {
    "original_text": "Kesklinna linnaosas on Tartu mnt 80 ees suur auk kõnniteel, mis on ohtlik jalakäijatele.",
    "language": "et",
    "session_language": "et",
    "title": {
      "et": "Ohtlik auk kõnniteel",
      "ru": "Опасная яма на тротуаре",
      "en": "Dangerous pothole on sidewalk"
    },
    "description": {
      "et": "Tartu mnt 80 ees on suur auk, mis ohustab jalakäijaid.",
      "ru": "Перед домом по адресу Tartu mnt 80 яма, представляющая угрозу для пешеходов.",
      "en": "A large pothole in front of Tartu mnt 80 poses danger to pedestrians."
    },
    "summary": {
      "et": "Auk kõnniteel Kesklinna linnaosas.",
      "ru": "Яма на тротуаре в Центральном районе.",
      "en": "Pothole on sidewalk in Kesklinn district."
    },
    "location_query": "Tartu mnt 80, Tallinn",
    "canonical_type": "complaint",
    "canonical_labels": ["pothole", "road_maintenance", "pedestrian_safety"]
  },
  "origin": {
    "source": "telegram_bot",
    "conversation_id": "conv-abc-123",
    "tool_call_id": "call-xyz-456"
  },
  "privacy": {
    "contains_pii": false,
    "redaction_requested": false
  }
}
```

---

### 6.5 Lifecycle after intake

After persisting, the service immediately advances the story lifecycle:

| Condition (`narrative_v2_complete()`) | Resulting `lifecycle_status` |
|---------------------------------------|------------------------------|
| All required text fields non-empty (`original_text`, `language`, `session_language`, all `title.*`, all `description.*`) | `ready_for_profile` |
| Any required field empty or missing | `partial_ready` |

Stories in `ready_for_profile` are picked up by the clustering cron. Stories in `partial_ready` are not clustered.

Source: `services.py:233-241`, `narrative_i18n.py:91-105`

---

### 6.6 Response (202 Accepted)

```json
{
  "data": {
    "schema_version": "m2.story_intake_response.v1",
    "story_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "ready_for_profile",
    "intake_notes": {
      "geo_resolved": true,
      "gpt_signals_persisted": true
    }
  },
  "trace_id": "abc123"
}
```

`status` is `"ready_for_profile"` or `"partial_ready"` depending on completeness of narrative fields.

`intake_notes` (REQ-46): transparency flags for the intake path (not persisted on `StoryRecord`).

| Field | Meaning |
|-------|---------|
| `geo_resolved` | `true` when `location_query` was resolved to a geo snapshot |
| `gpt_signals_persisted` | `true` when there were no `gpt_signals` to save, or when the signal store accepted the block; `false` when signals were present but not stored (missing store or persist error) |

---

### 6.7 Error responses

| HTTP | Condition |
|------|-----------|
| `400` | `schema_version` wrong, required field missing/empty, `canonical_labels` not array, boolean field not bool |
| `422` | `location_query` resolved to geo outside `CLUSTER_GEO_SCOPE` (when scope is configured) |
| `500` | Unexpected internal error |

---

### 6.8 Mapping: request → StoryRecord

| Request field | StoryRecord field |
|---------------|------------------|
| `schema_version` | `schema_version` |
| `submitter.external_user_id` | `submitter_external_user_id` |
| `submitter.identity_issuer` | `submitter_identity_issuer` |
| `narrative.original_text` | `narrative_original_text` |
| `narrative.language` | `narrative_language` |
| `narrative.session_language` | `narrative_session_language` |
| `narrative.title` | `narrative_title` (dict) |
| `narrative.description` | `narrative_description` (dict) |
| `narrative.summary` | `narrative_summary` (dict or `None`) |
| `narrative.institution` | `narrative_institution` (dict or `None`; column `institution_json`) |
| `narrative.location_query` | resolved → `geo` (`StoryGeoSnapshot`) |
| `narrative.canonical_type` | `narrative_canonical_type` |
| `narrative.canonical_labels` | `narrative_canonical_labels` (tuple) |
| `origin.source` | `origin_source` |
| `origin.conversation_id` | `origin_conversation_id` |
| `origin.tool_call_id` | `origin_tool_call_id` |
| `privacy.contains_pii` | `privacy_contains_pii` |
| `privacy.redaction_requested` | `privacy_redaction_requested` |
| `live_story_context.consistency_notes` | `narrative_consistency_notes` |
| — (server-generated) | `story_id` (UUID4) |
| — (server-generated) | `created_at`, `updated_at` (UTC) |
| — (server-generated) | `lifecycle_status` → `ready_for_profile` or `partial_ready` |

Source: `services.py:143-178`

---

### 6.9 Code sources

- `src/core/intake/contracts.py` — `StoryIntakeRequest`, `parse_story_intake_request()`, schema version constants
- `src/core/domain/narrative_i18n.py` — `I18N_LANGS`, `parse_required_i18n_dict()`, `narrative_v2_complete()`
- `src/core/application/services.py` — `StoryIntakeService.create_story()`, `advance_story_readiness()`
- `src/core/domain/contracts.py` — `StoryRecord`, `StoryLifecycleStatus`
- `src/core/api/idempotency.py` — `resolve_idempotency_key()`
- `src/core/geo/scope.py` — `GeoScopeMismatchError`, `assert_geo_in_scope()`

Test evidence:

- `tests/test_story_intake_contract.py`
- `tests/test_story_repository_lifecycle.py`
- `tests/test_story_intake_idempotency.py`

## 6.5 Label miss telemetry (GW-L10N-03)

Anonymous sink when SPA humanize cannot find a label translation. **No auth**, **no PII** — only canonical `label_key` and `locale`.

### `POST /telemetry/label-misses`

- **HTTP binding:** `asgi_app.py` → `handle_label_miss_telemetry` (`handlers.py`)
- **Auth:** public (no `SERVICE_API_TOKEN`)
- **Body:** `{ "label_key": string, "locale": "et"|"ru"|"en" }`
- **Success:** `202 Accepted` — `{ "data": { "accepted": true|false }, "trace_id": "..." }`
  - `accepted: true` when persisted to `label_translation_misses`
  - `accepted: false` on store degrade (endpoint still returns 202; process stable)
- **Validation error:** `400` — generic `VALIDATION_ERROR` / `"Invalid request"` (no field leak)
- **Storage:** aggregate table `label_translation_misses` (`label_key`, `locale`, `miss_count`, `last_seen_at`)
- **Operator queries:** [`appendix/label-translation-misses-operator-ru.md`](../appendix/label-translation-misses-operator-ru.md)

Test evidence: `tests/test_gw_l10n_03_label_miss_telemetry.py`

---

## 7. Issues API (as-is behavior, active HTTP binding)

All three `POST /tallinn/issues` endpoints are registered in `asgi_app.py` and routable in the current runtime.

### Issue projection i18n (GW-L10N-01)

Public issue fields `title`, `summary`, and `description` are stored as `{ et, ru, en }` objects. **Locale values may differ** — the gateway preserves per-locale text from the dominant linked story (cluster projection) or from the operator-supplied title on manual `POST /tallinn/issues`; identical copies across all three keys are not required when source narratives differ.

**`original_locale`** (GW-L10N-02): optional `string[]` on list/get responses. Unique `narrative_language` values from all linked stories in canonical order `et`, `ru`, `en`. Omitted when no known language. SPA treats locales outside the list as machine-translated.

Source: `extraction_policy.py` (`DeterministicStoryToProjectionPolicy.build_draft`), `issue_create.py` (`StoryPromotionProjectionBridge`, `create_manual_issue`), `i18n.py` (`original_locale_from_languages`).

---

### `GET /tallinn/issues`

- **HTTP binding state**: implemented — `asgi_app.py:322-361` → `handle_tallinn_issues_list` (`handlers.py:281-333`)
- **Auth**: public (no token required)
- **Returns**: `200` with `data.issues` — list of `DOGEIssue.to_public_dict()` shapes

#### Query parameters

All parameters are optional and can be combined.

| Parameter | Type | Semantics |
|-----------|------|-----------|
| `status` | `string[]` | Multi-value OR filter: `DRAFT`, `PUBLISHED` |
| `type` | `string` | Exact match: `complaint`, `system_bug`, `observation`, `absurdity` |
| `labels` | `string[]` | Multi-value OR — issue must carry at least one of the supplied labels |
| `institution` | `string` | Exact match on `payload_json.institution`: compares against any of `et`, `ru`, `en` when stored as i18n object (REQ-43) |
| `created_after` | `string` | ISO 8601 lower bound on `created_at` (inclusive) |
| `created_before` | `string` | ISO 8601 upper bound on `created_at` (inclusive) |
| `geo_lat_min` | `float` | Bounding-box south edge (latitude) |
| `geo_lat_max` | `float` | Bounding-box north edge (latitude) |
| `geo_lon_min` | `float` | Bounding-box west edge (longitude) |
| `geo_lon_max` | `float` | Bounding-box east edge (longitude) |
| `geo_district` | `string[]` | Multi-value OR on `geo.admin_district` |
| `geo_settlement` | `string[]` | Multi-value OR on `geo.admin_settlement` |
| `geo_region` | `string[]` | Multi-value OR on `geo.admin_region` |
| `geo_country` | `string[]` | Multi-value OR on `geo.admin_country` |
| `geo_postal_code` | `string[]` | Multi-value OR on `geo.admin_postal_code` |

Multi-value parameters are supplied as repeated query params: `?geo_district=Kesklinn&geo_district=Põhja-Tallinn`

#### Success example

```json
{
  "data": {
    "issues": [
      {
        "id": "a1b2c3d4-...",
        "status": "PUBLISHED",
        "type": "complaint",
        "labels": ["pothole", "road_maintenance"],
        "title": { "et": "Katki läinud tänav", "en": "Broken street" },
        "summary": { "et": "...", "en": "..." },
        "description": { "et": "...", "en": "..." },
        "institution": {
          "et": "Tallinna Linnavalitsus",
          "ru": "Таллинская городская управа",
          "en": "Tallinn City Government"
        },
        "created_at": "2026-05-01T10:00:00Z",
        "geo": {
          "admin_district": "Kesklinn",
          "admin_settlement": "tallinn",
          "admin_country": "ee",
          "lat": 59.437,
          "lon": 24.753
        }
      }
    ]
  },
  "trace_id": "trace-001"
}
```

---

### `GET /tallinn/issues/{issue_id}`

- **HTTP binding state**: implemented — `asgi_app.py:364-375` → `handle_tallinn_issue_get` (`handlers.py:336-362`)
- **Auth**: public (no token required)
- **Returns**: `200` with `data.issue` on success, `404` if no issue with that `issue_id` exists

#### Success example

```json
{
  "data": {
    "issue": {
      "id": "a1b2c3d4-...",
      "status": "PUBLISHED",
      "type": "complaint",
      "labels": ["pothole"],
      "title": { "et": "Katki läinud tänav", "en": "Broken street" },
      "summary": { "et": "...", "en": "..." },
      "description": { "et": "...", "en": "..." },
      "created_at": "2026-05-01T10:00:00Z"
    }
  },
  "trace_id": "trace-002"
}
```

#### Not-found example

```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "type": "internal",
    "message": "Issue not found: a1b2c3d4-...",
    "details": {}
  },
  "trace_id": "trace-002"
}
```

---

### `POST /tallinn/issues`

- **HTTP binding state**: implemented — `asgi_app.py:378-391` → `handle_tallinn_issue_create` (`handlers.py:365-396`)
- **Auth required**: Bearer token or `X-Service-Token` — same service-auth gate as `/protected/status`
- **Purpose**: operator-initiated manual issue creation from a set of story IDs
- **Returns**: `201` on success, `400` on validation error, `401` on auth failure

#### Request body

```json
{
  "cluster_id": "sha256-cluster-key-...",
  "story_ids": ["story-uuid-1", "story-uuid-2"],
  "title": { "et": "Käsitsi loodud probleem", "en": "Manually created issue" },
  "type": "complaint"
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `cluster_id` | string | yes | Cluster the issue belongs to |
| `story_ids` | string[] | yes | Must be a JSON array |
| `title` | object | yes | Multilingual title map (`et`, `ru`, `en`); **locales may differ** (GW-L10N-01) |
| `type` | string | no | Defaults to `"complaint"` |

#### Success example

```json
{
  "data": {
    "issue_id": "a1b2c3d4-..."
  },
  "trace_id": "trace-003"
}
```

#### Validation error example

```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "type": "internal",
    "message": "story_ids must be a list.",
    "details": {}
  },
  "trace_id": "trace-003"
}
```

---

## 8. Observability Notes

- `trace_id` is preserved or generated in API envelopes (`ensure_trace_id`).
- Auth failure metrics are exposed via `ApiMetrics` and can be checked by `alert_contract`.

Sources:

- `src/core/api/envelope.py`
- `src/core/api/metrics.py`
- `tests/test_api_security_and_ops.py`
- `tests/test_trace_propagation.py`

## 9. As-is vs Planned Summary

### As-is

- FastAPI/ASGI runtime entrypoint and routable HTTP operations.
- Envelope/error/trace consistency.
- Service-token gate on protected operations:
  - `GET /protected/status`
  - `GET /metrics`
  - `POST /tallinn/issues`
- Public operations (no auth required):
  - `GET /health`
  - `GET /ready`
  - `POST /intake/stories` (202 Accepted — clustering deferred to cron)
  - `POST /telemetry/label-misses` (202 Accepted — anonymous label miss telemetry, GW-L10N-03)
  - `GET /tallinn/issues` (15-parameter filter API)
  - `GET /tallinn/issues/{issue_id}`

### Planned

- Formal key lifecycle policy (rotation/revocation/audit procedures).
- Optional multi-key/keyset strategy for higher-assurance environments.
- `PATCH /tallinn/issues/{issue_id}` — status transitions (DRAFT → PUBLISHED) by operator.

## 10. Compatibility Guidance

For integrators:

1. Treat `openapi.yaml` as the normative reference format.
2. All endpoints listed in sections 5, 6, and 7 are routable in the current runtime.
3. `POST /intake/stories` returns `202 Accepted` — the story is queued for clustering; do not retry on 202.
4. `GET /tallinn/issues` multi-value filters use repeated query params, not comma-separated strings.
5. Demo static routes are active and routable in current runtime (`/demo/auth-page*`).
6. `POST /tallinn/issues` is for operator use only and requires `SERVICE_API_TOKEN`.
