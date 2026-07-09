# STORY-GW-DRAFT-01 — Стеш черновика истории (create + fetch)

## Meta
- **Key:** `STORY-GW-DRAFT-01-story-draft-stash`
- **Пакет:** [`story-draft-handoff/`](./INDEX.md)
- **Status:** 🟢 Done — pipeline [pkg-000043](../../gateway-active-packages/pkg-000043-20260703-gw-draft-01-story-draft-stash.yaml) (T01–T07, gate PASS 2026-07-03) + audit follow-up T08–T09 (2026-07-03): `StoryDraftRepository` порт+3 адаптера, `POST/GET /story-drafts`, TTL, 7 контракт-тестов; R1 DI fix (`test_di_service_factory.py` 10/10); R2 full unit 561/561 в gate. Код-аудит [`audit-gw-draft-01-...`](../../../analysis/audit-gw-draft-01-story-draft-stash-2026-07-03.md). G1 GET без auth → GW-DRAFT-02. SSOT исполнения — pipeline-копия.
- **Приоритет:** 🔴 HIGH (ядро M-3; без стеша нет handoff GPT→браузер)
- **Тип:** implement (новый ресурс + порт-адаптер store)
- **Основание:** [`interview-story-draft-handoff-2026-07-03`](./interview-story-draft-handoff-2026-07-03.md) (**D-DRAFT-2**); [`mvp-integration-plan-2026-07-02 §2,§4`](../../../../../doge-identity-service/docs/analysis/mvp-integration-plan-2026-07-02.md)
- **Зависит от:** —
- **Разблокирует:** [GW-DRAFT-02](./STORY-GW-DRAFT-02-browser-submit-verification-gate.md)

## Зачем простыми словами
GPT собрал историю, но сам её не публикует. Он **кладёт готовый JSON во временное хранилище** gateway и получает короткий `draft_id`, который передаёт браузеру через редирект. Браузер потом забирает черновик по этому id. Так контент не уходит в URL — передаём **ссылку, а не payload** (паттерн как OAuth authorization code).

## Что наблюдаю сейчас (verified по коду)
- **POST-роуты gateway:** `/tallinn/issues` ([asgi_app.py:459](../../../../src/core/api/asgi_app.py#L459)), `/intake/stories` ([:475](../../../../src/core/api/asgi_app.py#L475)), `/telemetry/label-misses`. Роутов `/story-drafts*` **нет**.
- **Порт-адаптер (гексагон):** порты — Protocols в [`domain/contracts.py`](../../../../src/core/domain/contracts.py) (`StoryRepository` save/get [:70-75](../../../../src/core/domain/contracts.py#L70), `IdempotencyRepository` [:99](../../../../src/core/domain/contracts.py#L99)); адаптеры — [`infrastructure/`](../../../../src/core/infrastructure/) (`repositories.py`, `db_sqlite.py`, `db_supabase.py`); сборка per `DB_BACKEND` — `ServiceFactory` ([service_factory.py:48-49](../../../../src/core/infrastructure/service_factory.py#L48)).
- **Сервис-авторизация (реюз):** `require_public_content_service_auth` (`ServiceTokenAuth.require(mandatory=True)`) ([asgi_app.py:291](../../../../src/core/api/asgi_app.py#L291), [security.py](../../../../src/core/api/security.py)) — **тот же** сервисный канал, что нужен GPT для стеша.
- **Контракт истории:** `parse_story_intake_request(payload)` ([intake/contracts.py](../../../../src/core/intake/contracts.py)) → `StoryIntakeRequest`; невалид → `IntakeValidationError` → envelope `VALIDATION_ERROR` ([envelope.py:71-82](../../../../src/core/api/envelope.py#L71)).
- **Идемпотентность (реюз):** `resolve_idempotency_key` ([api/idempotency.py](../../../../src/core/api/idempotency.py)); `IdempotencyRepository`.

## Требование / целевое состояние (D-DRAFT-2)
- **A. `POST /story-drafts`** — принимает контракт **`StoryDraftStashRequest`** (без `submitter`; см. [GW-DRAFT-05](./STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md) — разделение stash vs intake); **auth = только сервисный токен** (реюз `require_public_content_service_auth`, **без** user-слоя). Валидирует контракт, **сохраняет черновик** (issue НЕ создаётся), возвращает `{draft_id}` — короткий opaque id.
- **B. `GET /story-drafts/{draft_id}`** — отдаёт сохранённый черновик для предпросмотра. **auth = пользовательская** (браузерная сессия; конкретный механизм — [GW-DRAFT-02](./STORY-GW-DRAFT-02-browser-submit-verification-gate.md) через identity `/me`). Неизвестный/протухший id → 404.
- **C. Отдельный store `StoryDraftRepository`** (D-DRAFT-2): новый порт в `domain/contracts.py` + 3 адаптера (in_memory/sqlite/supabase) по образцу `StoryRepository`; черновик **≠** issue.
- **D. TTL** — черновик живёт ограниченно (реком. 1–24ч); по истечении → 404. `in_memory` для demo, `supabase` для durable.
- **E. Ошибки** — общий конверт `build_error_envelope` ([envelope.py:59](../../../../src/core/api/envelope.py#L59)): невалидный контракт → `VALIDATION_ERROR` (400); нет/битый сервисный токен → `UNAUTHORIZED` (401).

## Подзадачи (черновик)
- **T01** — Порт `StoryDraftRepository` (Protocol: `save_draft(record) -> draft_id`, `get_draft(draft_id) -> DraftRecord | None` с TTL) в [`domain/contracts.py`](../../../../src/core/domain/contracts.py); доменная модель `StoryDraftRecord` (draft_id, payload, created_at, expires_at).
- **T02** — 3 адаптера: in-memory ([`repositories.py`](../../../../src/core/infrastructure/repositories.py)), sqlite ([`db_sqlite.py`](../../../../src/core/infrastructure/db_sqlite.py)), supabase ([`db_supabase.py`](../../../../src/core/infrastructure/db_supabase.py)); проводка в `ServiceFactory` per `DB_BACKEND`.
- **T03** — Роут `POST /story-drafts` в [`asgi_app.py`](../../../../src/core/api/asgi_app.py): service-auth (реюз), `parse_story_intake_request` (валидация, без issue), генерация opaque `draft_id` + TTL, `{draft_id}`.
- **T04** — Роут `GET /story-drafts/{draft_id}`: выдача сохранённого JSON; 404 на unknown/expired (user-auth-хук — заглушка под GW-DRAFT-02).
- **T05** — Контракт-тесты (unit, паттерн `test_gw_*`): валидный сервисный токен → `{draft_id}`, issue НЕ создан; без токена → 401; невалидный контракт → 400 `VALIDATION_ERROR`; GET существующего → payload; GET unknown/expired → 404; TTL-истечение → 404. + story gate.

## Acceptance Criteria
- [ ] `POST /story-drafts` c валидным сервисным токеном сохраняет черновик и возвращает `{draft_id}`; issue при этом **не создаётся**.
- [ ] Без/с неверным сервисным токеном → **401 `UNAUTHORIZED`**, fail-closed.
- [ ] `GET /story-drafts/{draft_id}` отдаёт ранее сохранённый JSON; неизвестный/протухший id → **404**.
- [ ] Невалидный контракт истории → **400 `VALIDATION_ERROR`** (как `/intake/stories`).
- [ ] TTL соблюдается: по истечении — 404.
- [ ] Черновик хранится **отдельным** `StoryDraftRepository`, не смешан со story-store (D-DRAFT-2).

## Runtime-docs дельта
- [`api-reference/openapi.yaml`](../../../runtime-docs/api-reference/openapi.yaml) `paths:` — добавить `/story-drafts` (POST) и `/story-drafts/{draft_id}` (GET) по образцу `/intake/stories`.
- [`api-reference/API_REFERENCE.md`](../../../runtime-docs/api-reference/API_REFERENCE.md) — раздел стеша.
- [`story-persistence-model.md`](../../../runtime-docs/story-persistence-model.md) — модель draft-store + TTL.

## Открытые под-вопросы (реализация)
- Форма `draft_id` (opaque random + TTL); durable-cleanup для supabase-адаптера.
- Нужен ли на `GET` доп. one-time-секрет, или достаточно user-auth из GW-DRAFT-02 (привязка draft→user после логина).

## Швы
Новые роуты — [`asgi_app.py`](../../../../src/core/api/asgi_app.py); auth — [`security.py`](../../../../src/core/api/security.py); контракт — [`intake/contracts.py`](../../../../src/core/intake/contracts.py); порт — [`domain/contracts.py`](../../../../src/core/domain/contracts.py); адаптеры/DI — [`infrastructure/`](../../../../src/core/infrastructure/); ошибки — [`envelope.py`](../../../../src/core/api/envelope.py).

## Зависимости / связь
Потребитель `GET`+submit: [SPA-ID-12](../../../../../spa-app/docs/tasks/backlog-stories/identity-auth/STORY-SPA-ID-12-story-draft-handoff-submit.md). Поставщик `POST`: [GPT-SUBMIT-01](../../../../../GPT%20UI/docs/tasks/backlog-stories/story-submit-handoff/STORY-GPT-SUBMIT-01-redirect-handoff.md).
