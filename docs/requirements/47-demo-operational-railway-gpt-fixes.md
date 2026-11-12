# REQ-47: Demo операционные задачи — Railway + GPT-скрипты

**Статус:** §2 GPT-часть ПЕРЕНЕСЕНА → `GPT UI/docs/requirements/REQ-35-demo-field-population-gpt-fixes.md` (2026-06-03); §3 Railway ops — остаётся здесь, ready for tasking
**Источник:** `GPT UI/docs/analysis/1.06.26-testing-gap-report.md` + PM/CTO interview 2026-05-28  
**Дата:** 2026-05-28  
**Приоритет:** P2  
**Тип:** операционные + GPT-инструктажный слой — без изменений в Python backend  
**Парный REQ:** REQ-46 (backend code patch); **GPT-side REQ-35** (GPT UI — носитель §2 после переноса)  
**Зависит от:** REQ-26 (location_query), REQ-32 (origin_source), REQ-42 (gpt_signals)

> **Перенос §2 (2026-06-03):** GPT-инструктажные задачи §2.1–2.4 проверены по фактическому коду инструкций/yaml. Бóльшая часть уже закрыта парными REQ-26/32/34/27 (origin.source, summary, location wire-маппинг, gpt_signals enums). Остаточная дельта (location_query obligation+латиница, origin.conversation_id guidance, активное определение severity) вынесена в **GPT UI REQ-35**. Раздел §2 ниже сохранён как исторический источник; единый владелец GPT-дельты — REQ-35. Этот файл далее ведёт **только** §3 Railway ops.

---

## 1. Контекст

Тест-прогон `2026-06-01` показал что несколько полей пустые **не из-за бага в backend**, а из-за того что GPT просто не отправил эти данные в запросе:

| Пустое поле в БД | Причина |
|-----------------|---------|
| `geo_*` (18 полей) | GPT не включил `location_query` в запрос, хотя пользователь упомянул Таллинн |
| `origin_source` | GPT не отправил блок `origin.source = "openai_gpt_action"` |
| `origin_conversation_id` | GPT не отправил `origin.conversation_id` |
| `narrative_summary_json` | GPT не включил `summary` в запрос |
| `gpt_signals` → story_signals | Частично GPT-side (посланы правильно), частично backend |

Backend всё принимает корректно когда данные присутствуют. Проблема — в GPT-инструктажных файлах.

---

## 2. Задачи GPT-side

### 2.1 location_query: всегда отправлять когда место упомянуто

**Проблема:** GPT не формирует `location_query` даже когда пользователь явно называет место (Таллинн, район, улицу).

**Что нужно:** обновить `api-orchestrator.md §5.2.1` и `story-normalizer.md §4.6` — добавить чёткое правило:

> Если пользователь в любой момент интервью упомянул город, район, улицу, ориентир — `location_query` ОБЯЗАТЕЛЕН.
> Формат: латиница, т.к. backend нормализует через `normalize_location_query()` (lowercase).
> Примеры: "Tallinn", "Kalamaja, Tallinn", "Tartu mnt 80, Tallinn"

**Важно для backend:** после REQ-46 stub-провайдер будет понимать кириллицу ("Таллин"), но латиница предпочтительна для надёжности.

**Файлы GPT UI:**
- `GPT UI/instructions/api-orchestrator.md §5.2.1` — строка `narrative.location_query`
- `GPT UI/instructions/story-normalizer.md §4.6` — правило formation

### 2.2 origin: всегда отправлять блок

**Проблема:** GPT не заполняет `origin.source`, `origin.conversation_id`.

**Что нужно:** в `api-orchestrator.md §5.2.1` — уточнить что `origin` блок ОБЯЗАТЕЛЕН (не optional):

```json
"origin": {
    "source": "openai_gpt_action",
    "conversation_id": "<активный conversation_id из сессии>",
    "tool_call_id": "<tool_call_id если есть>"
}
```

`origin.source = "openai_gpt_action"` — всегда, это константа.
`origin.conversation_id` — брать из доступного в GPT Actions контекста.

### 2.3 summary: формировать и отправлять

**Проблема:** `narrative_summary_json` пустое — GPT не формировал summary.

**Что нужно:** обновить `story-normalizer.md §4.1` — summary должно формироваться на Phase 7, передаваться в `canonical_payload.summary`. Оркестратор отправляет в `narrative.summary`.

Правило omit: только если GPT не уверен в полноте summary (все три слота `{et, ru, en}` должны быть непустыми).

### 2.4 gpt_signals: всегда включать когда определены

**Проблема:** тест показал что gpt_signals были отправлены (CITY, ONGOING) — это позитивный факт. Нужно убедиться что `severity` тоже определяется.

**Что нужно:** в `story-normalizer.md §4.3` — если в интервью есть достаточно контекста, заполнять все три поля (`severity`, `impact_estimation`, `problem_status`), не только два.

---

## 3. Railway deployment задачи

### 3.1 Верификация environment variables

Проверить что Railway Variables содержат:

```bash
DB_BACKEND=supabase
SUPABASE_URL=https://<ref>.supabase.co
SUPABASE_SERVICE_ROLE=<service_role_key>
APP_PROFILE=demo
API_BASE_URL=https://<railway-url>
LOG_LEVEL=INFO
LOG_FORMAT=json
```

Без `DB_BACKEND=supabase` сервер запускается с `in_memory` — все записи теряются после перезапуска.

### 3.2 Верификация DB readiness на Railway

После деплоя проверить `/ready` endpoint:

```bash
curl https://<railway-url>/ready | jq .
```

Ожидаемый ответ:
```json
{
  "data": {
    "status": "ready",
    "db_ready": true,
    "db_checks": {
      "connectivity": true,
      "schema": true,
      "columns": true,
      "columns_v2": true,
      "policy_probe": true
    }
  }
}
```

Если `db_ready: false` — смотреть какие именно checks упали и применять нужные миграции.

### 3.3 Применить миграции (если не применены)

Проверить что все миграции из `supabase/migrations/` применены к Railway Supabase проекту (через Supabase SQL Editor):

```sql
-- Проверка story_signals таблицы:
SELECT COUNT(*) FROM story_signals LIMIT 1;

-- Проверка v2 колонок:
SELECT narrative_title_json, narrative_session_language FROM stories LIMIT 1;
```

Если таблица `story_signals` не существует — применить `20260523_1200_req42_story_signals.sql`.

---

## 4. Acceptance Criteria

### GPT-скрипты (§2.1–2.4)
- [ ] История с упомянутым городом → `location_query` присутствует в запросе к API
- [ ] История с Таллинном → `location_query` содержит "Tallinn" (латиница)
- [ ] Каждый запрос к `/intake/stories` содержит `origin.source = "openai_gpt_action"`
- [ ] Каждый запрос содержит `origin.conversation_id` (не null)
- [ ] История с достаточным контекстом → `gpt_signals` содержит все три поля
- [ ] История при наличии достаточных данных → `narrative.summary` отправляется

### Railway (§3.1–3.3)
- [ ] `GET /ready` → `db_ready: true`, все 5 checks = true
- [ ] `POST /intake/stories` с корректным payload → story_id в Supabase `stories` таблице
- [ ] `gpt_signals` в запросе → запись в `story_signals` таблице
- [ ] В Railway logs: `startup.config db_backend=supabase`

---

## 5. Не в scope этого REQ

- Изменения в Python backend — scope REQ-46
- Реальный geocoding API — product backlog
- User authentication (wallet) — scope отдельного identity REQ
