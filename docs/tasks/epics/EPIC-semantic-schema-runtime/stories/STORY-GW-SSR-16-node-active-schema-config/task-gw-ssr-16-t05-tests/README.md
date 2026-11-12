# task-gw-ssr-16-t05-tests

## Task: tests — `test_gw_ssr_16_*` + monkeypatch helper (T05)

## Meta
- **Story:** [STORY-GW-SSR-16](../STORY-GW-SSR-16-node-active-schema-config.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000073
- **Skill declared:** python-pro
- **Depends on:** T01 T02
- **Scaffolded:** 2026-08-30T14:18:27Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-16-node-active-schema-config.md` T05

## Purpose
`tests/test_gw_ssr_16_*` + shared monkeypatch helper for **both** env vars (story: subsequent suite must not fail `load_config`). Cover: missing pair → `ConfigError`; empty → `ConfigError`; existing pack (`tallinn_civic`/`v1`) loads; unknown id / missing dir → `ConfigError`.

## Code Facts
- `tests/test_gw_ssr_16_*` — **0 files** this APPLY
- Etalon missing required — [`test_config_loading.py:102–104`](../../../../../../../tests/test_config_loading.py)
- `load_config_from_env` / `ConfigError` — [`tests/test_config_loading.py`](../../../../../../../tests/test_config_loading.py); [`tests/test_config_env_only_contract.py`](../../../../../../../tests/test_config_env_only_contract.py)
- Packs on disk — `schema-packs/tallinn_civic/v1/pack.json`
- G16 pytest = `tests/test_gw_ssr_16_*.py` only — [`orchestrator-node-schema-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md) §6.1 (`:222–230`)
- Mass civic HTTP fixture rewrite — **SSR-17** (not this task)

## Acceptance / DoD
- [x] `tests/test_gw_ssr_16_*` + helper monkeypatch обеих переменных
- [x] missing pair / empty → `ConfigError`
- [x] existing pack (`tallinn_civic` / `v1`) loads
- [x] unknown id / missing dir → `ConfigError`
- [x] No intake 4xx asserts
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_16_*.py` (+ helper module/fixture as needed)

## Out of scope
- Intake 4xx asserts (→ SSR-17). Mass civic HTTP fixture rewrite (→ SSR-17). Full-suite proof (G16 = `test_gw_ssr_16_*` only).
- Overlay bans (every task):
  - **`NODE_SCHEMA_ID` / `NODE_SCHEMA_VERSION` only.** Не invent `DEFAULT_SCHEMA_PACK` / `ACTIVE_PACK`.
  - **`SCHEMA_PACKS_ROOT` не поле `AppConfig`.** Остаётся `os.environ` в `resolver.py:19–30`.
  - **Нет intake gate** — SSR-17. **Нет смены `ClusterLens`.** Нет `GET /schema-active`. Нет filter HTTP. Нет `story_dimensions`.
  - **Нет SSR-06/07/12.** Не reopen 01–05/08–15. Stay `semantic-schema-runtime`.
  - Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md` / `spa-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
# P3 / G16 — from doge-complaints-gateway:
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_16_*.py
```
