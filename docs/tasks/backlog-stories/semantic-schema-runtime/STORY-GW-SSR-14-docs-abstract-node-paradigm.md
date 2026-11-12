# STORY-GW-SSR-14 — Docs: abstract node public API (inventory)

## Meta
- **Key:** `STORY-GW-SSR-14-docs-abstract-node-paradigm`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — post-T-wave (sequence **14**)
- **Тип:** docs (операционные / нормативные; не rewrite аудитов)
- **Parent REQ:** D-SSR-7; 51 / spa-16 path contract после SSR-13
- **Skill declared:** python-pro (claims `analysis.mdc`)
- **Git:** `semantic-schema-runtime` — [пост-T-wave Шаг 0](./orchestrator-post-t-wave-runbook.md)
- **Зависит от:** SSR-13

## Зачем простыми словами

После смены URL код и SPA-клиенты уже на `/node/…`. Документы, которые **сейчас** учат `/tallinn/issues`, должны говорить тот же канон. Закрытые аудиты T-wave **не** переписывать.

## Scope / Out of scope

**In:** заменить публичные URL `/tallinn/issues|network-pulse|emerging-signals` на `/node/…` в списке ниже. Не менять смысл Pulse/Emerging, только путь. spa-15 sibling-строки 49/50 — да. Пакетные стори 08/11 формулировки read path, если ещё старые.

**Out:** `docs/analysis/audit-gw-ssr-0*`; spa `audit-STORY-SPA-ES-*`; примеры `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic`; G3 в [`orchestrator-t-wave-runbook.md`](./orchestrator-t-wave-runbook.md) (исторический gate).

## Подзадачи — инвентарь файлов (SSOT этого таска)

Один таск **T01**: пройти список; каждый файл — либо patched, либо «N/A (нет публичного URL / только geo)». Не invent новые manuals.

### Gateway runtime-docs

| Файл | Что менять |
|------|------------|
| [`api-reference/API_REFERENCE.md`](../../../runtime-docs/api-reference/API_REFERENCE.md) | Все секции Issues / Pulse / Emerging; оглавление |
| [`api-reference/openapi.yaml`](../../../runtime-docs/api-reference/openapi.yaml) | Если SSR-13 не закрыл descriptions |
| [`bootstrap-infrastructure/01-fastapi-transport.md`](../../../runtime-docs/bootstrap-infrastructure/01-fastapi-transport.md) | таблица маршрутов, `PUBLIC_ROUTES`, `handle_*` имена |
| [`bootstrap-infrastructure/06-testing-architecture.md`](../../../runtime-docs/bootstrap-infrastructure/06-testing-architecture.md) | примеры `client.get` |
| [`security-env-api-access.md`](../../../runtime-docs/security-env-api-access.md) | `POST /node/issues` |
| [`story-persistence-model.md`](../../../runtime-docs/story-persistence-model.md) | query example list issues |
| [`clustering-story-to-issue.md`](../../../runtime-docs/clustering-story-to-issue.md) | §результат GET (не `CLUSTER_GEO_SCOPE` value) |
| [`manuals/schema-packs-node-data-model-ru.md`](../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md) | карточка GET |
| [`manuals/seed-demo-data-runbook-ru.md`](../../../runtime-docs/manuals/seed-demo-data-runbook-ru.md) | curl / e2e |
| [`manuals/server-env-quickstart.md`](../../../runtime-docs/manuals/server-env-quickstart.md) | POST public-content |
| [`appendix/taxonomy-update-process-ru.md`](../../../runtime-docs/appendix/taxonomy-update-process-ru.md) | фильтр `?labels=` |

### Gateway requirements

| Файл | Что менять |
|------|------------|
| [`51-semantic-schema-runtime.md`](../../../requirements/51-semantic-schema-runtime.md) | sibling spa + verified `asgi` cite |
| [`49-early-signal-network-pulse-l1-api.md`](../../../requirements/49-early-signal-network-pulse-l1-api.md) | канон пути, не семантика L1 |
| [`50-early-signal-emerging-l2-api.md`](../../../requirements/50-early-signal-emerging-l2-api.md) | канон пути, не семантика L2 |

Grep `doge-complaints-gateway/docs/requirements` на `/tallinn/` — добить остаток, если есть.

### SPA (контракт путей, не overlay)

| Файл | Что менять |
|------|------------|
| [`16-semantic-schema-spa-compatibility.md`](../../../../../spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md) | если 13 не закрыл |
| [`15-early-signal-pre-cluster-public-dashboard.md`](../../../../../spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md) | sibling 49/50 URLs |
| [`spa-app/docs/requirements/README-index.md`](../../../../../spa-app/docs/requirements/README-index.md) | строка 15 paths |

**Не:** `spa-mvp-dashboard.md` / bullrun «Актуальная точка» (MVP snapshot). Если grep покажет только historical Done-строки — N/A + comment в gate.

### Пакет semantic-schema-runtime

INDEX / dashboard / формулировки SSR-08/11 read path — уже канон `/node` после этой волны. [`orchestrator-post-t-wave-runbook.md`](./orchestrator-post-t-wave-runbook.md) — rg `/node/`.

## Target / AC

- [x] Инвентарь T01 закрыт: каждый файл patched или N/A с причиной.
- [x] Операционные runtime-docs не учат `GET /tallinn/issues` как текущий контракт.
- [x] Аудиты T-wave / SPA-ES не переписаны.
- [x] Geo examples `settlement:tallinn` живы.

## Dependencies

- SSR-13 (код+SPA clients+16/51 минимум). Полный docs pass — эта стори.
