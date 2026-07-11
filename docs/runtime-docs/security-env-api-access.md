# Security, Env, API Access

## Контекст и управленческий вопрос

Ключевой вопрос:  
**какова фактическая security posture текущего runtime, где проходит trust boundary, и как обеспечить предсказуемый режим доступа в production-like окружении?**

## Current state (implemented now)

### 1) Модель доступа к API

В коде реализован **service-to-service gate**, а не пользовательская аутентификация:

- Принимаются токены из:
  - `Authorization: Bearer <token>`
  - `X-Service-Token: <token>`
- Извлечение токена: `extract_service_token` (`src/core/api/security.py`).
- Проверка: `ServiceTokenAuth.require` (`src/core/api/security.py`).
- Transport policy enforcement: `require_service_auth` dependency (`src/core/api/asgi_app.py`).
- Handler-level guard (defense in depth): `handle_protected_status` и `handle_metrics` (`src/core/api/handlers.py`).

Практический смысл: gateway защищает вызовы между сервисами/интеграторами, но не реализует full user auth flow.

Protected/public operation split (as-is, route policy — источник: `asgi_app.py`):

- Protected routes (Bearer token или `X-Service-Token` обязательны):
  - `GET /protected/status`
  - `GET /metrics`
- Public routes (без авторизации):
  - `GET /health`
  - `GET /ready`
  - `GET /demo/auth-page`
  - `GET /demo/auth-page/`
  - `GET /demo/auth-page/styles.css`
  - `POST /intake/stories` ← бизнес-эндпоинт, без auth

**Примечание:** бизнес-эндпоинт intake (`/intake/stories`) намеренно публичен в текущей модели — service-to-service auth применяется только к ops-маршрутам. В pilot-профиле бизнес-эндпоинт может быть защищен при необходимости.

### 1.1) User identifier linkage для stories

Два intake-контракта (GW-DRAFT-05):

| Path | Request schema | Author source |
|------|----------------|---------------|
| `POST /story-drafts` (GPT stash) | `StoryDraftStashRequest` — **без** `submitter` | n/a (draft only) |
| `POST /story-drafts/{id}/submit` (browser) | bridge → `StoryIntakeRequest` | identity `GET /me` → `authoritative_submitter_from_introspection` |
| `POST /intake/stories` (legacy service) | `StoryIntakeRequest` — `submitter` required in payload | payload fields (no `/me` override when `user_introspection=None`) |

- Домен: `parse_story_draft_stash_request`, `parse_story_intake_request`, `intake_request_from_stash_and_submitter` — `src/core/intake/contracts.py`.
- Привязка к доменной модели: `StoryIntakeService.create_story` записывает
  - `submitter_external_user_id=request.submitter.external_user_id`
  - `submitter_identity_issuer=request.submitter.identity_issuer`
  в `StoryRecord` (`src/core/application/services.py`).
- Поля persistence-контракта: `StoryRecord.submitter_external_user_id`, `StoryRecord.submitter_identity_issuer` (`src/core/domain/contracts.py`).

Legacy drafts (pre GW-DRAFT-05) с placeholder submitter в `story_drafts.payload_json` — tolerant read на submit (`parse_stored_draft_stash_request` strips placeholder).

### 2) Поведение auth при наличии/отсутствии секрета

- `SERVICE_API_TOKEN` читается через `build_service_auth_from_env`.
- Если переменная отсутствует или пустая, auth переходит в disabled mode (`require()` становится no-op).
- Для `APP_PROFILE=pilot` runtime config теперь работает в strict mode: `load_config_from_env` вызывает fail-fast при отсутствии `SERVICE_API_TOKEN`.
- Сравнение токена выполняется через `secrets.compare_digest`, что исключает простейшие timing comparison ошибки.

### 3) Error и trace контракт как часть security-операционки

- Ошибки доступа маппятся в `UNAUTHORIZED` envelope (`build_error_envelope`).
- `trace_id` сохраняется в ответах и structured logs:
  - `src/core/api/envelope.py`
  - `src/core/api/logging.py`
  - `tests/test_trace_propagation.py`

### 4) Runtime env contract (фактически используемый)

| Variable | Where used | Operational meaning |
|---|---|---|
| `SERVICE_API_TOKEN` | `src/core/api/security.py` | Включает/фиксирует service auth gate |
| `APP_PROFILE` | `src/core/config/schema.py` | Переключает demo/pilot defaults |
| `API_BASE_URL` | `src/core/config/schema.py` | Обязательный базовый URL runtime profile |
| `REQUEST_TIMEOUT_S` | `src/core/config/schema.py` | Таймаут исходящих запросов/политик |
| `FF_WALLET_ADAPTER` | `src/core/config/schema.py` | Override adapter behavior |
| `FF_BLOCKCHAIN_ADAPTER` | `src/core/config/schema.py` | Override adapter behavior |
| `FF_TOKENIZATION_PIPELINE` | `src/core/config/schema.py` | Override pipeline behavior |
| `LOG_LEVEL` | `src/core/config/schema.py` | Уровень логирования |
| `IDENTITY_BASE_URL` | `src/core/config/schema.py`, `src/core/identity/me_client.py` | Base URL for browser session check via identity `GET /me` (GW-DRAFT-02) |
| `SPA_VERIFY_BASE_URL` | `src/core/identity/verify_url.py` | SPA verify redirect base for `verification_required` (403) responses |

### 4.1) Browser story-draft auth paths (GW-DRAFT-02)

**GET `/story-drafts/{draft_id}` (read / preview):**

- Token extraction: `extract_authorization_bearer` — `Authorization: Bearer` (Supabase session).
- Identity check: `IdentityMeClient.fetch_me` → `GET {IDENTITY_BASE_URL}/me`.
- Dependency: `require_story_draft_read_user` — **active session only** (`result.active=true`); **no** `phone_verified` gate (mvp §4: preview before verify is allowed).
- Fail-closed: missing/inactive token → **401**; identity down / unconfigured → **503**.

**POST `/story-drafts/{draft_id}/submit` (create story):**

- Same Bearer + `/me` client, but dependency `require_story_draft_submit_user` applies full `evaluate_verification_gate` (GAUTH-03): `phone_verified=true` required; `false` → **403** `verification_required` + `verify_url`.
- Fail-closed: `IdentityMeError` or missing client → **503**; story is not created.

Gateway does **not** validate Supabase JWT locally on either path; trust boundary is identity service.

### 4.1.1) Legacy public-content writes — trusted service channel (GW-DRAFT-04)

**`POST /intake/stories` and `POST /tallinn/issues`:**

- Auth: `require_public_content_service_auth` — valid `SERVICE_API_TOKEN` only (`asgi_app.py`).
- **No user-token layer** — OAuth introspection removed (GW-DRAFT-04); payload `submitter` fields persist as provided (no authoritative override when `user_introspection=None`).
- Intended use: trusted operators — seed scripts, simulation runner, internal tooling — **not** end-user browser submit.
- **Product user submit** with `phone_verified` gate: browser `POST /story-drafts/{id}/submit` only (GW-DRAFT-02); superseded legacy GPT direct path per [story-draft-handoff](../../tasks/backlog-stories/story-draft-handoff/INDEX.md).

> **Risk:** compromise of `SERVICE_API_TOKEN` or re-exposing these routes as user-facing removes prior confused-deputy protection; scope tokens and keep routes non-public in production-like environments.

### 4.2) Identity canon sync (GW-DRAFT-03)

Identity runtime-docs (`04-security.md` §A, `09-gateway-expectations.md`) **временно рассинхронизированы** с as-built browser-submit на gateway. Канон identity правится в identity-репо: [STORY-IDS-DOC-DRAFT-05](../../../doge-identity-service/docs/tasks/backlog-stories/story-draft-handoff/STORY-IDS-DOC-DRAFT-05-browser-submit-security-canon-sync.md). Gateway не редактирует чужой SSOT (D-DRAFT-5).

### 5) Readiness and auth boundary semantics

- `GET /ready` всегда публичный и не требует service token.
- `GET /protected/status` и `GET /metrics` — единственные маршруты с обязательным service token.
- В `demo` profile при пустом `SERVICE_API_TOKEN` protected checks de-facto становятся permissive; в `pilot` конфиг не стартует без токена.

### 6) Test evidence

- `tests/test_api_security_and_ops.py`
  - проверяет Bearer/X-Service-Token extraction;
  - проверяет reject без токена при enabled auth;
  - проверяет allow в disabled режиме;
  - проверяет metrics/alert contract для auth failures.
- `tests/test_http_transport_smoke.py`
  - проверяет policy map (public/protected);
  - проверяет 401/200 поведение на реальном HTTP transport.
- `tests/test_error_envelope_contract.py`
  - проверяет маппинг `UnauthorizedError` -> `UNAUTHORIZED`.
- `tests/test_trace_propagation.py`
  - проверяет трассировку `trace_id` в error path.
- `tests/test_story_intake_contract.py`
  - проверяет обязательность `submitter.external_user_id`.
- `tests/test_story_repository_lifecycle.py`
  - проверяет сохранение `submitter_external_user_id` и `submitter_identity_issuer`.
- `tests/test_gw_draft_02_story_draft_submit_contract.py`
  - проверяет browser Bearer → `/me` gate, 202/403/401/503/404, idempotent submit.
- `tests/test_gw_draft_02_get_auth_contract.py`
  - проверяет GET read auth: 401/503/200; unverified session allowed on GET (no 403).

## Архитектурные последствия и ограничения

- Security baseline минималистичен и прозрачен: легко аудировать, но он intentionally narrow (service token gate only).
- Основная операционная опасность — неявный запуск в auth-disabled mode при незаданном `SERVICE_API_TOKEN`.
- Внутри текущего scope это приемлемо для demo-режима, но требует явного контроля в production-like окружениях.

## Strict Bearer runbook (current runtime)

1. Для `pilot` обязательно установить `SERVICE_API_TOKEN` (иначе startup config validation завершится ошибкой).
2. Для `demo` тоже установить `SERVICE_API_TOKEN`, если нужен строгий режим API gate.
3. Проверить, что protected вызовы несут `Authorization: Bearer ...` (или `X-Service-Token`):
   - `GET /protected/status`
   - `GET /metrics`
4. Выполнить контрольные тесты:
   - `python3 -m pytest tests/test_api_security_and_ops.py tests/test_http_transport_smoke.py tests/test_error_envelope_contract.py tests/test_trace_propagation.py tests/test_config_loading.py -q`
5. Оценить `auth_failures` через `ApiMetrics.alert_contract()` для сигнализации инцидентов.

## Planned target

- Полноценный server auth для business-operations API:
  - `ServiceTokenAuth.require()` применяется ко всем защищаемым handler/route операциям, а не только к `handle_protected_status`.
  - Policy по умолчанию для production-like профиля: fail-fast startup при пустом/отсутствующем `SERVICE_API_TOKEN`.
  - Единый список публичных vs защищённых операций фиксируется в runtime docs + tests.
- Ввести формальную policy документацию по key lifecycle:
  - ротация, TTL, revoke, emergency replace.
- Добавить интеграцию с внешним secret manager (если выйдем за рамки single token модели).
- При необходимости расширить модель до keyset/multi-token с audit metadata.

## Gaps / risks

- В `demo` профиль всё ещё может работать в auth-disabled режиме при пустом `SERVICE_API_TOKEN`; это допустимо для демо, но рискованно без операционного контроля.
- Бизнес-эндпоинт (`POST /intake/stories`) публичен — это осознанное решение для текущей фазы, но в production-like окружении может потребоваться auth gate.
- Отсутствует отдельный формализованный документ по ротации и аудит-требованиям для сервисных ключей.
- Нет transport-level rate limiting/WAF логики в текущем `src/core` scope.

## Контрольные проверки

- Конфиг валидность: `python3 -m pytest tests/test_config_loading.py -q`
- Security baseline: `python3 -m pytest tests/test_api_security_and_ops.py -q`
