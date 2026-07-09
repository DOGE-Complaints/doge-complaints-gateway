# Интервью CPO/CTO — story-draft-handoff (browser-submit модель) → решения

**Дата:** 2026-07-03
**Метод:** `.cursor/rules/analysis.mdc` — решения поверх verified-фактов (пути указаны).
**Контекст:** [`mvp-integration-plan-2026-07-02.md`](../../../../../doge-identity-service/docs/analysis/mvp-integration-plan-2026-07-02.md) — разворот модели с «GPT сам сабмитит» (пакет [gpt-submit-authz](../gpt-submit-authz/INDEX.md), GAUTH-01..04) на «браузер сабмитит».
**Назначение:** этот отчёт — SSOT решений; стори пакета ссылаются на `D-DRAFT-*` в точках выбора.

---

## Verified-факты перед решениями (по коду)

- **Порт-адаптер (гексагон):** порты — Protocols в [`domain/contracts.py`](../../../../src/core/domain/contracts.py) (`StoryRepository` save/get [:70-75](../../../../src/core/domain/contracts.py#L70), `IdempotencyRepository` [:99](../../../../src/core/domain/contracts.py#L99)); адаптеры — [`infrastructure/`](../../../../src/core/infrastructure/) (`repositories.py`/`db_sqlite.py`/`db_supabase.py`); DI — `bootstrap.py` + `service_factory.py`.
- **Идемпотентность УЖЕ есть:** [`api/idempotency.py`](../../../../src/core/api/idempotency.py) `resolve_idempotency_key`; intake шлёт `idempotency-key` ([asgi_app.py:486](../../../../src/core/api/asgi_app.py#L486)).
- **Supabase-JWT в gateway НЕТ:** grep `SupabaseJwt/jwks/joserfc` в `src/` = 0.
- **Story-drafts в gateway НЕТ:** greenfield (есть лишь несвязанный `StoryProjectionDraft`).
- **`_PUBLIC_CONTENT_WRITE_DEPS`** = `[require_public_content_service_auth, require_user_token]` ([asgi_app.py:332-334](../../../../src/core/api/asgi_app.py#L332)) на **двух** роутах: `/intake/stories` ([:475](../../../../src/core/api/asgi_app.py#L475)) и `/tallinn/issues` ([:459](../../../../src/core/api/asgi_app.py#L459)).
- **identity `/me`:** защищён `get_current_user` (валидирует Supabase Bearer), отдаёт `{sub, phone_verified}` ([me_response.py:42-45](../../../../../doge-identity-service/src/core/api/me_response.py#L42), [asgi_app.py:299](../../../../../doge-identity-service/src/core/api/asgi_app.py#L299)).

---

## Решения (D-DRAFT)

### D-DRAFT-1 — Проверка браузер-юзера: **identity `/me`-forward**
gateway пересылает Supabase-Bearer браузера в identity `GET /me` → `{sub, phone_verified}`. Реюз готового эндпоинта, identity остаётся единственным «хозяином личности», не дублируем крипту. Нужен новый мелкий `/me`-клиент в gateway + env `IDENTITY_BASE_URL` (образец — существующий HTTP-клиент [`introspection_client.py`](../../../../src/core/identity/introspection_client.py)). fail-closed при недоступности identity (принцип D-GAUTH-4). Отклонено: локальная Supabase-JWT-валидация (дублирует identity, тянет секреты).
→ [GW-DRAFT-02](./STORY-GW-DRAFT-02-browser-submit-verification-gate.md).

### D-DRAFT-2 — Хранилище стеша: **отдельный `StoryDraftRepository`**
Порт `StoryDraftRepository` в [`domain/contracts.py`](../../../../src/core/domain/contracts.py) + 3 адаптера (in_memory/sqlite/supabase) по образцу `StoryRepository`. Черновик ≠ issue, не смешиваются. **TTL** черновика (реком. 1–24ч, уточнить); `in_memory` для demo, `supabase` для durable (durable TTL требует cleanup — при реализации). Отклонено: реюз story-store с флагом `draft` (риск публикации черновика/утечки в проекцию).
→ [GW-DRAFT-01](./STORY-GW-DRAFT-01-story-draft-stash.md).

### D-DRAFT-3 — Роут финального сабмита: **новый `POST /story-drafts/{draft_id}/submit`**
Явная REST-семантика «подтвердить черновик», отделён от прямого intake, идемпотентность естественна по `draft_id` (реюз [`IdempotencyRepository`](../../../../src/core/domain/contracts.py#L99)). Отклонено: расширять `/intake/stories` (перегрузка одного эндпоинта двумя auth-моделями).
→ [GW-DRAFT-02](./STORY-GW-DRAFT-02-browser-submit-verification-gate.md).

### D-DRAFT-4 — Осиротевший GAUTH: **отдельная стори безопасного удаления (новая GW-DRAFT-04)**
Не «пометить superseded и оставить хвост», а **продуманно и безопасно удалить неиспользуемый код** осиротевшего функционала (против анти-паттерна «Legacy Accumulation»). Отдельная стори, **зависит от GW-DRAFT-01/02** (новая модель должна уже стоять) и GW-DRAFT-03 (канон помечен). Ключ — удалять **только осиротевшее**, не трогая переиспользуемое (см. §Инвентарь ниже).
→ новая [GW-DRAFT-04](./STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md) (создать при углублении).

### D-DRAFT-5 — Канон identity `04-security.md`: **пометить в gateway + завести identity-задачу**
GW-DRAFT-03 фиксирует as-built (browser-submit) в **gateway-доках** и **заводит явную identity-side задачу** на правку `04-security.md` §A (кросс-репо SSOT). Мы не редактируем чужой репо сами. Минус — канон временно рассинхронизирован (принять, зафиксировать в задаче).
→ [GW-DRAFT-03](./STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon.md).

### D-DRAFT-6 — Объём удаления (GW-DRAFT-04): **только живой src+тесты; историю не трогать**
Удаляем осиротевший **живой код** (GPT-специфика GAUTH-01/02) + его тесты; backlog-стори помечаем superseded. **Аудиты / `pkg-000039..042` / run-summary — НЕ трогаем** (иммутабельный аудиторский след). Чистим хвосты, не переписываем прошлое.

---

## Инвентарь: переиспользуется vs осиротело (verified 2026-07-03)

> Критично для D-DRAFT-4/6 — «безопасно» = удалять только осиротевшее.

| Компонент | Путь | Статус | Обоснование |
|-----------|------|--------|-------------|
| `authoritative_submitter.py` (автор=`sub`) | [src/core/identity/](../../../../src/core/identity/authoritative_submitter.py) | ✅ **ПЕРЕИСПОЛЬЗУЕТСЯ** | Браузер-сабмит тоже атрибутирует историю проверенному `sub` (GW-DRAFT-02) |
| `verification_gate.py` + `verify_url.py` + `VerificationRequiredError` | src/core/identity/, api/envelope.py | ✅ **ПЕРЕИСПОЛЬЗУЕТСЯ** | Браузер-путь гейтит `phone_verified`→403 `verification_required` |
| `IntrospectionResult` (value-object `{active,sub,phone_verified}`) | [introspection_client.py](../../../../src/core/identity/introspection_client.py) | ⚠️ **СОХРАНИТЬ (рефактор)** | Импортируется `verification_gate.py:5` и `authoritative_submitter.py:7`. Новый `/me`-клиент будет **производить** этот же shape → вынести в нейтральный модуль, НЕ удалять вместе с OAuth-клиентом |
| `IdentityIntrospectionClient` + `build_identity_introspection_from_config` (OAuth-introspect HTTP) | introspection_client.py, dependencies.py:16 | ❌ **ОСИРОТЕЛО** | OAuth-introspection токена GPT не нужна — переходим на `/me` (D-DRAFT-1) |
| env `IDENTITY_INTROSPECT_URL` / `IDENTITY_SERVICE_TOKEN` | schema.py:130,139 | ❌ **ОСИРОТЕЛО** (замена `IDENTITY_BASE_URL` для /me) | вход GPT-introspection уходит |
| `require_user_token` (OAuth-introspect на входящем запросе) | asgi_app.py:298 | ❌ **ОСИРОТЕЛО** для GPT-пути | GPT больше не шлёт `X-User-Token`; браузер идёт новым роутом |
| `_PUBLIC_CONTENT_WRITE_DEPS` на `/intake/stories` **и** `/tallinn/issues` | asgi_app.py:459,475 | ⚠️ **РЕШИТЬ в GW-DRAFT-04** | Судьба обоих роутов под user-layer: `/intake/stories` (GPT-путь) и `/tallinn/issues` (ручное создание) — оба несут `require_user_token`; чем заменяется user-слой — change-propagation анализ |

**Вывод инвентаря:** удаление НЕ равно «стереть `introspection_client.py`». Это: (1) вынести `IntrospectionResult` в нейтральный модуль, (2) удалить OAuth-introspect **клиент** + его DI + env, (3) снять `require_user_token`-OAuth с роутов и решить их user-слой, (4) сохранить gate/verify/author. Именно поэтому — отдельная продуманная стори (D-DRAFT-4).

---

## Открытые под-вопросы (решить при реализации, не блокируют углубление)
- Точная форма `draft_id` (opaque random + TTL) и durable-cleanup для supabase-адаптера.
- Нужен ли на `GET /story-drafts/{id}` доп. one-time-секрет, или достаточно user-auth (привязка draft→user после логина).
- Судьба `/tallinn/issues` user-слоя (ручное создание issue) — переиспользует ли новый браузер-auth или остаётся сервисным.
- `IDENTITY_BASE_URL` vs реюз базы из `IDENTITY_INTROSPECT_URL` для `/me`-клиента.

---

## Влияние на пакет (итог)
- **3 стори → 4:** добавляется **GW-DRAFT-04** (safe removal, D-DRAFT-4/6).
- Порядок: GW-DRAFT-01 (стеш) → GW-DRAFT-02 (браузер-сабмит+гейт) → GW-DRAFT-03 (канон/supersede docs + identity-задача) → **GW-DRAFT-04 (безопасное удаление осиротевшего)**.
- Каждая стори углубляется до build-стандарта (verified-state + T01–T05 + AC + runtime-docs дельта + тест-подзадачи), ссылаясь на `D-DRAFT-*` этого отчёта.
