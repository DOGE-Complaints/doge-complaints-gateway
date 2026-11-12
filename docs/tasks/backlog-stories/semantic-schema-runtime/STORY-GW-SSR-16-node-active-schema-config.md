# STORY-GW-SSR-16 — Node active schema (config + boot)

## Meta
- **Key:** `STORY-GW-SSR-16-node-active-schema-config`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — node-schema wave (sequence **16**)
- **Тип:** implement (config + boot resolve; первый слой)
- **Parent REQ:** 51 SCHEMA; INDEX **D-SSR-8**
- **Skill declared:** python-pro
- **Git:** только `semantic-schema-runtime` — [node-schema Шаг 0](./orchestrator-node-schema-runbook.md)
- **Зависит от:** SSR-15 (post-T-wave product Done)

## Зачем простыми словами

На диске несколько pack — это склад для отладки. Рабочая модель ноды должна быть **одна** и читаться из `.env`, не «первая папка» и не выбор клиента. При старте процесс либо поднимает этот pack, либо падает. Intake-gate — следующая стори.

## Scope / Out of scope

**In:** `EnvSpec` + поля `AppConfig`: **`NODE_SCHEMA_ID`**, **`NODE_SCHEMA_VERSION`** — оба **required**, без default ([`schema.py`](../../../../src/core/config/schema.py) `AppConfig` `:34–62`, `ENV_SCHEMA` `:65+`, `load_config_from_env` `:492`). Fail-fast как `API_BASE_URL` (`_require_value`). Boot: `resolve_pack(SchemaRef(id, version))`; нет каталога → `ConfigError`. Lifespan лог id/version ([`asgi_app.py`](../../../../src/core/api/asgi_app.py) `_lifespan` — рядом с `startup.config`). [`.env.test.example`](../../../../.env.test.example) две строки. [`server-env-quickstart.md`](../../../runtime-docs/manuals/server-env-quickstart.md) — одна секция. Тесты `tests/test_gw_ssr_16_*`. Общий pytest helper (monkeypatch обеих переменных), чтобы последующий suite не падал на load_config.

**Out:** проверка binding на intake (SSR-17); смена civic engine / `ClusterLens`; перенос `SCHEMA_PACKS_ROOT` в AppConfig (остаётся `os.environ` в [`resolver.py:19–30`](../../../../src/core/schema/resolver.py)); `GET /schema-active`; GPT UI.

## Verified current state

**As-of-Done (pkg-000073 G16 PASS 2026-08-30T14:24:58Z):**

| Fact | Ref |
|------|-----|
| `AppConfig.node_schema_id` / `node_schema_version` | [`schema.py:63–64`](../../../../src/core/config/schema.py) |
| Оба required, без default | EnvSpec [`:262–268`](../../../../src/core/config/schema.py); `_require_value` [`:684–685`](../../../../src/core/config/schema.py) |
| Boot `resolve_pack`; unknown → `ConfigError` | [`schema.py:506–518`](../../../../src/core/config/schema.py) / [`:686–689`](../../../../src/core/config/schema.py) |
| Lifespan логирует активную пару | [`asgi_app.py:121–128`](../../../../src/core/api/asgi_app.py) |
| `SCHEMA_PACKS_ROOT` | только `os.environ` в resolver; не в `AppConfig` |
| Склад | `legal_process/v1`, `mobility_observation/v1`, `tallinn_civic/v1` |

**Historical (pre-P3):** `AppConfig` без node schema полей ([`schema.py:34–62`](../../../../src/core/config/schema.py) тогда); lifespan логировал `db_backend` / cron, не pack id ([`asgi_app.py:110–138`](../../../../src/core/api/asgi_app.py) тогда).

## Стыковка

Не invent третье имя (`ACTIVE_PACK`). Пара = folder names loader: `schema-packs/<NODE_SCHEMA_ID>/<NODE_SCHEMA_VERSION>/`.

Pytest, который зовёт `load_config_from_env` / поднимает app, после этой стори **обязан** иметь обе переменные (фикстура 16). Массовая правка civic HTTP без binding — **SSR-17**.

## Подзадачи

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **T01** | Config | EnvSpec + AppConfig fields; required; fail-fast empty | Default «первый pack» |
| **T02** | Boot | resolve_pack на старте / load_config; unknown id → ConfigError | Тихий civic fallback |
| **T03** | Lifespan | Лог `node_schema_id` / version | Dump payload |
| **T04** | Env docs | `.env.test.example` + server-env строка | Railway secrets invent |
| **T05** | Tests | `test_gw_ssr_16_*` + monkeypatch helper | Intake 4xx (→ 17) |
| **T06** | Gate | missing env ConfigError; existing pack loads; missing dir ConfigError | |

## Target / AC

- [x] `NODE_SCHEMA_ID` и `NODE_SCHEMA_VERSION` в AppConfig; оба required.
- [x] Нет пары / нет каталога pack → процесс не стартует (`ConfigError`).
- [x] Каталог на диске резолвится (пример `tallinn_civic` / `v1`).
- [x] Lifespan логирует активную пару.
- [x] `SCHEMA_PACKS_ROOT` не перенесён в AppConfig в этой стори.

## Dependencies

- SSR-15 Done. Intake — SSR-17. Clustering skip mismatch — SSR-18.
