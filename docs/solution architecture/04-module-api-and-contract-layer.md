# 04. Module: API & Contract Layer

## Responsibilities
- Приём narrative package.
- Единая валидация входных контрактов.
- Стабильные response envelopes.
- Контроль auth/authz/policy на границе.

## Architecture pattern (from node reference)
- `api/main` + middleware chain;
- `api/dependencies` как DI-bridge;
- routes тонкие, orchestration в application service.

## Required interfaces
- `StoryIntakeRequest` v2 (versioned `m2.story_intake_envelope.v2`), включая:
  - **`submitter`** — `external_user_id` (обязательный) + `identity_issuer` (обязательный, eID gate)
  - **`narrative.title`** — `{et, ru, en}` dict, обязательный
  - **`narrative.description`** — `{et, ru, en}` dict, обязательный
  - **`narrative.summary`** — `{et, ru, en}` dict, опциональный
  - **`narrative.session_language`** — `"et"|"ru"|"en"`, обязательный
  - **`narrative.canonical_type`**, **`narrative.canonical_labels`** — опциональные GPT-классификаторы
  - (OAuth на стороне GPT; формат id не фиксируется; см. REQ-33)
- `StoryIntakeResponse` — `story_id`, `status`, `trace_id`.
- `IssueProjectionResponse` (SPA shape).
- `POST /issues` — эндпоинт **не реализован**; требует отдельной задачи (REQ-39).
- `ErrorEnvelope` (unified).

## Rules
- GPT не является source-of-truth для status/publish.
- strict schema validation + semantic validation в service layer:
  - отсутствие `identity_issuer` → HTTP 400 (eID gate)
  - отсутствие `title`, `description`, `session_language` → HTTP 400
- `simulate_error`-style тестовый режим опционально для demo.
- `Idempotency-Key` header: при отсутствии — SHA-256 от raw request body (auto-fallback).

## NFR
- p95 latency intake <= 400ms без внешних slow calls.
- idempotency key support на intake endpoint (header или SHA-256 fallback).
- request trace id в каждом ответе.

## Решения интервью (2026-05-13)
- Schema version v1 → v2 (breaking change)
- `identity_issuer` из optional → required (eID gate на intake)
- `title_hint` (single string) → `title` (`{et,ru,en}`) — удалить старые flat поля
- `description` — новое обязательное multilingual поле
- `session_language` — новое обязательное поле в `narrative`
- SHA-256 idempotency fallback (G-08)
- Подробнее: см. REQ-33, `docs/analysis/gap-interview-decisions-2026-05-13.md` G-01/G-08
