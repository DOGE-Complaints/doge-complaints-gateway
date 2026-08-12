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

| Order | Story | Status | Depends |
|-------|-------|--------|---------|
| 1 | [GW-DRAFT-01 — Стеш черновика](./STORY-GW-DRAFT-01-story-draft-stash.md) | Done | — |
| 2 | [GW-DRAFT-02 — Браузер-сабмит + гейт phone_verified](./STORY-GW-DRAFT-02-browser-submit-verification-gate.md) | Done | GW-DRAFT-01 |
| 3 | [GW-DRAFT-03 — Supersede gpt-submit-authz canon](./STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon.md) | Done | GW-DRAFT-01/02 |
| 4 | [GW-DRAFT-04 — Безопасное удаление осиротевшего GAUTH-кода](./STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md) | Done | GW-DRAFT-01/02/03 |
| 5 | [GW-DRAFT-05 — Dual intake contract stash vs submit](./STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md) | Done (Awaiting Commits) | GW-DRAFT-01/02 |
| 6 | [GW-DRAFT-06 — Удаление legacy `POST /intake/stories`](./STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md) | Done (P3 gate PASS pkg-000050) | GW-DRAFT-05 |
| 7 | [GW-DRAFT-07 — Hosted schema blocks browser submit](./STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md) | 🔵 Done (Awaiting Commits) · gate PASS pkg-000056 · pipeline [`STORY-GW-DRAFT-07`](../../epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md) · [`evidence`](../../../analysis/evidence-STORY-GW-DRAFT-07-hosted-submit-2026-08-07T070417Z.md) | GW-DRAFT-02 Done · TAX-01 код Done / hosted DDL applied |

**Progress:** 7/7 Done (100%); **DRAFT-07** closed P3 2026-08-07 — hosted `story_labels` + `/ready` + submit 202.

**Порядок:** 01 стеш → 02 браузер-сабмит+гейт → 03 канон/supersede → 04 безопасное удаление осиротевшего GAUTH-кода → **05** dual contract stash/intake → **06** удаление публичного `/intake/stories` + runner на story-drafts → **07** hosted schema ready для browser submit (ops / Public Node DDL + redeploy).

## Граница
- Идентичность/логин/verify/OAuth — identity + spa (reuse ID-08/ID-04). Здесь только gateway-часть: стеш, браузер-сабмит, гейт, гигиена кода.
- Осиротевший пакет [`gpt-submit-authz`](../gpt-submit-authz/INDEX.md) (GAUTH-01..04) — часть переиспользуется (03/04-инвентарь), часть удаляется (GW-DRAFT-04); история (аудиты/pkg) сохраняется (D-DRAFT-6).
- Кросс-репо канон identity (`04-security.md`) — не правим сами (D-DRAFT-5): gateway помечает + заводит identity-задачу.

## Связи (traceability)
- Контекст/gap-лист: [`mvp-integration-plan-2026-07-02.md`](../../../../../doge-identity-service/docs/analysis/mvp-integration-plan-2026-07-02.md) (M-3/M-7).
- Потребитель (spa): [SPA-ID-12](../../../../../spa-app/docs/tasks/backlog-stories/identity-auth/STORY-SPA-ID-12-story-draft-handoff-submit.md). Поставщик (GPT): [GPT-SUBMIT-01](../../../../../GPT%20UI/docs/tasks/backlog-stories/story-submit-handoff/STORY-GPT-SUBMIT-01-redirect-handoff.md).
- Hosted submit blocker (DRAFT-07): [SPA-BUG-01](../../../../../spa-app/docs/tasks/backlog-stories/bugs/STORY-SPA-BUG-01-story-submission-unavailable.md) · FE-HANDOFF-03.