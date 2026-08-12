# User Cabinet API (gateway side) — backend story package · index

**Зона:** `doge-complaints-gateway/docs/tasks/backlog-stories/cabinet-api/`
**Тип:** backlog (постановка задач; pass-1 — тонкие стори, детали/субтаски в pass-2).
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc) — факты по фактическому коду, пути указаны.
**Эпик-дом (gateway):** `EPIC-M2-22-user-cabinet-api` (gateway-сторона SPA `EPIC-SPA-07 User Cabinet`).

## Контекст одной фразой
SPA-кабинет (EPIC-SPA-07, стори CAB-01…07) написан **contract-first**: FE строит по MVP-контрактам как «сделано», а gateway реализует недостающие user-scoped read-эндпоинты **параллельно**. Здесь — только **gateway-MVP-гапы** (identity `/me`-extend и post-MVP wallet/reputation исключены).

## Источник требований (SSOT статуса поставки)
- [`spa-app/.../cabinet/STORY-SPA-CAB-api-requirements.md`](../../../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-api-requirements.md) §0 (MVP-контракты) + §4 (сводная матрица). Проверено 2026-07-12.

## Общий архитектурный паттерн (verified)
Все эндпоинты — **user-scoped read** под browser-Bearer: gateway форвардит Bearer в identity `GET /me` → author = `sub`. Паттерн уже есть: `IdentityMeClient` ([me_client.py](../../../../src/core/identity/me_client.py)) + read-dep `require_story_draft_read_user` (GW-DRAFT-02, browser Bearer → `/me`, active-session, без phone-гейта). Новые cabinet-роуты переиспользуют его.

## Стори пакета (pass-1 постановки)

| Order | Story | Контракт (§0) | Tier | Status |
|-------|-------|---------------|------|--------|
| 1 | [GW-CAB-01 — Story Activity API](./STORY-GW-CAB-01-story-activity-api.md) → [pipeline](../epics/EPIC-M2-22-user-cabinet-api/stories/STORY-GW-CAB-01-story-activity-api/STORY-GW-CAB-01-story-activity-api.md) | `GET /story-activity` | **1** (на готовых данных) | 🔵 Done (Awaiting Commits) pkg-000052 |
| 2 | [GW-CAB-02 — Current draft discovery](./STORY-GW-CAB-02-current-draft-discovery.md) → [pipeline](../epics/EPIC-M2-22-user-cabinet-api/stories/STORY-GW-CAB-02-current-draft-discovery/STORY-GW-CAB-02-current-draft-discovery.md) | `GET /story-drafts/current` | **2** (D-CAB02 interview 2026-07-14: gateway association on first read) | 🔵 Done (Awaiting Commits) pkg-000053 |
| 3 | [GW-CAB-03 — Contribution layer API](./STORY-GW-CAB-03-contribution-layer-api.md) | `GET /contribution/receipts` + `/records` | **2** (нет data-source — web3 `TxReceipt`) | ⏸️ Deferred (post-MVP, до web3; решение 2026-07-14) |

**Progress:** 2/3 Done (67%); GW-CAB-01 pkg-000052 + GW-CAB-02 pkg-000053 gate PASS 2026-07-14. GW-CAB-03 ⏸️ Deferred (post-MVP web3) — активных Todo в пакете нет.

## Принятое решение — доступ к черновикам (DOC-TASK-DRAFT-OWNERSHIP-01, 2026-07-23)

MVP-модель **capability + first-wins** (не баг, by design):

- Знание `draft_id` (`secrets.token_urlsafe(16)`) + валидный user-Bearer = право на GET и submit; ownership-gate на чтении/сабмите **нет**.
- `draft_owner.set_owner` = **first-wins** (DO NOTHING / ignore-duplicates / setdefault); `/current` scoped по первому владельцу.
- Strict ownership-gate — post-MVP.

SSOT + Security note: [DOC-TASK-DRAFT-OWNERSHIP-01](./DOC-TASK-DRAFT-OWNERSHIP-01-clarify-capability-model.md).

## Тиры реализуемости (verified по коду)
- **Tier 1 — на существующих данных:** `StoryRecord.submitter_external_user_id` хранится ([contracts.py:48](../../../../src/core/domain/contracts.py#L48), sqlite+supabase), `StoryRepository.list_stories()` есть ([contracts.py:79](../../../../src/core/domain/contracts.py#L79)). GW-CAB-01 реализуем; нужен user-scoped query + маппинг статуса + метрики.
- **Tier 2 — требует решения до реализации:**
  - **GW-CAB-02:** **разблокирован** интервью 2026-07-14 (D-CAB02-1..3): gateway-ассоциация при первом чтении + `updated_at` + latest non-expired by `created_at`. Pipeline pkg-000053.
  - **GW-CAB-03:** cabinet-contribution-модели в коде **нет** (только web3 `TxReceipt` в `adapters/`, к кабинету не относится). Нужен новый источник данных.

## Статус-факт (для маппинга CAB-04)
Ни один существующий enum не даёт `under_review`: `StoryLifecycleStatus` = `accepted/partial_ready/ready_for_profile/clustered` ([contracts.py:20](../../../../src/core/domain/contracts.py#L20)); issue `DOGEIssueStatus` = `DRAFT/PUBLISHED` ([enums.py:6](../../../../src/core/projection/enums.py#L6)). Маппинг `published/under_review` — продуктовое решение (pass-2).

## Границы пакета
- **In scope (MVP):** 3 gateway user-scoped read-эндпоинта из §4 (scope=MVP, backend=gateway, статус ❌).
- **НЕ трогаем:** identity `/me`-extension (email/created_at/account_status) — CAB-02, identity-владелец, отдельно.
- **POST-MVP (исключено):** CAB-05 wallet/web3 целиком; CAB-06 reputation (Module C).

## Порядок работы
- **Pass-1 (этот заход):** тонкие постановки (контракт, verified-реальность, тир, открытые вопросы). Субтаски/DTO/handlers/тесты/AC — **не** здесь.
- **Pass-2 (отдельно, по каждой стори):** уход в глубину — субтаски, готовые к реализации; предварительно закрыть открытые вопросы Tier-2 (интервью).
