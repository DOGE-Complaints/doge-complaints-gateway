# Story-draft handoff (browser-submit модель) · index

**Зона:** `doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/`
**Метод:** [`analysis.mdc`](../../../../../.cursor/rules/analysis.mdc) — факты по коду, пути указаны.
**Решение (интервью 2026-07-02/03):** модель создания истории развёрнута с «GPT сам сабмитит» на **«браузер сабмитит»**. См. [`mvp-integration-plan-2026-07-02.md §2`](../../../../../doge-identity-service/docs/analysis/mvp-integration-plan-2026-07-02.md).
**Решения интервью (2026-07-03):** [`interview-story-draft-handoff-2026-07-03.md`](./interview-story-draft-handoff-2026-07-03.md) (**D-DRAFT-1..6**) — SSOT выборов; стори ссылаются на `D-DRAFT-*`.

## Модель одной фразой
GPT по сервис-авторизации кладёт готовый JSON истории в **стеш** gateway → получает короткий `draft_id` → редиректит юзера в spa. Браузер (Supabase-сессия после логина+phone-verify) забирает черновик по `draft_id`, подтверждает и **сам сабмитит**; gateway проверяет `phone_verified` (через identity `/me`) и создаёт запись, атрибутированную верифицированному человеку. Контент в URL не гуляет (передаём ссылку, не payload).

## Решения интервью (D-DRAFT, 2026-07-03) — кратко
| D | Решение | Где |
|---|---------|-----|
| **D-DRAFT-1** | Проверка браузер-юзера — **identity `/me`-forward** (не локальная JWT-валидация) | [GW-DRAFT-02](./STORY-GW-DRAFT-02-browser-submit-verification-gate.md) |
| **D-DRAFT-2** | Стеш — **отдельный `StoryDraftRepository`** (порт+3 адаптера), TTL | [GW-DRAFT-01](./STORY-GW-DRAFT-01-story-draft-stash.md) |
| **D-DRAFT-3** | Сабмит — **новый `POST /story-drafts/{id}/submit`** (идемпотентность по draft_id) | [GW-DRAFT-02](./STORY-GW-DRAFT-02-browser-submit-verification-gate.md) |
| **D-DRAFT-4** | Осиротевший GAUTH — **отдельная стори безопасного удаления** | [GW-DRAFT-04](./STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md) |
| **D-DRAFT-5** | Канон identity `04-security` — **пометить в gateway + identity-задача** (не кросс-репо-правка) | [GW-DRAFT-03](./STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon.md) |
| **D-DRAFT-6** | Объём удаления — **только живой src+тесты**; аудиты/pkg/run-summary не трогать | [GW-DRAFT-04](./STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md) |

## Verified-факты пакета (по коду gateway)
- Порт-адаптер: порты в [`domain/contracts.py`](../../../../src/core/domain/contracts.py) (`StoryRepository`/`IdempotencyRepository`), адаптеры в [`infrastructure/`](../../../../src/core/infrastructure/), сборка per `DB_BACKEND` — `ServiceFactory`.
- Идемпотентность УЖЕ есть ([`api/idempotency.py`](../../../../src/core/api/idempotency.py)); envelope-коды `VALIDATION_ERROR`/`UNAUTHORIZED`/`VERIFICATION_REQUIRED`/`SERVICE_UNAVAILABLE`/`DOMAIN_ERROR` ([`envelope.py`](../../../../src/core/api/envelope.py)).
- Supabase-JWT в gateway НЕТ (grep=0) → браузер-проверка через identity `/me` (D-DRAFT-1).
- Переиспользуемое из gpt-submit-authz: `authoritative_submitter.py` (GAUTH-04), `verification_gate.py`+`verify_url.py`+`VerificationRequiredError` (GAUTH-03), value-object `IntrospectionResult`. Осиротело: OAuth-introspection-клиент токена GPT (GAUTH-02), `require_user_token`-путь (GAUTH-01), env `IDENTITY_INTROSPECT_URL/SERVICE_TOKEN`.

## Стори пакета
| S | Key | Требование | Приоритет | Зависит от |
|---|-----|------------|-----------|------------|
| 🟢 | GW-DRAFT-01 | [Стеш черновика: `POST /story-drafts` (service-auth) + `GET /story-drafts/{id}` (user-auth), TTL](./STORY-GW-DRAFT-01-story-draft-stash.md) | 🔴 HIGH | — |
| ⚪ | GW-DRAFT-02 | [Браузер-сабмит `POST /story-drafts/{id}/submit` + гейт `phone_verified` через identity `/me`](./STORY-GW-DRAFT-02-browser-submit-verification-gate.md) | 🔴 HIGH | GW-DRAFT-01 |
| ⚪ | GW-DRAFT-03 | [Supersede-пометки gpt-submit-authz + identity-задача на канон (docs)](./STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon.md) | 🟠 MED | GW-DRAFT-01/02 | 🔵 Done (pkg-000045) |
| ⚪ | GW-DRAFT-04 | [Безопасное удаление осиротевшего кода gpt-submit-authz (код, по инвентарю)](./STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md) | 🟠 MED | GW-DRAFT-01/02/03 | 🔵 Done (pkg-000046 + audit T08–T09) |
| ⚪ | GW-DRAFT-05 | [Dual intake contract: stash vs submit (убрать placeholder submitter)](./STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md) | 🟠 MED | GW-DRAFT-01/02, GPT-SUBMIT-02 | — |

**Порядок:** 01 стеш → 02 браузер-сабмит+гейт → 03 канон/supersede (docs + identity-задача) → 04 безопасное удаление осиротевшего кода → **05** раздельные domain-контракты stash/intake (рефакторинг hotfix `87fc272`).

## Граница
- Идентичность/логин/verify/OAuth — identity + spa (reuse ID-08/ID-04). Здесь только gateway-часть: стеш, браузер-сабмит, гейт, гигиена кода.
- Осиротевший пакет [`gpt-submit-authz`](../gpt-submit-authz/INDEX.md) (GAUTH-01..04) — часть переиспользуется (03/04-инвентарь), часть удаляется (GW-DRAFT-04); история (аудиты/pkg) сохраняется (D-DRAFT-6).
- Кросс-репо канон identity (`04-security.md`) — не правим сами (D-DRAFT-5): gateway помечает + заводит identity-задачу.

## Связи (traceability)
- Контекст/gap-лист: [`mvp-integration-plan-2026-07-02.md`](../../../../../doge-identity-service/docs/analysis/mvp-integration-plan-2026-07-02.md) (M-3/M-7).
- Потребитель (spa): [SPA-ID-12](../../../../../spa-app/docs/tasks/backlog-stories/identity-auth/STORY-SPA-ID-12-story-draft-handoff-submit.md). Поставщик (GPT): [GPT-SUBMIT-01](../../../../../GPT%20UI/docs/tasks/backlog-stories/story-submit-handoff/STORY-GPT-SUBMIT-01-redirect-handoff.md).
