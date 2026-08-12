# STORY-GW-GAUTH-02 — Introspection пользовательского токена у identity

> **⚠️ Superseded (user submit):** browser path использует `IdentityMeClient` + `/me` ([GW-DRAFT-02](../story-draft-handoff/STORY-GW-DRAFT-02-browser-submit-verification-gate.md)). OAuth introspection на submit остаётся на legacy `POST /intake/stories`. См. [`gpt-submit-authz/INDEX.md`](./INDEX.md).

## Meta
- **Key:** `STORY-GW-GAUTH-02`
- **Status:** 🔵 Done (Awaiting Commits) — pipeline ([pkg-000040](../../gateway-active-packages/pkg-000040-20260625-gw-gauth-02-user-token-introspection.yaml), T01–T06, gate PASS 2026-06-25): `identity/introspection_client.py` + `IDENTITY_*` EnvSpec; `require_user_token` зовёт `/oauth/introspect`, fail-closed; 8 contract + 541 unit. Код-аудит [`audit-gw-gauth-02-...`](../../../analysis/audit-gw-gauth-02-user-token-introspection-2026-06-25.md). **G1:** enforce только `active`; `phone_verified` сохранён в `request.state` → verify-гейт в GAUTH-03. **CF-1:** hosted-seed теперь fail-closed без `IDENTITY_*`+реального user-токена. SSOT исполнения — pipeline-копия.
- **Приоритет:** P1
- **Тип:** implement (gateway↔identity клиент)
- **Закрывает:** отсутствие пользовательского слоя на intake (gateway не зовёт identity)
- **Источник процесса:** [`04-security §A`](../../../../../doge-identity-service/docs/runtime-docs/04-security.md) шаг 7; [`09-gateway-expectations §Модель аутентификации`](../../../../../doge-identity-service/docs/runtime-docs/09-gateway-expectations.md).
- **Основание:** [`interview-gpt-submit-authz-2026-06-24`](./interview-gpt-submit-authz-2026-06-24.md) (D-GAUTH-3, D-GAUTH-4)
- **Зависит от:** [GW-GAUTH-01](./STORY-GW-GAUTH-01-two-layer-auth-on-submit.md)
- **Разблокирует:** [GW-GAUTH-03](./STORY-GW-GAUTH-03-verification-gate-403.md), [GW-GAUTH-04](./STORY-GW-GAUTH-04-authoritative-author-from-introspection.md)

## Зачем простыми словами
Чтобы решить, можно ли создать историю, gateway должен знать: жив ли пользовательский токен и **пройдена ли верификация** (`phone_verified`). По решению статус **не зашит в токен** — gateway каждый раз спрашивает identity и получает свежий ответ. Так статус нельзя «заморозить» в старом токене.

## Что наблюдаю сейчас (verified по коду)
- **Gateway:** introspection-клиента нет; **ни одного env** `IDENTITY_*`/`INTROSPECT_*` в [`config/schema.py`](../../../../src/core/config/schema.py); `phone_verified` нигде не читается.
- **Identity — endpoint ПОСТРОЕН (2026-06-24):** `POST /oauth/introspect` ([`asgi_app.py:407`](../../../../../doge-identity-service/src/core/api/asgi_app.py#L407)), защищён `require_service_token` (вход без сервисного токена → 401/403).
- **Контракт identity (RFC 7662, всегда HTTP 200)** ([`oauth/introspection.py:14-32`](../../../../../doge-identity-service/src/core/oauth/introspection.py#L14)):
  - вход: form-поле `token=<пользовательский access-токен>`;
  - активный → `{"active": true, "sub": <id>, "phone_verified": <bool>}`;
  - битый/пустой/просроченный → `{"active": false}`.
  - `phone_verified` берётся из профиля по `claims.sub` — **не из тела токена** ([`introspection.py:24-27`](../../../../../doge-identity-service/src/core/oauth/introspection.py#L24)).

## Требование / целевое состояние
- На verify-гейтед мутации gateway берёт **пользовательский** токен и вызывает identity `POST /oauth/introspect` (form `token=…`), получая `{ active, sub, phone_verified }` — **D-GAUTH-3** (анкер — реально построенный endpoint, не `/me`).
- Gateway аутентифицируется **перед** identity своим **сервисным токеном** (требование identity-входа `require_service_token`).
- Статус берётся **свежим у identity** на каждый такой запрос; не извлекается из тела токена.
- Ответ identity — единственный источник истины о пользователе для решения доступа.
- **Fail-closed (D-GAUTH-4):** identity недоступен / ответ невалиден / `active=false` → **безопасный отказ** (НЕ считать пользователя верифицированным; историю не создавать). Без degraded-режима и без fallback на payload-submitter.

## Граница и контракт
- Сам introspection-endpoint и его контракт — на стороне **identity** ([OAUTH-02](../../../../../doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md), **построен**); здесь — требование gateway **вызывать** его и доверять ответу.
- Решение «создавать/отказать» по статусу — [GW-GAUTH-03](./STORY-GW-GAUTH-03-verification-gate-403.md); авторство по `sub` — [GW-GAUTH-04](./STORY-GW-GAUTH-04-authoritative-author-from-introspection.md).

## Подзадачи (черновик)
- **T01** — Конфиг: добавить EnvSpec в [`config/schema.py`](../../../../src/core/config/schema.py) — `IDENTITY_INTROSPECT_URL` (база identity) + `IDENTITY_SERVICE_TOKEN` (сервисный токен gateway→identity). По образцу существующих EnvSpec-записей.
- **T02** — Introspection-клиент: `POST {IDENTITY_INTROSPECT_URL}/oauth/introspect`, form `token=<user>`, заголовок сервисного токена identity; парсинг `{active, sub, phone_verified}`. Тайм-аут + единый путь ошибки.
- **T03** — Извлечение пользовательского токена из входящего запроса: заголовок **`X-User-Token`** (verified в GAUTH-01 — [`security.py:16-19`](../../../../src/core/api/security.py#L16); audit G2 [`audit-gw-gauth-01-...`](../../../analysis/audit-gw-gauth-01-two-layer-auth-on-submit-2026-06-25.md) §3 G2). Сервисный слой отдельно: `Authorization: Bearer` / `X-Service-Token`.
- **T04** — **Fail-closed**: timeout/5xx/`active=false`/невалидный JSON → `verified=false`, история не создаётся (передаётся в GAUTH-03 как «отказ»).
- **T05** — Тесты: активный+verified → проброс `{sub, phone_verified}`; `active=false` → отказ; identity down (timeout) → отказ (fail-closed); статус НЕ берётся из тела токена.

## Acceptance Criteria
- [ ] Для verify-гейтед действия gateway получает от identity свежий `{ active, sub, phone_verified }` по пользовательскому токену через `POST /oauth/introspect`.
- [ ] Gateway предъявляет identity свой сервисный токен (иначе identity отвечает 401/403).
- [ ] Статус не берётся из тела токена.
- [ ] Identity недоступен/ответ невалиден/`active=false` → **безопасный отказ** (fail-closed, D-GAUTH-4).
- [ ] Контракт ответа соответствует построенному identity ([`introspection.py`](../../../../../doge-identity-service/src/core/oauth/introspection.py)).

## Открытые вопросы
- Кэшировать ли результат introspection в пределах одного запроса (без «заморозки» статуса) — перф-решение на этапе реализации.
- ~~Имя заголовка пользовательского токена на входе gateway~~ → **решено GAUTH-01:** `X-User-Token` ([`security.py:16-19`](../../../../src/core/api/security.py#L16)); согласовать с GPT-Action конфигом при деплое.
- **Doc prerequisite (audit G3):** перед/вместе с P3 обновить seed manuals — [`TASK-GW-GAUTH-01-T06`](../../epics/EPIC-M2-20-gpt-submit-authz/stories/STORY-GW-GAUTH-01-two-layer-auth-on-submit/task-gw-gauth-01-t06-audit-g3-seed-docs-user-token/README.md) (`run_mode=gw_gauth_01_audit_g3_followup`) или в рамках GAUTH-02 P3.
