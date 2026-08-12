# Интервью CPO/CTO — gateway-сторона авторизации GPT-сабмита (gpt-submit-authz) → решения

**Дата:** 2026-06-24
**Метод:** `.cursor/rules/analysis.mdc` — решения поверх verified-фактов (gateway + identity).
**Итог:** углубление 4 стори пакета [`gpt-submit-authz`](./INDEX.md) до стандарта build-беклога (verified-state + подзадачи T01–T05 + AC).

## Verified-факты перед решениями

### Gateway (as-is, по коду)
- `POST /intake/stories` ([`asgi_app.py:396`](../../../../src/core/api/asgi_app.py#L396)) — **без auth-зависимости** (открыт); `POST /tallinn/issues` ([`:380`](../../../../src/core/api/asgi_app.py#L380)) — под `require_service_auth`.
- `ServiceTokenAuth` ([`security.py:31-62`](../../../../src/core/api/security.py#L31)) — **опционален** (no-op без `SERVICE_API_TOKEN`); токен из `Authorization: Bearer` или `X-Service-Token` ([`security.py:16-27`](../../../../src/core/api/security.py#L16)).
- Пользовательский слой **отсутствует**: нет introspection-клиента; **ни одного env** `IDENTITY_*`/`INTROSPECT_*`/`OAUTH_*` в [`config/schema.py`](../../../../src/core/config/schema.py); `phone_verified` не проверяется.
- `submitter.external_user_id` + `identity_issuer` берутся **из тела как есть** ([`intake/contracts.py:223-227`](../../../../src/core/intake/contracts.py#L223)) → доходят до Story Store ([`application/services.py:238`](../../../../src/core/application/services.py#L238)).

### Identity (теперь ПОСТРОЕНО, 2026-06-24, по коду)
- `POST /oauth/introspect` ([`asgi_app.py:407`](../../../../../doge-identity-service/src/core/api/asgi_app.py#L407)), защищён `require_service_token` (вход без сервисного токена → 401/403).
- Контракт (RFC 7662, всегда HTTP 200): form-вход `token=<пользовательский токен>`; активный → `{active:true, sub, phone_verified}`, иначе `{active:false}` ([`oauth/introspection.py:14-32`](../../../../../doge-identity-service/src/core/oauth/introspection.py#L14)).
- `phone_verified` берётся из профиля по `claims.sub` (не из тела токена) ([`introspection.py:24-27`](../../../../../doge-identity-service/src/core/oauth/introspection.py#L24)).
- `/oauth/authorize`, `/oauth/token`, `/me` — также построены. → **разрыв на identity закрыт**; gateway-сторона реализуема end-to-end.

## Решения (D-GAUTH)

- **D-GAUTH-1 — Глубина:** углубить до **полного стандарта build-беклога** (как [issues-read-contract](../issues-read-contract/INDEX.md)): раздел «Что наблюдаю сейчас (verified)» с путями, подзадачи **T01–T05**, обогащённые AC/контракты, документ решений (этот), таблица в INDEX. Основание: identity OAuth/introspection **уже построен** → реализация больше не преждевременна.
- **D-GAUTH-2 — Охват auth:** двухслойную проверку применять к **всем мутациям публичного контента** (intake + любые будущие write-пути, влияющие на публичную доску), а не только к `/intake/stories`. Единая политика. (Уточняет open-question GAUTH-01.)
- **D-GAUTH-3 — Источник статуса:** анкер — **реально построенный `/oauth/introspect`** identity (form `token=…`, ответ `{active, sub, phone_verified}`, защищён сервисным токеном). Не `/me`. Gateway аутентифицируется перед identity своим сервисным токеном. (Закрывает open-question GAUTH-02.)
- **D-GAUTH-4 — Identity недоступен:** **fail-closed** — при недоступном/невалидном ответе introspection историю **не создавать** (нельзя считать непроверенного верифицированным). Без degraded-режима и без fallback на payload-submitter. (Закрывает open-question GAUTH-02 «безопасный отказ» и GAUTH-04 fallback.)

## Производные (зафиксировать в стори, не отдельные вопросы)
- **Автор (GAUTH-04):** при успешном introspection авторитетен **introspected `sub`**; расхождение с `submitter.external_user_id` из тела → в пользу `sub`. fail-closed (D-GAUTH-4) означает: нет introspection → нет истории → вопрос fallback снят.
- **`verification_required` (GAUTH-03):** канон тела + `verify_url` согласуется с identity [OAUTH-04](../../../../../doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md); различать `verification_required` (403, phone_verified=false) vs `invalid/expired token` (401) — разные next-action для GPT.

## Открытые (реализационные, не блокеры требований)
- Кэш introspection в пределах одного запроса (без «заморозки» статуса) — перф-решение в фокусном gateway-диалоге.
- Точные имена env gateway (`IDENTITY_INTROSPECT_URL`, `IDENTITY_SERVICE_TOKEN`) — на этапе реализации (EnvSpec в `config/schema.py`).
