# STORY-GW-GAUTH-02 — Introspection пользовательского токена у identity

## Meta
- **Key:** `STORY-GW-GAUTH-02`
- **Parent Epic:** [`../../../EPIC-M2-20-gpt-submit-authz.md`](../../../EPIC-M2-20-gpt-submit-authz.md)
- **Type:** implement (gateway↔identity клиент)
- **Status:** 🔵 Implemented (Waiting Acceptance)
- **Приоритет:** P1
- **source:** [`../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-02-user-token-introspection.md`](../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-02-user-token-introspection.md)
- **Закрывает:** отсутствие пользовательского слоя на intake (gateway не зовёт identity)
- **Источник процесса:** [`04-security §A`](../../../../../../../doge-identity-service/docs/runtime-docs/04-security.md) шаг 7; [`09-gateway-expectations §Модель аутентификации`](../../../../../../../doge-identity-service/docs/runtime-docs/09-gateway-expectations.md).
- **Decision Ref:** backlog file above; [`interview-gpt-submit-authz-2026-06-24`](../../../../backlog-stories/gpt-submit-authz/interview-gpt-submit-authz-2026-06-24.md) (D-GAUTH-3, D-GAUTH-4); [`gpt-submit-authz/INDEX.md`](../../../../backlog-stories/gpt-submit-authz/INDEX.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000040-20260625-gw-gauth-02-user-token-introspection.yaml`](../../../../gateway-active-packages/pkg-000040-20260625-gw-gauth-02-user-token-introspection.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **6** тасков T01–T06; audit follow-up **T07** (`run_mode=gw_gauth_02_audit_cf1_followup`)
- **Зависит от:** [GW-GAUTH-01](../STORY-GW-GAUTH-01-two-layer-auth-on-submit/STORY-GW-GAUTH-01-two-layer-auth-on-submit.md)
- **Разблокирует:** [GW-GAUTH-03](../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-03-verification-gate-403.md), [GW-GAUTH-04](../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-04-authoritative-author-from-introspection.md)

## Зачем простыми словами
Чтобы решить, можно ли создать историю, gateway должен знать: жив ли пользовательский токен и **пройдена ли верификация** (`phone_verified`). По решению статус **не зашит в токен** — gateway каждый раз спрашивает identity и получает свежий ответ. Так статус нельзя «заморозить» в старом токене.

## Что наблюдаю сейчас (verified по коду)
- **Gateway:** introspection-клиента нет; **ни одного env** `IDENTITY_*`/`INTROSPECT_*` в [`config/schema.py`](../../../../../../src/core/config/schema.py); `phone_verified` нигде не читается.
- **Identity — endpoint ПОСТРОЕН (2026-06-24):** `POST /oauth/introspect` ([`asgi_app.py:407`](../../../../../../../doge-identity-service/src/core/api/asgi_app.py#L407)), защищён `require_service_token` (вход без сервисного токена → 401/403).
- **Контракт identity (RFC 7662, всегда HTTP 200)** ([`oauth/introspection.py:14-32`](../../../../../../../doge-identity-service/src/core/oauth/introspection.py#L14)):
  - вход: form-поле `token=<пользовательский access-токен>`;
  - активный → `{"active": true, "sub": <id>, "phone_verified": <bool>}`;
  - битый/пустой/просроченный → `{"active": false}`.
  - `phone_verified` берётся из профиля по `claims.sub` — **не из тела токена** ([`introspection.py:24-27`](../../../../../../../doge-identity-service/src/core/oauth/introspection.py#L24)).

## Требование / целевое состояние
- На verify-гейтед мутации gateway берёт **пользовательский** токен и вызывает identity `POST /oauth/introspect` (form `token=…`), получая `{ active, sub, phone_verified }` — **D-GAUTH-3** (анкер — реально построенный endpoint, не `/me`).
- Gateway аутентифицируется **перед** identity своим **сервисным токеном** (требование identity-входа `require_service_token`).
- Статус берётся **свежим у identity** на каждый такой запрос; не извлекается из тела токена.
- Ответ identity — единственный источник истины о пользователе для решения доступа.
- **Fail-closed (D-GAUTH-4):** identity недоступен / ответ невалиден / `active=false` → **безопасный отказ** (НЕ считать пользователя верифицированным; историю не создавать). Без degraded-режима и без fallback на payload-submitter.

## Out of scope
- Сам introspection-endpoint и его контракт — на стороне **identity** ([OAUTH-02](../../../../../../../doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md), **построен**); здесь — требование gateway **вызывать** его и доверять ответу.
- Решение «создавать/отказать» по статусу — [GW-GAUTH-03](../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-03-verification-gate-403.md); авторство по `sub` — [GW-GAUTH-04](../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-04-authoritative-author-from-introspection.md).

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-gauth-02-t01-identity-introspect-env-config`](./task-gw-gauth-02-t01-identity-introspect-env-config/README.md) | pkg-000040 |
| 2 | [`task-gw-gauth-02-t02-introspection-http-client`](./task-gw-gauth-02-t02-introspection-http-client/README.md) | pkg-000040 |
| 3 | [`task-gw-gauth-02-t03-wire-user-gate-to-introspection`](./task-gw-gauth-02-t03-wire-user-gate-to-introspection/README.md) | pkg-000040 |
| 4 | [`task-gw-gauth-02-t04-fail-closed-introspection-policy`](./task-gw-gauth-02-t04-fail-closed-introspection-policy/README.md) | pkg-000040 |
| 5 | [`task-gw-gauth-02-t05-introspection-contract-tests`](./task-gw-gauth-02-t05-introspection-contract-tests/README.md) | pkg-000040 |
| 6 | [`task-gw-gauth-02-t06-story-acceptance-gate`](./task-gw-gauth-02-t06-story-acceptance-gate/README.md) | pkg-000040 |
| 7 | [`task-gw-gauth-02-t07-audit-cf1-hosted-seed-identity-env-docs`](./task-gw-gauth-02-t07-audit-cf1-hosted-seed-identity-env-docs/README.md) | audit override (`run_mode=gw_gauth_02_audit_cf1_followup`) |

## Acceptance Criteria
- [x] Для verify-гейтед действия gateway получает от identity свежий `{ active, sub, phone_verified }` по пользовательскому токену через `POST /oauth/introspect`.
- [x] Gateway предъявляет identity свой сервисный токен (иначе identity отвечает 401/403).
- [x] Статус не берётся из тела токена.
- [x] Identity недоступен/ответ невалиден/`active=false` → **безопасный отказ** (fail-closed, D-GAUTH-4).
- [x] Контракт ответа соответствует построенному identity ([`introspection.py`](../../../../../../../doge-identity-service/src/core/oauth/introspection.py)).

## Открытые вопросы
- Кэшировать ли результат introspection в пределах одного запроса (без «заморозки» статуса) — перф-решение на этапе реализации.
- ~~Имя заголовка пользовательского токена на входе gateway~~ → **решено GAUTH-01:** `X-User-Token` ([`security.py:16-19`](../../../../../../src/core/api/security.py#L16)); согласовать с GPT-Action конфигом при деплое.
- **Doc prerequisite (audit G3):** перед/вместе с P3 обновить seed manuals — [`TASK-GW-GAUTH-01-T06`](../STORY-GW-GAUTH-01-two-layer-auth-on-submit/task-gw-gauth-01-t06-audit-g3-seed-docs-user-token/README.md) (`run_mode=gw_gauth_01_audit_g3_followup`) или в рамках GAUTH-02 P3.
