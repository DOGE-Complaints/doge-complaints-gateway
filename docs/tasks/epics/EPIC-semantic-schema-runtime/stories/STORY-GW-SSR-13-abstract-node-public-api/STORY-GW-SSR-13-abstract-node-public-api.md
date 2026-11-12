# STORY-GW-SSR-13 — Abstract public API (`/node/*`, hard cut `/tallinn/*`)

## Meta
- **Key:** `STORY-GW-SSR-13-abstract-node-public-api`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — post-T-wave product (sequence **13**; overnight **до** SSR-11)
- **Тип:** implement (HTTP paths + SPA clients; первый слой)
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-13-abstract-node-public-api.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-13-abstract-node-public-api.md)
- **Parent REQ:** 51 public read; sibling spa [`16-…`](../../../../../../../spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md) (**D-SSR-7**)
- **Decision:** INDEX **D-SSR-7** / **D-SSR-3** / **D-SSR-6**
- **decision_ref:** backlog SSR-13 + INDEX **D-SSR-7** / **D-SSR-3** / **D-SSR-6**
- **Skill declared:** python-pro (gateway); SPA path strings — тот же P3, не form builder
- **Etalon структуры:** [STORY-GW-SSR-10](../STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses/STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000069-20260829-gw-ssr-13-abstract-node-public-api.yaml`](../../../../gateway-active-packages/pkg-000069-20260829-gw-ssr-13-abstract-node-public-api.yaml)
- **Git:** только `semantic-schema-runtime` — [пост-T-wave Шаг 0](../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md)
- **Зависит от:** SSR-05
- **Scaffolded:** 2026-08-29T18:50:30Z

### Трассировка
| Слой | Документ | §§ |
|------|----------|-----|
| Child REQ | 51 public read; sibling spa-16 | D-SSR-7 |
| Decision | INDEX **D-SSR-7** `/node/*` hard cut, no alias; `settlement:tallinn` + pack id `tallinn_civic` stay; **D-SSR-3** identity; **D-SSR-6** SSR-06/07 Draft not this pkg |

- **Разблокирует:** G13 → SSR-11. **Not** SSR-06/07/11/12/14/15 this pkg
- **Не reopen:** SSR-01…05 / 08 / 09 / 10 product; T-wave G3 «`GET /tallinn/issues` stays» = historical
- **Не трогаем:** identity-service / claim keys (**D-SSR-3**); overlay UI (SSR-11)

## Nested tasks (pkg-000069)

| ID | Folder |
|----|--------|
| T01 | [`task-gw-ssr-13-t01-node-public-routes`](./task-gw-ssr-13-t01-node-public-routes/README.md) |
| T02 | [`task-gw-ssr-13-t02-rename-tallinn-handlers`](./task-gw-ssr-13-t02-rename-tallinn-handlers/README.md) |
| T03 | [`task-gw-ssr-13-t03-openapi-node-paths`](./task-gw-ssr-13-t03-openapi-node-paths/README.md) |
| T04 | [`task-gw-ssr-13-t04-spa-gateway-url-clients`](./task-gw-ssr-13-t04-spa-gateway-url-clients/README.md) |
| T05 | [`task-gw-ssr-13-t05-sibling-req-node-paths`](./task-gw-ssr-13-t05-sibling-req-node-paths/README.md) |
| T06 | [`task-gw-ssr-13-t06-story-acceptance-gate`](./task-gw-ssr-13-t06-story-acceptance-gate/README.md) |
| T07 | [`task-gw-ssr-13-t07-audit-g1-epic-story-ssot`](./task-gw-ssr-13-t07-audit-g1-epic-story-ssot/README.md) (P5 audit G1; not product AC) |

## Зачем простыми словами

Публичный API сейчас назван городом: `/tallinn/issues`, Pulse, Emerging. Для любой ноды это ложный контракт. Канон — нейтральный префикс **`/node/…`**. Старые URL **не** оставляем алиасом. SPA ходит в те же пути — правим репозитории и spa-16 **в этой стори** (исключение INDEX: только URL, не overlay карточки).

## Scope / Out of scope

**In (gateway):** роуты + OPTIONS + `PUBLIC_ROUTES` в [`asgi_app.py`](../../../../../../src/core/api/asgi_app.py) (`:59–67`, `:421–518`); хендлеры [`handle_tallinn_*`](../../../../../../src/core/api/handlers.py) → `handle_issues_list` / `handle_issue_get` / `handle_issue_create` (и аналоги Pulse/Emerging, если имена содержат `tallinn`); [`config/schema.py:127`](../../../../../../src/core/config/schema.py); канон в [`openapi.yaml`](../../../../../runtime-docs/api-reference/openapi.yaml) (полный нарратив API_REFERENCE — SSR-14, здесь минимум paths). После Done: **нет** `/tallinn/` в `src/core/api`.

**In (SPA, эта стори):** [`GatewayIssueRepository.js`](../../../../../../../spa-app/src/repositories/GatewayIssueRepository.js), [`GatewayNetworkPulseRepository.js`](../../../../../../../spa-app/src/repositories/GatewayNetworkPulseRepository.js), [`GatewayEmergingSignalsRepository.js`](../../../../../../../spa-app/src/repositories/GatewayEmergingSignalsRepository.js) + `__tests__`. Патч [`16-semantic-schema-spa-compatibility.md`](../../../../../../../spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md): read = `GET /node/issues`. Патч sibling-строки [`51-semantic-schema-runtime.md`](../../../../../requirements/51-semantic-schema-runtime.md).

**Out:** alias `/tallinn/*`; GPT instruction pack; IDX HTTP; `ClusterLens`; overlay полей карточки (SSR-11); переименование geo `settlement:tallinn`; pack id `tallinn_civic`; form builder.

## Verified current state

**As-of-Done (pkg-000069 G13):** `/node/*` **есть** — `PUBLIC_ROUTES` `/node/issues`, `/node/network-pulse`, `/node/emerging-signals` ([`asgi_app.py:65–67`](../../../../../../src/core/api/asgi_app.py)); GET/POST [`:462`](../../../../../../src/core/api/asgi_app.py)/[`:518`](../../../../../../src/core/api/asgi_app.py); handlers `handle_issues_list` / `handle_issue_get` / `handle_issue_create` ([`handlers.py:385,433,462`](../../../../../../src/core/api/handlers.py)); OpenAPI `/node/…`; spa three repos + spa-16 `GET /node/issues`. No alias. `/tallinn/` empty in `src/core/api`.

**Historical (pre-P3):** city prefix `/tallinn/issues` + `handle_tallinn_*` + OpenAPI `/tallinn/…` + spa-16 «Keep `GET /tallinn/issues`».

| Fact | Ref |
|------|-----|
| Public routes | [`asgi_app.py:65–67`](../../../../../../src/core/api/asgi_app.py) `/node/issues`, `/node/network-pulse`, `/node/emerging-signals` |
| GET list / get / POST | [`:462`](../../../../../../src/core/api/asgi_app.py), `:504`, `:518` |
| Handlers | [`handlers.py:385,433,462`](../../../../../../src/core/api/handlers.py) `handle_issues_list` / `handle_issue_get` / `handle_issue_create` |
| OpenAPI | [`openapi.yaml`](../../../../../runtime-docs/api-reference/openapi.yaml) `/node/…` |
| SPA Issue | [`GatewayIssueRepository.js:77,85`](../../../../../../../spa-app/src/repositories/GatewayIssueRepository.js) `/node/issues` |
| spa-16 | `GET /node/issues` (Keep `/tallinn/issues` **Historical**) |

## Стыковка

Hard cut: `/tallinn/issues` → 404. SSR-15 покрывает негатив-тест. Не оставлять оба префикса «на всякий случай».

T-wave AC «`GET /tallinn/issues` stays» — **исторический** (SSR-05 Done). Новый канон = D-SSR-7. Не переписывать closed P4-аудиты.

SSR-11 execute **после** этой стори: public read = `/node/issues`.

## Подзадачи (первый слой)

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **T01** | Gateway routes | `/node/issues`, `/{id}`, POST, Pulse, Emerging + OPTIONS + `PUBLIC_ROUTES` | Alias `/tallinn` |
| **T02** | Handlers | Rename `handle_tallinn_*`; импорт в asgi | Новая семантика Pulse/Emerging |
| **T03** | OpenAPI paths | Paths `/node/…` в openapi.yaml | Полный проход всех manuals (→ SSR-14) |
| **T04** | SPA clients | Три repository + unit tests | Overlay UI; form builder |
| **T05** | Sibling REQ | spa-16 + 51 sibling строка | REQ-45 GPT |
| **T06** | Gate | rg `/tallinn/` пуст в `src/core/api`; SPA fetch на `/node/` | |

## Target / AC

- [x] Канон: `GET/POST /node/issues`, `GET /node/issues/{issue_id}`, `GET /node/network-pulse`, `GET /node/emerging-signals`.
- [x] `/tallinn/` отсутствует в `src/core/api`.
- [x] SPA три репозитория бьют в `/node/…`.
- [x] spa-16 и REQ-51 sibling называют `/node/issues`, не город.
- [x] Нет alias.

## Dependencies

- SSR-05 Done. Overlay — SSR-11. Docs inventory — SSR-14. Gateway pytest URL — SSR-15.
