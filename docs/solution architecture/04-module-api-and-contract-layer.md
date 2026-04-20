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
- `StoryIntakeRequest` (versioned), включая **`submitter`** — opaque `external_user_id` и опционально `identity_issuer` для авторства (OAuth на стороне GPT; формат id не фиксируется; см. `requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md`).
- `StoryIntakeResponse`.
- `IssueProjectionResponse` (SPA shape).
- `ErrorEnvelope` (unified).

## Rules
- GPT не является source-of-truth для status/publish.
- `simulate_error`-style тестовый режим опционально для demo.
- strict schema validation + semantic validation в service layer.

## NFR
- p95 latency intake <= 400ms без внешних slow calls.
- idempotency key support на intake endpoint.
- request trace id в каждом ответе.
