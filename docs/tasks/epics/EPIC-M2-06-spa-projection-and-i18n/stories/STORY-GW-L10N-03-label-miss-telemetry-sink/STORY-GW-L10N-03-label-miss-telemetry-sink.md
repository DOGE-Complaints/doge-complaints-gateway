# STORY-GW-L10N-03 — Анонимный приём телеметрии непереведённых меток

## Meta
- **Key:** `STORY-GW-L10N-03`
- **Parent Epic:** [`../../../EPIC-M2-06-spa-projection-and-i18n.md`](../../../EPIC-M2-06-spa-projection-and-i18n.md)
- **Type:** Technical Story
- **Status:** 🔵 Done (Awaiting Commits)
- **source:** [`../../../../backlog-stories/localization-l10n/STORY-GW-L10N-03-label-miss-telemetry-sink.md`](../../../../backlog-stories/localization-l10n/STORY-GW-L10N-03-label-miss-telemetry-sink.md)
- **Закрывает:** REQ-BE-2
- **Источник:** [REQUIREMENTS-BACKEND-L10N §REQ-BE-2](../../../../../../../spa-app/docs/tasks/backlog-stories/localization/REQUIREMENTS-BACKEND-L10N.md); решение D-L10N-3
- **Decision Ref:** backlog file above; [`localization-l10n/INDEX.md`](../../../../backlog-stories/localization-l10n/INDEX.md) D-L10N-3
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000029-20260615-gw-l10n-03-label-miss-telemetry-sink.yaml`](../../../../gateway-active-packages/pkg-000029-20260615-gw-l10n-03-label-miss-telemetry-sink.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **7** тасков T01–T07; audit follow-up **T08** Done (`run_mode=gw_l10n_03_audit_followup`, G1/R1 closed 2026-06-15)
- **Зависит от:** —

## Зачем простыми словами
На фронте у меток issue есть «запасной» режим: если для метки нет перевода в словаре, она показывается «как есть» (humanize). Фронт хочет анонимно сообщать бэку: «вот этой метки нет перевода на таком-то языке», чтобы оператор видел растущий список и докручивал переводы. Никаких данных о пользователе — только ключ метки и язык.

## Что наблюдаю сейчас (verified по коду)
- Инфраструктуры событий/телеметрии на бэке нет (по api-reference §5/§7 endpoint-ов событий нет).
- Публичный POST **без авторизации** в системе уже существует — `POST /intake/stories` ([asgi_app.py:394](../../../../../../../src/core/api/asgi_app.py#L394)). Остальные POST закрыты `require_service_auth` ([asgi_app.py:378](../../../../../../../src/core/api/asgi_app.py#L378)). То есть анонимный приёмник архитектурно вписывается.
- Конверт ответа/трейс — общий `build_success_envelope` / `ensure_trace_id` ([envelope.py](../../../../../../../src/core/api/envelope.py)).
- Принцип «no analytics/cookies» пересматривается решением D11 фронта; данная телеметрия анонимна (без PII/идентификаторов).

## Требование / целевое состояние (решение D-L10N-3)
- **Эндпоинт-приёмник** анонимных событий humanize-miss. Минимальная нагрузка: **канонический ключ метки** + **локаль**, где не нашёлся перевод. Без PII, без идентификаторов пользователя/сессии.
- **Хранение:** отдельная таблица (новая) — напр. `label_translation_misses` с полями вида `label_key`, `locale`, `count`/`last_seen_at` (агрегат или сырые события — на усмотрение бэка).
- **Видимость оператору:** простой запрос/агрегатор «новые непереведённые ключи по локалям» (SQL/вьюха), без полноценного дашборда.
- Устойчивость: фронт при недоступности sink делает тихий no-op → endpoint не должен быть критичным путём; ошибки приёма не должны влиять на остальную систему.

## Контракт со стороны фронта (приёмка FE-POV)
- Фронт шлёт событие только на humanize-miss; объём минимальный (`label_key` + `locale`).
- Адрес sink конфигурируется на фронте env-переменной (по аналогии с `VITE_GATEWAY_BASE_URL`).
- Куки/идентификаторы фронт не добавляет; ответ может быть пустым/`202`.

## Предлагаемый контракт (на усмотрение бэка, как стартовая точка)
```
POST /telemetry/label-misses        # публичный, без токена
body: { "label_key": "string", "locale": "et|ru|en" }
→ 202 Accepted, { "data": {"accepted": true}, "trace_id": "..." }
```
- Валидация: `label_key` непустой, `locale` из набора; иначе мягкий 400 без деталей.
- Без rate-limit на MVP — зафиксировать как риск (см. ниже).

## Product decisions (fixed, P1 materialization)
- **Endpoint path:** `POST /telemetry/label-misses` — публичный, без `require_service_auth`.
- **Storage model:** агрегат `(label_key, locale)` + `count` + `last_seen_at` (не сырые события).
- **Response:** `202 Accepted` + success envelope с `data.accepted: true`.
- **Invalid payload:** мягкий `400` без деталей утечки.
- **Store failure:** изолированная обработка — endpoint не роняет ASGI; безопасный ответ.
- **Rate-limit:** out of scope MVP — риск зафиксирован в «Открытые вопросы».

## Out of scope
- Rate-limit / anti-abuse на MVP
- Полноценный operator dashboard
- PII / session / cookie tracking
- GW-L10N-04 label taxonomy registry
- SPA MT UI (frontend L10N)

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-l10n-03-t01-label-translation-misses-migration`](./task-gw-l10n-03-t01-label-translation-misses-migration/README.md) | pkg-000029 |
| 2 | [`task-gw-l10n-03-t02-label-miss-repository-and-di`](./task-gw-l10n-03-t02-label-miss-repository-and-di/README.md) | pkg-000029 |
| 3 | [`task-gw-l10n-03-t03-public-post-telemetry-handler`](./task-gw-l10n-03-t03-public-post-telemetry-handler/README.md) | pkg-000029 |
| 4 | [`task-gw-l10n-03-t04-operator-aggregate-query-view`](./task-gw-l10n-03-t04-operator-aggregate-query-view/README.md) | pkg-000029 |
| 5 | [`task-gw-l10n-03-t05-label-miss-acceptance-tests`](./task-gw-l10n-03-t05-label-miss-acceptance-tests/README.md) | pkg-000029 |
| 6 | [`task-gw-l10n-03-t06-openapi-api-reference-telemetry`](./task-gw-l10n-03-t06-openapi-api-reference-telemetry/README.md) | pkg-000029 |
| 7 | [`task-gw-l10n-03-t07-story-acceptance-gate`](./task-gw-l10n-03-t07-story-acceptance-gate/README.md) | pkg-000029 |
| 8 | [`task-gw-l10n-03-t08-decouple-label-miss-from-readiness`](./task-gw-l10n-03-t08-decouple-label-miss-from-readiness/README.md) | audit override (`run_mode=gw_l10n_03_audit_followup`) |

## Acceptance Criteria
- [x] Публичный `POST` принимает `{label_key, locale}` без токена и без PII.
- [x] Валидное событие фиксируется в отдельной таблице; повтор агрегируется/накапливается.
- [x] Невалидный payload → мягкая ошибка без утечки деталей; недоступность хранилища не влияет на другие пути.
- [x] Есть оператор-запрос для просмотра новых непереведённых ключей.
- [x] openapi/API_REFERENCE обновлены; зафиксирована анонимность.

## Открытые вопросы / риски к аналитике
- **Защита от злоупотреблений:** публичный анонимный POST → возможен спам/накрутка. Нужен ли rate-limit / дедуп по окну / cap на размер? (на MVP можно отложить, но зафиксировать.)
- Сырые события или сразу агрегат (счётчик по `label_key+locale`)? Агрегат дешевле и достаточен для «оператор видит рост». → **Закрыто P1:** агрегат.
- Путь endpoint (`/telemetry/label-misses` vs `/tallinn/...`) — согласовать неймспейс. → **Закрыто P1:** `/telemetry/label-misses`.

**Gate:** [`story-acceptance-gate-STORY-GW-L10N-03.md`](./story-acceptance-gate-STORY-GW-L10N-03.md) — PASS 2026-06-15
