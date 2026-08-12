# STORY-GW-GAUTH-03 — Гейт верификации + `verification_required` (403)

## Meta
- **Key:** `STORY-GW-GAUTH-03`
- **Parent Epic:** [`../../../EPIC-M2-20-gpt-submit-authz.md`](../../../EPIC-M2-20-gpt-submit-authz.md)
- **Type:** implement (gateway гейт + контракт отказа)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** P1
- **source:** [`../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-03-verification-gate-403.md`](../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-03-verification-gate-403.md)
- **Закрывает:** отсутствие verify-гейта на intake (история создаётся без проверки `phone_verified`)
- **Источник процесса:** [`04-security §A`](../../../../../../../doge-identity-service/docs/runtime-docs/04-security.md) шаг 8 (+ Note «если `phone_verified=false` → 403»).
- **Decision Ref:** backlog file above; [`interview-gpt-submit-authz-2026-06-24`](../../../../backlog-stories/gpt-submit-authz/interview-gpt-submit-authz-2026-06-24.md) (D-GAUTH-4); [`gpt-submit-authz/INDEX.md`](../../../../backlog-stories/gpt-submit-authz/INDEX.md); [OAUTH-04](../../../../../doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000041-20260625-gw-gauth-03-verification-gate-403.yaml`](../../../../gateway-active-packages/pkg-000041-20260625-gw-gauth-03-verification-gate-403.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **6** тасков T01–T06
- **Зависит от:** [GW-GAUTH-02](../STORY-GW-GAUTH-02-user-token-introspection/STORY-GW-GAUTH-02-user-token-introspection.md)
- **Разблокирует:** [GW-GAUTH-04](../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-04-authoritative-author-from-introspection.md)

## Зачем простыми словами
Историю можно принять только от **реального верифицированного** человека. Если телефон не подтверждён — это не «доступ запрещён навсегда», а сигнал: «сначала пройди верификацию». GPT по этому сигналу отправляет пользователя на verify и затем повторяет подачу.

## Что наблюдаю сейчас (verified по коду)
- **GW-GAUTH-02 Done:** `require_user_token` вызывает identity introspection, сохраняет `request.state.user_introspection` с `{active, sub, phone_verified}` — [`asgi_app.py:272-290`](../../../../../../src/core/api/asgi_app.py#L272); `phone_verified` парсится — [`introspection_client.py:72-77`](../../../../../../src/core/identity/introspection_client.py#L72).
- **Гейт отсутствует:** после introspection проверяется только `active`; `phone_verified=false` **не** блокирует intake — история создаётся.
- **`active=false` / introspection fail** → **401** `UserTokenIntrospectionError` — [`asgi_app.py:287-288`](../../../../../../src/core/api/asgi_app.py#L287), handler [`asgi_app.py:245-248`](../../../../../../src/core/api/asgi_app.py#L245).
- **Нет `verification_required` / 403 auth path** — [`envelope.py:86-95`](../../../../../../src/core/api/envelope.py#L86) только `UnauthorizedError` → 401.
- **Нет env для `verify_url`** — grep `VERIFY`/`CORS` в [`schema.py`](../../../../../../src/core/config/schema.py) = 0.
- **Источник статуса построен:** introspection identity отдаёт `{active, sub, phone_verified}` ([`oauth/introspection.py:28-32`](../../../../../../../doge-identity-service/src/core/oauth/introspection.py#L28)).
- **Канон отказа зафиксирован у identity (OAUTH-04):** `verification_required` (403) = `{ "error": "verification_required", "reason": "...", "verify_url": "https://…/verify?context=…" }`, **под `phone_verified`** (не eID); enforcement — на стороне gateway ([OAUTH-04 §Требование/Граница](../../../../../doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md)).
- Формат ошибок gateway — общий envelope `build_error_envelope` ([`api/envelope.py:55`](../../../../../../src/core/api/envelope.py#L55)); 403-ответ ляжет в него.
- Intake deps = gate **до** handler — [`asgi_app.py:292-296`](../../../../../../src/core/api/asgi_app.py#L292) `_PUBLIC_CONTENT_WRITE_DEPS`.

## Требование / целевое состояние
- История создаётся **только** при `active == true && phone_verified == true` (по ответу introspection из [GW-GAUTH-02](../STORY-GW-GAUTH-02-user-token-introspection/STORY-GW-GAUTH-02-user-token-introspection.md)).
- Иначе при `phone_verified == false` — **HTTP 403** с телом `verification_required` (канон OAUTH-04), содержащим **куда вести пользователя** (`verify_url` / context), чтобы GPT дал ссылку и попросил повторить.
- **Неактивный/битый пользовательский токен** (`active == false`) → **401** (не `verification_required`) — другой next-action для GPT (перелогиниться, не verify).
- **Identity недоступен (fail-closed, D-GAUTH-4)** → отказ (история не создаётся); ответ — ошибка/повтор позже, **не** `verification_required` (это не «нужна верификация», а «не смогли проверить»).
- Контент истории при любом отказе **не сохраняется** как принятая история.

## Граница и контракт
- Сам verify-флоу (телефон: номер → OTP) — на стороне **identity/spa** (PV-флоу); здесь только **гейт** и **формат отказа**.
- Канон тела `verification_required` (+ `verify_url`) — единый с identity ([OAUTH-04](../../../../../doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md)); gateway его **переиспользует**, не вводит свой.
- Получение статуса — [GW-GAUTH-02](../STORY-GW-GAUTH-02-user-token-introspection/STORY-GW-GAUTH-02-user-token-introspection.md) (здесь не дублируется).

## Out of scope
- Сам verify-флоу (телефон: номер → OTP) — identity/spa (PV-флоу)
- Авторитетный `submitter` из introspection — [GW-GAUTH-04](../../../../backlog-stories/gpt-submit-authz/STORY-GW-GAUTH-04-authoritative-author-from-introspection.md)
- Draft persistence при отказе — продуктовое решение отложено (backlog §Открытые вопросы)

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-gauth-03-t01-verify-url-env-config`](./task-gw-gauth-03-t01-verify-url-env-config/README.md) | pkg-000041 |
| 2 | [`task-gw-gauth-03-t02-verification-gate-decision`](./task-gw-gauth-03-t02-verification-gate-decision/README.md) | pkg-000041 |
| 3 | [`task-gw-gauth-03-t03-verification-required-response`](./task-gw-gauth-03-t03-verification-required-response/README.md) | pkg-000041 |
| 4 | [`task-gw-gauth-03-t04-wire-gate-and-status-separation`](./task-gw-gauth-03-t04-wire-gate-and-status-separation/README.md) | pkg-000041 |
| 5 | [`task-gw-gauth-03-t05-verification-gate-contract-tests`](./task-gw-gauth-03-t05-verification-gate-contract-tests/README.md) | pkg-000041 |
| 6 | [`task-gw-gauth-03-t06-story-acceptance-gate`](./task-gw-gauth-03-t06-story-acceptance-gate/README.md) | pkg-000041 |

## Acceptance Criteria
- [x] `phone_verified == false` → **403 `verification_required`**, история не создаётся.
- [x] Ответ содержит `verify_url` / контекст (куда вести пользователя), по канону OAUTH-04.
- [x] `active == true && phone_verified == true` → история создаётся (happy path).
- [x] `active == false` (битый/просроченный токен) → **401** (отделён от verification_required).
- [x] Identity недоступен → отказ (fail-closed), не `verification_required`.
- [x] Формат `verification_required` совпадает с каноном identity ([OAUTH-04](../../../../../doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md)).

## Открытые вопросы
- ~~Различать «нужна верификация» vs «токен истёк»?~~ → **решено: да** (403 verification_required vs 401).
- Сохранять ли при отказе черновик (draft) на стороне gateway, чтобы не терять контент при повторе — **продуктовое решение отложено** (по умолчанию НЕ сохраняем; ср. draft-паттерн identity-frontend). При fail-closed (D-GAUTH-4) draft не создаётся.
