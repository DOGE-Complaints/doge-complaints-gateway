# STORY-GW-GAUTH-03 — Гейт верификации + `verification_required` (403)

> **↔ Reused (browser submit):** `evaluate_verification_gate` на `POST /story-drafts/{id}/submit` ([GW-DRAFT-02](../../story-draft-handoff/STORY-GW-DRAFT-02-browser-submit-verification-gate.md)). Разведение: [`gpt-submit-authz/INDEX.md`](./INDEX.md).

## Meta
- **Key:** `STORY-GW-GAUTH-03`
- **Status:** 🔵 Done (Awaiting Commits) — pipeline [pkg-000041](../../gateway-active-packages/pkg-000041-20260625-gw-gauth-03-verification-gate-403.yaml) (T01–T06, gate PASS 2026-06-25): `evaluate_verification_gate` (401/403/503), `verification_required` 403 по OAUTH-04 + `build_verify_url`; 7 contract + 548 unit. Код-аудит [`audit-gw-gauth-03-...`](../../../analysis/audit-gw-gauth-03-verification-gate-403-2026-06-25.md) — **закрывает G1 GAUTH-02** (`phone_verified` теперь enforced; цель пакета достигнута на уровне кода). CF-1: seed теперь требует verified user-токен (→ T07). SSOT исполнения — pipeline-копия.
- **Приоритет:** P1
- **Тип:** implement (gateway гейт + контракт отказа)
- **Закрывает:** отсутствие verify-гейта на intake (история создаётся без проверки `phone_verified`)
- **Источник процесса:** [`04-security §A`](../../../../../doge-identity-service/docs/runtime-docs/04-security.md) шаг 8 (+ Note «если `phone_verified=false` → 403»).
- **Основание:** [`interview-gpt-submit-authz-2026-06-24`](./interview-gpt-submit-authz-2026-06-24.md) (D-GAUTH-4)
- **Зависит от:** [GW-GAUTH-02](./STORY-GW-GAUTH-02-user-token-introspection.md)

## Зачем простыми словами
Историю можно принять только от **реального верифицированного** человека. Если телефон не подтверждён — это не «доступ запрещён навсегда», а сигнал: «сначала пройди верификацию». GPT по этому сигналу отправляет пользователя на verify и затем повторяет подачу.

## Что наблюдаю сейчас (контекст до реализации)

> Секция ниже — gap **до** GAUTH-03. Актуальное состояние — **Текущее состояние (post-Done)**.

## Текущее состояние (post-Done, verified)

- `evaluate_verification_gate` на `POST /story-drafts/{id}/submit` ([`verification_gate.py`](../../../../src/core/identity/verification_gate.py)); источник `{sub, phone_verified}` — [`me_client.py`](../../../../src/core/identity/me_client.py) → identity `/me` (не OAuth introspect на gateway).
- 403 `verification_required` + `verify_url` — [`envelope.py`](../../../../src/core/api/envelope.py), [`verify_url.py`](../../../../src/core/identity/verify_url.py).
- pkg-000041 gate PASS; 7 contract tests + 548 unit (audit 2026-06-25).

## Контекст до реализации (исторический)

- Intake создавал историю **без** проверки `phone_verified` (пользовательского слоя не было — см. superseded [GW-GAUTH-02](./STORY-GW-GAUTH-02-user-token-introspection.md)).

## Требование / целевое состояние
- История создаётся **только** при `active == true && phone_verified == true` (по ответу introspection из [GW-GAUTH-02](./STORY-GW-GAUTH-02-user-token-introspection.md)).
- Иначе при `phone_verified == false` — **HTTP 403** с телом `verification_required` (канон OAUTH-04), содержащим **куда вести пользователя** (`verify_url` / context), чтобы GPT дал ссылку и попросил повторить.
- **Неактивный/битый пользовательский токен** (`active == false`) → **401** (не `verification_required`) — другой next-action для GPT (перелогиниться, не verify).
- **Identity недоступен (fail-closed, D-GAUTH-4)** → отказ (история не создаётся); ответ — ошибка/повтор позже, **не** `verification_required` (это не «нужна верификация», а «не смогли проверить»).
- Контент истории при любом отказе **не сохраняется** как принятая история.

## Граница и контракт
- Сам verify-флоу (телефон: номер → OTP) — на стороне **identity/spa** (PV-флоу); здесь только **гейт** и **формат отказа**.
- Канон тела `verification_required` (+ `verify_url`) — единый с identity ([OAUTH-04](../../../../../doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md)); gateway его **переиспользует**, не вводит свой.
- Получение статуса на browser path — [`me_client.py`](../../../../src/core/identity/me_client.py) (GW-DRAFT-02), не OAuth introspection gateway (удалён GW-DRAFT-04).

## Подзадачи (черновик)
- **T01** — Гейт-функция: по `{active, phone_verified}` из GAUTH-02 решить `allow | verification_required | unauthorized | unavailable`.
- **T02** — 403 `verification_required` через `build_error_envelope`: тело по канону OAUTH-04 (`error`, `reason`, `verify_url`); источник `verify_url` — конфиг/identity.
- **T03** — Развести коды: `active=false` → 401; `phone_verified=false` → 403 `verification_required`; introspection unavailable → 5xx/«повторить» (fail-closed), **не** verification_required.
- **T04** — Гарантия «при отказе история не сохраняется» (ни как принятая, ни как side-effect проекции/кластеризации).
- **T05** — Тесты на все ветки (happy verified → 200; не верифицирован → 403 c verify_url; битый токен → 401; identity down → отказ) + story gate.

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
