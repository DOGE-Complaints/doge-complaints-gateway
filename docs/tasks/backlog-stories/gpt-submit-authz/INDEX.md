# GPT story-submit: авторизация и гейт верификации (gateway-сторона) · index

**Зона:** `doge-complaints-gateway/docs/tasks/backlog-stories/gpt-submit-authz/`
**Тип:** backlog — углублён до build-стандарта (verified-state + подзадачи T01–T05); enforcement «как делать» детализируется в фокусном gateway-диалоге.
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc) — факты по фактическому коду, пути указаны.
**Решения интервью (2026-06-24):** [`interview-gpt-submit-authz-2026-06-24.md`](./interview-gpt-submit-authz-2026-06-24.md) (D-GAUTH-1..4).

## ⚠️ Superseded — user story submit path (D-DRAFT-5, GW-DRAFT-03)

**Актуальная модель подачи истории пользователем:** browser-submit через [`story-draft-handoff/`](../story-draft-handoff/INDEX.md) — GPT стешит черновик (`POST /story-drafts`, service-auth only) → браузер сабмитит (`POST /story-drafts/{id}/submit`, Bearer → identity `/me` + `phone_verified` gate). См. [GW-DRAFT-02](../story-draft-handoff/STORY-GW-DRAFT-02-browser-submit-verification-gate.md).

| Часть пакета | Статус | Примечание |
|--------------|--------|------------|
| **GW-GAUTH-01** (два токена на submit: service + `X-User-Token`) | **Superseded** для user submit | OAuth user path удалён GW-DRAFT-04; legacy `POST /intake/stories` → [GW-DRAFT-06](../story-draft-handoff/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md) |
| **GW-GAUTH-02** (OAuth introspection токена GPT на submit) | **Superseded** для user submit | Заменено `IdentityMeClient` + `/me` на browser path (GW-DRAFT-02) |
| **GW-GAUTH-03** (`verification_required` / 403 gate) | **Still valid — reused** | `evaluate_verification_gate` на browser submit ([GW-DRAFT-02](../story-draft-handoff/STORY-GW-DRAFT-02-browser-submit-verification-gate.md)) |
| **GW-GAUTH-04** (авторитетный автор = `sub`) | **Still valid — reused** | `authoritative_submitter_from_introspection` на browser submit ([GW-DRAFT-02](../story-draft-handoff/STORY-GW-DRAFT-02-browser-submit-verification-gate.md)) |

**История сохранена (D-DRAFT-6):** pipeline stories EPIC-M2-20, pkg-000039..042, аудиты `docs/analysis/audit-gw-gauth-*` — **не удалять**.

**Identity canon** (`04-security.md` §A, `09-gateway-expectations.md`) пока описывает старый GPT-direct path — рассинхрон; задача на синхронизацию: [STORY-IDS-DOC-DRAFT-05](../../../../../doge-identity-service/docs/tasks/backlog-stories/story-draft-handoff/STORY-IDS-DOC-DRAFT-05-browser-submit-security-canon-sync.md).

## ✅ Разблокировано: identity-сторона построена (2026-06-24)
Ранее e2e упирался в identity (introspection/OAuth = 501). **Теперь по коду:** `POST /oauth/introspect` построен ([`identity asgi_app.py:407`](../../../../../doge-identity-service/src/core/api/asgi_app.py#L407)), защищён сервисным токеном, отдаёт `{active, sub, phone_verified}` ([`introspection.py:28-32`](../../../../../doge-identity-service/src/core/oauth/introspection.py#L28)); `/oauth/authorize`, `/oauth/token`, `/me` тоже построены. → gateway-сторона **реализуема end-to-end**.

## Источник процесса (SSOT) — historical + identity canon (partially stale)
Каноничный сквозной флоу «подача истории из GPT» **исторически** описан в identity: [`04-security.md` §A](../../../../../doge-identity-service/docs/runtime-docs/04-security.md) и [`09-gateway-expectations.md`](../../../../../doge-identity-service/docs/runtime-docs/09-gateway-expectations.md). **User submit superseded** — см. [`story-draft-handoff/`](../story-draft-handoff/INDEX.md). Ниже — **исторический** контекст пакета GAUTH (шаги 6–8 GPT-direct); pkg/аудиты сохранены для traceability.

## Контекст одной фразой (historical — GPT two-token direct submit)
~~По целевой модели GPT шлёт историю **напрямую в gateway** с двумя токенами~~ — **superseded for user submit** by browser handoff ([story-draft-handoff](../story-draft-handoff/INDEX.md)). Исторически: gateway проверял два слоя (service + user introspection) на `POST /intake/stories`; GAUTH-03/04 переиспользуются на browser path.

## Текущее состояние (verified по коду gateway, 2026-07-10)

- **Продуктовый GPT path:** `POST /story-drafts` (service auth) → `POST /story-drafts/{id}/submit` (browser Bearer → identity `/me`) — [`asgi_app.py:521-552`](../../../../src/core/api/asgi_app.py).
- **Reused modules:** `evaluate_verification_gate` ([`verification_gate.py`](../../../../src/core/identity/verification_gate.py)), `authoritative_submitter_from_introspection` ([`authoritative_submitter.py`](../../../../src/core/identity/authoritative_submitter.py)), `IdentityMeClient` ([`me_client.py`](../../../../src/core/identity/me_client.py)).
- **Удалено GW-DRAFT-04:** `require_user_token`, `IdentityIntrospectionClient`, `IDENTITY_INTROSPECT_*` — grep **0** в `src/`.
- **Legacy:** `POST /intake/stories` ([`:501`](../../../../src/core/api/asgi_app.py)) — не целевой путь; removal → [GW-DRAFT-06](../story-draft-handoff/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md).
- **Deploy:** [`railpack.json`](../../../../railpack.json) (не backlog story; см. [retire-STORY-GW-DEPLOY-01](../../analysis/retire-STORY-GW-DEPLOY-01-2026-07-10.md)).

## Исторический контекст (pre browser-submit, до GW-DRAFT-04)

~~Прямой GPT submit через `/intake/stories` + OAuth introspection~~ — superseded. Ниже D-GAUTH и interview отражают исходный GPT-direct дизайн; pkg/аудиты сохранены.

## Решения интервью (D-GAUTH, 2026-06-24) — кратко
| D | Решение | Где применено |
|---|---------|---------------|
| **D-GAUTH-1** | Углубить до полного build-стандарта (verified-state + T01–T05) — identity готов, реализация не преждевременна | все 4 стори |
| **D-GAUTH-2** | Двухслойная auth — на **все мутации публичного контента**, не только `/intake/stories` | [GAUTH-01](./STORY-GW-GAUTH-01-two-layer-auth-on-submit.md) |
| **D-GAUTH-3** | Источник статуса — **реальный `/oauth/introspect`** identity (`{active,sub,phone_verified}`, form `token=`, сервисный токен), не `/me` | [GAUTH-02](./STORY-GW-GAUTH-02-user-token-introspection.md) |
| **D-GAUTH-4** | Identity недоступен/невалиден → **fail-closed** (история не создаётся; без degraded, без payload-fallback) | [GAUTH-02](./STORY-GW-GAUTH-02-user-token-introspection.md)/[03](./STORY-GW-GAUTH-03-verification-gate-403.md)/[04](./STORY-GW-GAUTH-04-authoritative-author-from-introspection.md) |

## Коды статусов (S)
⚪ Todo · 🟡 In Progress · 🔵 Implemented (Waiting Acceptance) · 🟢 Done

## Стори пакета

| Order | Story | Status | Depends |
|-------|-------|--------|---------|
| — | [GW-GAUTH-01 — Двухслойная auth на submit](./STORY-GW-GAUTH-01-two-layer-auth-on-submit.md) | Superseded | — |
| — | [GW-GAUTH-02 — User token introspection](./STORY-GW-GAUTH-02-user-token-introspection.md) | Superseded | GAUTH-01 |
| 1 | [GW-GAUTH-03 — Verification gate 403](./STORY-GW-GAUTH-03-verification-gate-403.md) | Done | — |
| 2 | [GW-GAUTH-04 — Authoritative author from introspection](./STORY-GW-GAUTH-04-authoritative-author-from-introspection.md) | Done | GAUTH-03 |

**Progress:** 2/2 active Done (100%); GAUTH-01/02 Superseded (excluded from denominator)

## Граница пакета
- ✅ Описываем gateway-сторону: verified-state + подзадачи T01–T05 (черновик) + AC; точное enforcement дорабатывается в фокусном gateway-диалоге.
- ❌ Не дублируем identity: OAuth-сервер, выдача токена, introspection-endpoint, verify-флоу телефона — на стороне identity ([OAUTH-02](../../../../../doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md) ✅ построен, [OAUTH-04](../../../../../doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md)). Gateway лишь **вызывает** их и переиспользует канон `verification_required`.
- ❌ Не дублируем inbound-контракт submitter/препроцессинг — [`req-19`](../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md) (GW-GAUTH-04 лишь уточняет, кто авторитетный автор).

## Зависимость от identity (статус: ✅ готово)
Требования предполагают готовые **identity**-эндпоинты: OAuth-токен ([OAUTH-01](../../../../../doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md)) и introspection ([OAUTH-02](../../../../../doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md)) — **построены по коду** (`/oauth/authorize|token|introspect`, [`identity asgi_app.py:368-417`](../../../../../doge-identity-service/src/core/api/asgi_app.py#L368)). Канон `verification_required` фиксирует [OAUTH-04](../../../../../doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md). → gateway-сторона реализуема end-to-end; остаётся согласовать сервисный токен gateway→identity и имя заголовка пользовательского токена.
