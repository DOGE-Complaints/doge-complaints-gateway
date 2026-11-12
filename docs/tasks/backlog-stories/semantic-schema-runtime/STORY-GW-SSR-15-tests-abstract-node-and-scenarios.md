# STORY-GW-SSR-15 — Tests: `/node/*` naming + scenario spectrum

## Meta
- **Key:** `STORY-GW-SSR-15-tests-abstract-node-and-scenarios`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — post-T-wave (sequence **15**; конец overnight)
- **Тип:** test (pytest + сценарии; не live_integration proof)
- **Parent REQ:** D-SSR-7
- **Skill declared:** python-pro
- **Git:** `semantic-schema-runtime` — [пост-T-wave Шаг 0](./orchestrator-post-t-wave-runbook.md)
- **Зависит от:** SSR-13; pack-сценарии — после execute 08 (и 10, если уже Done)

## Зачем простыми словами

Клиенты и роуты уже `/node/…` (SSR-13). Тесты gateway всё ещё бьют в `/tallinn/…` и закрепляют город в именах. Нужно: URL/хендлеры = канон; плюс **сценарии** civic / pack / Pulse≠Issues / 404 на старый путь — не только «строка в assert».

## Scope / Out of scope

**In (gateway `tests/`):** все обращения к публичным URL с `/tallinn/` (не geo fixtures `admin_settlement=tallinn` / `CLUSTER_GEO_SCOPE`). Предпочесть **rename** [`test_req24_tallinn_issues_read_api.py`](../../../../tests/test_req24_tallinn_issues_read_api.py) → нейтральное имя (например `test_req24_issues_read_api.py`), чтобы test id не держал город.

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

**As-of-Done (pkg-000072 G15 PASS 2026-08-29T19:47:15Z):** HTTP asserts `/node/…`; req24 renamed; scenarios + T-dual in `tests/test_gw_ssr_15_scenarios.py`; leftover `client.get("/tallinn/issues")` = T05 404 only.

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
