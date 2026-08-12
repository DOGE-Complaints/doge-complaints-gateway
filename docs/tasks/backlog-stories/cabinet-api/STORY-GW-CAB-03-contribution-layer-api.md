# STORY-GW-CAB-03 — Contribution layer API (`GET /contribution/receipts` + `/records`)

## Meta
- **Key:** `STORY-GW-CAB-03-contribution-layer-api`
- **Пакет:** [`cabinet-api/`](./INDEX.md)
- **Status:** ⏸️ Deferred (post-MVP) — решение оператора 2026-07-14: **до web3-подключения**. Contribution (receipts/records) завязан на web3 `TxReceipt`; MVP-источника нет. Вернуться, когда появится web3-интеграция.
- **Приоритет:** 🟠 MED (отложен) — разблокирует SPA CAB-06 A/B (Receipts / Contribution Records)
- **Тип:** feature (new domain + 2 user-scoped read endpoints)
- **Tier:** **2** — ⚠️ модели данных нет (нужен новый источник)
- **Источник:** [`STORY-SPA-CAB-api-requirements.md` §0 + §2.3 + §4](../../../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-api-requirements.md)
- **Разблокирует:** SPA `CAB-06` States populated (A Receipts, B Records)
- **Зависит от:** **решение об источнике contribution-данных** (см. открытые вопросы)

## Зачем простыми словами
В кабинете «Contribution Layer» показывает вклад юзера: **Story Receipts** (квитанции о принятых историях) и **Contribution Records** (журнал действий). Сейчас таких данных в gateway **нет** — эндпоинты нужно наполнять из нового источника.

## MVP-контракты (§0, contract-first)
```
GET /contribution/receipts   (browser Bearer)
200 → { "data": { "count": int, "receipts": [ { "receipt_id": str, "story_id": str, "issued_at": str } ] } }

GET /contribution/records    (browser Bearer)
200 → { "data": { "count": int, "records": [ { "record_id": str, "kind": str, "occurred_at": str } ] } }
```
Author scoping: browser Bearer → `/me` → `sub`.

## Что наблюдаю сейчас (verified по коду)
| Элемент | Реальность |
|---------|-----------|
| Cabinet-receipt/record модель | **нет** — grep `receipt/contribution` в `src/` даёт только web3 `TxReceipt` ([adapters/types.py:7](../../../../src/core/adapters/types.py#L7)), это blockchain-tx-стаб, к кабинету **не относится** |
| Персистентность | нет таблицы/репозитория contribution/receipts |
| Что уже есть рядом | принятая история (`StoryRecord` с `submitter_external_user_id`) — потенциальный источник «receipt = факт принятой истории» |
| Auth-паттерн | browser Bearer → `/me` (как GW-CAB-01) |

## Открытые вопросы (решить в pass-2 — БЛОКИРУЮЩИЕ)
1. **Что порождает receipt/record?**
   - (а) **сабмит истории → receipt** (тонкий MVP: `receipts` = производная от моих принятых историй, `receipt_id`≈`story_id`, `issued_at`=`created_at`) — реализуемо без нового стораджа;
   - (б) web3-анкоринг (`TxReceipt`) как источник — но это post-MVP web3-слой;
   - (в) отдельный **contribution-лог** (новая таблица) — полноценно, дороже.
2. **`kind` у records:** какой enum действий журналируется (submitted / verified / clustered / …)? Согласовать с SPA CAB-06.
3. **Раздельность:** 1 стори на 2 эндпоинта (общий домен) — оставить вместе или разнести на CAB-03a/03b в pass-2.
4. **Персистентность:** нужна ли запись (новая таблица + миграция) или всё **производно** от существующих историй (вариант 1а — без стораджа).

> ⚠️ До ответа на (1) «populated»-состояние недостижимо. Вариант (1а) даёт дешёвый MVP на существующих данных; (1в) — отдельная модель.

## Границы
- **In scope (MVP):** CAB-06 **A (receipts)** + **B (records)** — user-scoped read.
- **Вне scope (POST-MVP):** CAB-06 **C Reputation** (числовой score/rank) — исключено из MVP (заглушка `comingSoon`).

## Pass-2 (не здесь)
Сначала — решение по вопросу 1 (источник данных, интервью), затем субтаски/DTO/handlers/(опц. модель+миграция)/тесты/AC.
