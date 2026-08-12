# STORY-GW-DRAFT-02 — Браузер-сабмит истории + гейт phone_verified

## Meta
- **Key:** `STORY-GW-DRAFT-02-browser-submit-verification-gate`
- **Пакет:** [`story-draft-handoff/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🔴 HIGH (замыкает M-3/M-7 на gateway)
- **Тип:** implement (identity-`/me`-клиент + submit-роут + гейт)
- **Основание:** [`interview-story-draft-handoff-2026-07-03`](./interview-story-draft-handoff-2026-07-03.md) (**D-DRAFT-1, D-DRAFT-3**); [`mvp-integration-plan-2026-07-02 §2,§4`](../../../../../doge-identity-service/docs/analysis/mvp-integration-plan-2026-07-02.md)
- **Зависит от:** [GW-DRAFT-01](./STORY-GW-DRAFT-01-story-draft-stash.md)

## Зачем простыми словами
Теперь историю публикует **браузер**, а не GPT. У браузера есть Supabase-сессия юзера (после логина+phone-verify). Gateway должен: принять сабмит от браузера по `draft_id`, убедиться что телефон подтверждён, и создать историю **от имени этого верифицированного человека**.

## Что наблюдаю сейчас (verified по коду)
- **gateway Supabase-JWT НЕ валидирует:** grep `SupabaseJwt/jwks/joserfc` в `src/` = 0. Supabase-конфиг только для БД ([schema.py:161-167](../../../../src/core/config/schema.py#L161)).
- **identity `/me`** (D-DRAFT-1 якорь): защищён `get_current_user` (валидирует **Supabase Bearer**), отдаёт `{sub, phone_verified}` ([me_response.py:42-45](../../../../../doge-identity-service/src/core/api/me_response.py#L42), [asgi_app.py:299](../../../../../doge-identity-service/src/core/api/asgi_app.py#L299)).
- **Переиспользуемое из gpt-submit-authz** (verified, см. [interview §Инвентарь](./interview-story-draft-handoff-2026-07-03.md)):
  - `IntrospectionResult` (`{active, sub, phone_verified}`) — [`introspection_result.py`](../../../../src/core/identity/introspection_result.py).
  - `evaluate_verification_gate(result)` → ALLOW / VERIFICATION_REQUIRED / UNAUTHORIZED ([`verification_gate.py:19-25`](../../../../src/core/identity/verification_gate.py#L19)).
  - `VerificationRequiredError` + `build_verify_url` → **403** `verification_required` + `verify_url` ([`envelope.py:93-99`](../../../../src/core/api/envelope.py#L93), [`verify_url.py`](../../../../src/core/identity/verify_url.py)).
  - `authoritative_submitter_from_introspection` → автор = `sub` ([`authoritative_submitter.py`](../../../../src/core/identity/authoritative_submitter.py), GAUTH-04).
  - `StoryIntakeService.create_story(request, *, idempotency_key)` → `StoryIntakeResult` ([`services.py:147`](../../../../src/core/application/services.py#L147)) + `IdempotencyRepository`.
- **HTTP-клиент:** [`me_client.py`](../../../../src/core/identity/me_client.py) — identity `/me` forward (D-DRAFT-1); OAuth introspection client **удалён** GW-DRAFT-04.

## Требование / целевое состояние (D-DRAFT-1, D-DRAFT-3)
- **A. Роут `POST /story-drafts/{draft_id}/submit`** (D-DRAFT-3): вход — `draft_id` (из GW-DRAFT-01) + браузерная user-auth (Supabase Bearer).
- **B. Проверка юзера через identity `/me`** (D-DRAFT-1): [`me_client.py`](../../../../src/core/identity/me_client.py) + env `IDENTITY_BASE_URL`; форвардит Supabase-Bearer → `{sub, phone_verified}`, **маппит в `IntrospectionResult`**. НЕ локальная JWT-валидация.
- **C. Гейт** (реюз `evaluate_verification_gate`): `phone_verified=true` → взять черновик по `draft_id`, создать историю через `StoryIntakeService.create_story`, `submitter = sub` (реюз `authoritative_submitter_from_introspection`). `phone_verified=false` → **403 `verification_required`** + `verify_url`. `active=false`/нет токена → **401**.
- **D. Fail-closed** (D-GAUTH-4): identity недоступен/ответ невалиден → **503**, история не создаётся.
- **E. Идемпотентность:** повторный submit того же `draft_id` не плодит дубли (реюз `IdempotencyRepository`; ключ ← `draft_id`).
- **F. `draft_id` unknown/expired → 404** (из GW-DRAFT-01 store).

> **Security model — story drafts (MVP).** Доступ = capability: `draft_id` — неугадываемый 128-битный токен (`secrets.token_urlsafe(16)`). Валидный user-Bearer + знание `draft_id` = право на чтение и сабмит; отдельная проверка владельца на GET/submit **не выполняется by design**. Ассоциация `draft_owner` на успешном GET — **first-wins** (`set_owner`: INSERT … DO NOTHING / ignore-duplicates / setdefault); `GET /story-drafts/current` scoped по первому записанному владельцу. Модель достаточна, пока `draft_id` не утекает (логи, реферер, пересланные ссылки). Strict ownership-gate — post-MVP, вне скоупа.
>
> SSOT: [DOC-TASK-DRAFT-OWNERSHIP-01](../cabinet-api/DOC-TASK-DRAFT-OWNERSHIP-01-clarify-capability-model.md).

## Подзадачи (черновик)
- **T01** — Конфиг+клиент: EnvSpec `IDENTITY_BASE_URL` в [`schema.py`](../../../../src/core/config/schema.py); `identity/me_client.py` (`GET {IDENTITY_BASE_URL}/me` с Bearer форвардом; парсинг `{sub, phone_verified}` → `IntrospectionResult(active=True,…)`; timeout; ошибки → fail-closed).
- **T02** — Роут `POST /story-drafts/{draft_id}/submit` в [`asgi_app.py`](../../../../src/core/api/asgi_app.py): извлечь Supabase-Bearer, вызвать `/me`-клиент, достать черновик (GW-DRAFT-01 store).
- **T03** — Гейт: реюз `evaluate_verification_gate` → 202 (создать историю, автор=`sub`) / 403 `verification_required` / 401 / 503; при отказе история **не** создаётся.
- **T04** — Идемпотентность по `draft_id` + удаление/пометка черновика после успешного submit (не переиспользовать протухший).
- **T05** — Контракт-тесты (unit): verified→202+`submitter=sub`; `phone_verified=false`→403+`verify_url`; нет/битый токен→401; identity down→503; повтор `draft_id`→идемпотентно; unknown draft→404. + story gate.

## Acceptance Criteria
- [x] Браузер с валидной Supabase-сессией + `phone_verified=true` → история создаётся, `submitter=sub`, **202** (как `/intake/stories`).
- [x] `phone_verified=false` → **403 `verification_required`** + `verify_url` (реюз канона).
- [x] Нет/битый юзер-токен → **401**; identity недоступен → **503** (fail-closed), история не создаётся.
- [x] Повторный submit `draft_id` идемпотентен (нет дублей).
- [x] `draft_id` неизвестен/протух → **404**.
- [x] Проверка юзера идёт через identity `/me` (D-DRAFT-1), gateway Supabase-JWT сам не валидирует.

## Runtime-docs дельта
- [`openapi.yaml`](../../../runtime-docs/api-reference/openapi.yaml) + [`API_REFERENCE.md`](../../../runtime-docs/api-reference/API_REFERENCE.md) — `POST /story-drafts/{id}/submit` (коды 202/403/401/503/404).
- [`security-env-api-access.md`](../../../runtime-docs/security-env-api-access.md) — `IDENTITY_BASE_URL` + браузерный auth-путь.

## Открытые под-вопросы (реализация)

- ~~`IDENTITY_BASE_URL` отдельным env~~ — **resolved:** `IDENTITY_BASE_URL` в [`schema.py`](../../../../src/core/config/schema.py).
- ~~Обобщить под `IntrospectionResult`~~ — **Done** GW-DRAFT-04: [`introspection_result.py`](../../../../src/core/identity/introspection_result.py).

## Швы
Роут/гейт — [`asgi_app.py`](../../../../src/core/api/asgi_app.py); `/me`-клиент — [`me_client.py`](../../../../src/core/identity/me_client.py); гейт — [`verification_gate.py`](../../../../src/core/identity/verification_gate.py); автор — [`authoritative_submitter.py`](../../../../src/core/identity/authoritative_submitter.py); intake — [`services.py`](../../../../src/core/application/services.py).

## Зависимости / связь
Клиент: [SPA-ID-12](../../../../../spa-app/docs/tasks/backlog-stories/identity-auth/STORY-SPA-ID-12-story-draft-handoff-submit.md). Канон-пересмотр: [GW-DRAFT-03](./STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon.md). Закрывает часть **M-7** (spa сабмитит на реальный роут).
