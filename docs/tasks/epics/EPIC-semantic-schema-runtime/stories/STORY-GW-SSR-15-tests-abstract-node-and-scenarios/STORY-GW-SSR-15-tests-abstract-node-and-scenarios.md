# STORY-GW-SSR-15 — Tests: `/node/*` naming + scenario spectrum

## Meta
- **Key:** `STORY-GW-SSR-15-tests-abstract-node-and-scenarios`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — post-T-wave (sequence **15**; конец overnight)
- **Тип:** test (pytest + сценарии; не live_integration proof)
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md)
- **Parent REQ:** D-SSR-7
- **Decision:** INDEX **D-SSR-7**
- **decision_ref:** backlog SSR-15 + INDEX **D-SSR-7**
- **Skill declared:** python-pro
- **Etalon структуры:** [STORY-GW-SSR-13](../STORY-GW-SSR-13-abstract-node-public-api/STORY-GW-SSR-13-abstract-node-public-api.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000072-20260829-gw-ssr-15-tests-abstract-node-and-scenarios.yaml`](../../../../gateway-active-packages/pkg-000072-20260829-gw-ssr-15-tests-abstract-node-and-scenarios.yaml)
- **Git:** только `semantic-schema-runtime` — [пост-T-wave Шаг 0](../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md)
- **Зависит от:** SSR-13; pack-сценарии — после execute 08 (и 10, если уже Done)
- **Scaffolded:** 2026-08-29T19:41:20Z

### Трассировка
| Слой | Документ | §§ |
|------|----------|-----|
| Child REQ | D-SSR-7 | public `/node/*` hard cut |
| Decision | INDEX **D-SSR-7** `/node/*` hard cut; geo `settlement:tallinn` + pack id `tallinn_civic` stay |

- **Разблокирует:** G15 → конец волны. **Not** SSR-06/07/12 this pkg
- **Не reopen:** SSR-01…05 / 08 / 09 / 10 / 11 / 13 / 14 product; T-wave G3 historical
- **Не трогаем:** `live_integration` proof; alias 200; geo vocabulary `tallinn`; bullrun §«Актуальная точка»

## Nested tasks (pkg-000072)

| ID | Folder |
|----|--------|
| T01 | [`task-gw-ssr-15-t01-path-rename`](./task-gw-ssr-15-t01-path-rename/README.md) |
| T02 | [`task-gw-ssr-15-t02-civic-scenario`](./task-gw-ssr-15-t02-civic-scenario/README.md) |
| T03 | [`task-gw-ssr-15-t03-pack-scenario`](./task-gw-ssr-15-t03-pack-scenario/README.md) |
| T04 | [`task-gw-ssr-15-t04-pulse-emerging`](./task-gw-ssr-15-t04-pulse-emerging/README.md) |
| T05 | [`task-gw-ssr-15-t05-negative-tallinn-404`](./task-gw-ssr-15-t05-negative-tallinn-404/README.md) |
| T-dual | [`task-gw-ssr-15-t-dual-membership-public-path`](./task-gw-ssr-15-t-dual-membership-public-path/README.md) |
| T06 | [`task-gw-ssr-15-t06-story-acceptance-gate`](./task-gw-ssr-15-t06-story-acceptance-gate/README.md) |
| T07 | [`task-gw-ssr-15-t07-audit-g1-suite-isolation`](./task-gw-ssr-15-t07-audit-g1-suite-isolation/README.md) |

## Зачем простыми словами

Клиенты и роуты уже `/node/…` (SSR-13). Тесты gateway всё ещё бьют в `/tallinn/…` и закрепляют город в именах. Нужно: URL/хендлеры = канон; плюс **сценарии** civic / pack / Pulse≠Issues / 404 на старый путь — не только «строка в assert».

## Scope / Out of scope

**In (gateway `tests/`):** все обращения к публичным URL с `/tallinn/` (не geo fixtures `admin_settlement=tallinn` / `CLUSTER_GEO_SCOPE`). Предпочесть **rename** [`test_req24_tallinn_issues_read_api.py`](../../../../../../tests/test_req24_tallinn_issues_read_api.py) → нейтральное имя (например `test_req24_issues_read_api.py`), чтобы test id не держал город.

Файлы с URL (grep, не исчерпывающий до execute): `test_gw_ssr_03_*`, `test_gw_ssr_05_*` (assert `@app.get("/node/issues")`), `test_gw_es_02_*`, `test_gw_es_03_*`, smoke, `test_e2e_sandbox_full_pipeline.py`, `test_gw_gauth_01_*`, `test_gw_public_01_*`, `test_gw_rc_*`, `test_req35_geo_scope_and_filter.py` **только** если там HTTP path, не только geo token.

**SPA unit tests репозиториев:** в **SSR-13**, не дублировать здесь.

**Сценарии (обязательные AC):**

1. Civic без binding → list `GET /node/issues` (смысл текущего read API).
2. Schema-bound pack (`legal_process` или `tallinn_civic` после 08) → карточка на **том же** `/node/issues`.
3. Pulse → `/node/network-pulse`; Emerging → `/node/emerging-signals`; не issues.
4. Dual (SSR-10): если 10 ещё не Done к execute — подзадача **T-dual** = skip с пометкой «после 10»; иначе один тест dual membership + тот же public path.
5. Негатив: `GET /tallinn/issues` → **404**.

**Out:** `live_integration` как proof волны; IDX/QRY HTTP; alias 200 на `/tallinn`; менять geo vocabulary `tallinn`.

## Verified current state

Grep `tallinn` в `doge-complaints-gateway/tests` попадает и в URL, и в geo. Разделять: path vs settlement token.

**As-of-Done (pkg-000072 G15 PASS 2026-08-29T19:47:15Z; T07 suite exit 0 2026-08-29T19:57:04Z):** HTTP asserts `/node/…`; req24 renamed; scenarios + T-dual in `tests/test_gw_ssr_15_scenarios.py`; `@app.get("/tallinn"` empty; leftover `client.get("/tallinn/issues")` = T05 404 only. G15: 745 passed / 12 skipped / 10 deselected.

SSR-10 **Done** (G10 PASS 2026-08-29T18:31:19Z) — T-dual = **include**, не skip.

## Стыковка

Порядок overnight: 13 (роуты+SPA) → 11 → 14 → **15**. Если pytest красный сразу после 13 — допустимо до 15; gate G13 не требует полный `pytest` suite URL, G15 требует.

Не расширять `build_index` / filter routes.

## Подзадачи (первый слой)

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **T01** | Path rename | Все HTTP asserts `/node/…`; rename req24 file | Трогать geo `tallinn` fixtures |
| **T02** | Civic scenario | Unbound → GET `/node/issues` | |
| **T03** | Pack scenario | Bound pack → тот же path | Новый HTTP filter |
| **T04** | Pulse/Emerging | Отдельные `/node/` paths | Кормить Emerging из issues |
| **T05** | Negative | `/tallinn/issues` 404 | 301 alias |
| **T-dual** | Dual | После SSR-10 или skip | Выдумывать dual если 10 не Done |
| **T06** | Gate | `pytest -q -m "not live_integration"`; rg `@app.get("/tallinn"` пуст в tests **кроме** негатива 404 | |

## Target / AC

- [x] Публичные URL в pytest = `/node/…`.
- [x] Сценарии 1–3 и 5 зелёные; 4 по правилу T-dual.
- [x] Файл req24 без `tallinn` в имени (или явная N/A в gate, если rename ломает внешние ссылки — тогда comment + всё же path `/node`).
- [x] Не live_integration.

## Dependencies

- SSR-13. SSR-08 для pack scenario предпочтителен (иначе legal_process example pack). SSR-10 optional для T-dual.
