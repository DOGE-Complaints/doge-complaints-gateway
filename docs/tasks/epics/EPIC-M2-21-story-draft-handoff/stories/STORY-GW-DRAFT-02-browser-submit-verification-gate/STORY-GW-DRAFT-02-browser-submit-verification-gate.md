# STORY-GW-DRAFT-02 — Браузер-сабмит истории + гейт phone_verified

## Meta
- **Key:** `STORY-GW-DRAFT-02`
- **Parent Epic:** [`../../../EPIC-M2-21-story-draft-handoff.md`](../../../EPIC-M2-21-story-draft-handoff.md)
- **Type:** implement (identity-`/me`-клиент + submit-роут + гейт)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🔴 HIGH (замыкает M-3/M-7 на gateway)
- **source:** [`../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-02-browser-submit-verification-gate.md`](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-02-browser-submit-verification-gate.md)
- **Decision Ref:** backlog file above; [`interview-story-draft-handoff-2026-07-03`](../../../../backlog-stories/story-draft-handoff/interview-story-draft-handoff-2026-07-03.md) (**D-DRAFT-1, D-DRAFT-3**); [`mvp-integration-plan-2026-07-02 §2,§4`](../../../../../../../doge-identity-service/docs/analysis/mvp-integration-plan-2026-07-02.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000044-20260703-gw-draft-02-browser-submit-verification-gate.yaml`](../../../../gateway-active-packages/pkg-000044-20260703-gw-draft-02-browser-submit-verification-gate.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **7** тасков T01–T07
- **Зависит от:** [GW-DRAFT-01](../STORY-GW-DRAFT-01-story-draft-stash/STORY-GW-DRAFT-01-story-draft-stash.md)
- **Разблокирует:** [GW-DRAFT-03](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon.md)

## Зачем простыми словами
Теперь историю публикует **браузер**, а не GPT. У браузера есть Supabase-сессия юзера (после логина+phone-verify). Gateway должен: принять сабмит от браузера по `draft_id`, убедиться что телефон подтверждён, и создать историю **от имени этого верифицированного человека**.

## Что наблюдаю сейчас (verified по коду)
- **gateway Supabase-JWT НЕ валидирует:** grep `SupabaseJwt/jwks/joserfc` в `src/` = 0. Supabase-конфиг только для БД ([schema.py:161-167](../../../../../../src/core/config/schema.py#L161)).
- **identity `/me`** (D-DRAFT-1 якорь): защищён `get_current_user` (валидирует **Supabase Bearer**), отдаёт `{sub, phone_verified}` ([me_response.py:42-45](../../../../../../../../doge-identity-service/src/core/api/me_response.py#L42), [asgi_app.py:299](../../../../../../../../doge-identity-service/src/core/api/asgi_app.py#L299)).
- **Переиспользуемое из gpt-submit-authz** (verified, см. [interview §Инвентарь](../../../../backlog-stories/story-draft-handoff/interview-story-draft-handoff-2026-07-03.md)):
  - `IntrospectionResult` (`{active, sub, phone_verified}`) — общий value-object ([introspection_client.py:16-19](../../../../../../src/core/identity/introspection_client.py#L16)).
  - `evaluate_verification_gate(result)` → ALLOW / VERIFICATION_REQUIRED / UNAUTHORIZED ([verification_gate.py:19-25](../../../../../../src/core/identity/verification_gate.py#L19)).
  - `VerificationRequiredError` + `build_verify_url` → **403** `verification_required` + `verify_url` ([envelope.py:93-99](../../../../../../src/core/api/envelope.py#L93), [verify_url.py](../../../../../../src/core/identity/verify_url.py)).
  - `authoritative_submitter_from_introspection` → автор = `sub` ([authoritative_submitter.py](../../../../../../src/core/identity/authoritative_submitter.py), GAUTH-04).
  - `StoryIntakeService.create_story(request, *, idempotency_key)` → `StoryIntakeResult` ([services.py:147](../../../../../../src/core/application/services.py#L147)) + `IdempotencyRepository`.
- **HTTP-клиент-образец:** [`introspection_client.py`](../../../../../../src/core/identity/introspection_client.py) (httpx, timeout, fail-closed).
- **Нет `POST /story-drafts/{id}/submit`:** [`asgi_app.py`](../../../../../../src/core/api/asgi_app.py) — только POST/GET stash; `require_story_draft_user_auth` — stub ([asgi_app.py:343-345](../../../../../../src/core/api/asgi_app.py#L343)).

## Требование / целевое состояние (D-DRAFT-1, D-DRAFT-3)
- **A. Роут `POST /story-drafts/{draft_id}/submit`** (D-DRAFT-3): вход — `draft_id` (из GW-DRAFT-01) + браузерная user-auth (Supabase Bearer).
- **B. Проверка юзера через identity `/me`** (D-DRAFT-1): новый мелкий **`/me`-клиент** в gateway (образец `introspection_client.py`) + env `IDENTITY_BASE_URL`; форвардит Supabase-Bearer → `{sub, phone_verified}`, **маппит в `IntrospectionResult`** (реюз гейта/автор-резолвера). НЕ локальная JWT-валидация.
- **C. Гейт** (реюз `evaluate_verification_gate`): `phone_verified=true` → взять черновик по `draft_id`, создать историю через `StoryIntakeService.create_story`, `submitter = sub` (реюз `authoritative_submitter_from_introspection`). `phone_verified=false` → **403 `verification_required`** + `verify_url`. `active=false`/нет токена → **401**.
- **D. Fail-closed** (D-GAUTH-4): identity недоступен/ответ невалиден → **503**, история не создаётся.
- **E. Идемпотентность:** повторный submit того же `draft_id` не плодит дубли (реюз `IdempotencyRepository`; ключ ← `draft_id`).
- **F. `draft_id` unknown/expired → 404** (из GW-DRAFT-01 store).

## Out of scope
- GW-DRAFT-03/04 (supersede/removal GAUTH)
- Локальная JWT-валидация в gateway
- SPA/GPT client changes (links only)

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-draft-02-t01-identity-me-client-and-config`](./task-gw-draft-02-t01-identity-me-client-and-config/README.md) | pkg-000044 |
| 2 | [`task-gw-draft-02-t02-post-story-drafts-submit-route`](./task-gw-draft-02-t02-post-story-drafts-submit-route/README.md) | pkg-000044 |
| 3 | [`task-gw-draft-02-t03-verification-gate-and-intake-submit`](./task-gw-draft-02-t03-verification-gate-and-intake-submit/README.md) | pkg-000044 |
| 4 | [`task-gw-draft-02-t04-draft-submit-idempotency-and-cleanup`](./task-gw-draft-02-t04-draft-submit-idempotency-and-cleanup/README.md) | pkg-000044 |
| 5 | [`task-gw-draft-02-t05-story-draft-submit-contract-tests`](./task-gw-draft-02-t05-story-draft-submit-contract-tests/README.md) | pkg-000044 |
| 6 | [`task-gw-draft-02-t06-runtime-docs-submit-api`](./task-gw-draft-02-t06-runtime-docs-submit-api/README.md) | pkg-000044 |
| 7 | [`task-gw-draft-02-t07-story-acceptance-gate`](./task-gw-draft-02-t07-story-acceptance-gate/README.md) | pkg-000044 |

## Audit follow-up (G1 — GET user-auth)

Post-audit P5 2026-07-03. **Не** в pkg-000044. Исполнение: `run_mode=gw_draft_02_audit_followup` ([`Gateway_builder.plan.md`](../../../../../../../.cursor/plans/Gateway_builder.plan.md)).

| Order | Task folder | Wave |
|-------|-------------|------|
| 8 | [`task-gw-draft-02-t08-get-story-draft-read-user-auth`](./task-gw-draft-02-t08-get-story-draft-read-user-auth/README.md) | audit override |
| 9 | [`task-gw-draft-02-t09-get-story-draft-auth-contract-tests`](./task-gw-draft-02-t09-get-story-draft-auth-contract-tests/README.md) | audit override |
| 10 | [`task-gw-draft-02-t10-runtime-docs-get-user-auth`](./task-gw-draft-02-t10-runtime-docs-get-user-auth/README.md) | audit override |

**Audit ref:** [`audit-gw-draft-02-browser-submit-verification-gate-2026-07-03`](../../../../../../analysis/audit-gw-draft-02-browser-submit-verification-gate-2026-07-03.md) §G1 — **Done** 2026-07-03 (`run_mode=gw_draft_02_audit_followup`). **G2** (dep consolidation) → [GW-DRAFT-04](../../../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md), `activation: none`.

## Acceptance Criteria
- [x] Браузер с валидной Supabase-сессией + `phone_verified=true` → история создаётся, `submitter=sub`, **202** (как `/intake/stories`).
- [x] `phone_verified=false` → **403 `verification_required`** + `verify_url` (реюз канона).
- [x] Нет/битый юзер-токен → **401**; identity недоступен → **503** (fail-closed), история не создаётся.
- [x] Повторный submit `draft_id` идемпотентен (нет дублей).
- [x] `draft_id` неизвестен/протух → **404**.
- [x] Проверка юзера идёт через identity `/me` (D-DRAFT-1), gateway Supabase-JWT сам не валидирует.

## Runtime-docs дельта
- [`openapi.yaml`](../../../../../runtime-docs/api-reference/openapi.yaml) + [`API_REFERENCE.md`](../../../../../runtime-docs/api-reference/API_REFERENCE.md) — `POST /story-drafts/{id}/submit` (коды 202/403/401/503/404).
- [`security-env-api-access.md`](../../../../../runtime-docs/security-env-api-access.md) — `IDENTITY_BASE_URL` + браузерный auth-путь.

## Открытые под-вопросы (реализация)
- `IDENTITY_BASE_URL` отдельным env или реюз базы из `IDENTITY_INTROSPECT_URL`.
- Обобщить `evaluate_verification_gate`/автор-резолвер под нейтральный `IntrospectionResult` (сейчас импорт из `introspection_client`) — согласовать с рефактором в [GW-DRAFT-04](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md).
- **P1 decision:** `/me` client maps `supabase_user_id` → `IntrospectionResult.sub` (identity unchanged this wave).

## Швы
Роут/гейт — [`asgi_app.py`](../../../../../../src/core/api/asgi_app.py); `/me`-клиент — новый (образец [`introspection_client.py`](../../../../../../src/core/identity/introspection_client.py)); гейт — [`verification_gate.py`](../../../../../../src/core/identity/verification_gate.py); автор — [`authoritative_submitter.py`](../../../../../../src/core/identity/authoritative_submitter.py); intake — [`services.py`](../../../../../../src/core/application/services.py).

## Зависимости / связь
Клиент: [SPA-ID-12](../../../../../../../spa-app/docs/tasks/backlog-stories/identity-auth/STORY-SPA-ID-12-story-draft-handoff-submit.md). Канон-пересмотр: [GW-DRAFT-03](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon.md). Закрывает часть **M-7** (spa сабмитит на реальный роут).
