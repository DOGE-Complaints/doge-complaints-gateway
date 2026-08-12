# STORY-M2-02-06: Data model registry §16 — follow-up gaps (верификация 2026-05-11)

## Meta
- Key: `STORY-M2-02-06`
- Parent Epic: [`../../../EPIC-M2-02-story-intake-and-store.md`](../../../EPIC-M2-02-story-intake-and-store.md)
- Type: Technical Story
- Status: Implemented (Waiting Acceptance/Commits)
- Stream: M2 Intake / contracts / observability
- Decision Ref (реестр гапов): [`../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md`](../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md) — **§16**, колонка «Статус (верификация 2026-05-11)»
- Gateway override (без смены YAML SSOT): `run_mode=story02_06_sec16_data_model_gaps` (T01–T06); **final tails:** `run_mode=story02_06_sec16_final_tails` (T07–T10) — см. [`.cursor/plans/Gateway_builder.plan.md`](../../../../../../../.cursor/plans/Gateway_builder.plan.md)
- Skill declared: `python-pro` (runtime), продуктовые правки GPT — отдельный репозиторий / инструкции по scope таска

## Story Goal
Закрыть или явно задокументировать **не закрытые** и **частично закрытые** разрывы из §16 сводного реестра (после внешней верификации 2026-05-11): мультиязычный title, summary, origin из GPT-потока, персистенция `live_story_context`, pytest vs lifespan логирование, операционный риск `DB_BACKEND` и синхронизация текста верификации в анализе с фактом кода.

## Scope
- Только GAP с статусом **НЕ ЗАКРЫТ**, **ЧАСТИЧНО** в §16 (GAP-01 DEFERRED, GAP-05 BY DESIGN — вне этой story).
- Не менять канонический `pkg-000011` и `gateway-active-package.current.yaml`; очередь Build по умолчанию остаётся YAML.
- **Final tails:** подтаски T07–T10 закрывают хвосты из раздела анализа [«Незакрытые хвосты — финальный прогон»](../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md) (раннер `simulation_runner`, TestClient E2E по canvas, hosted Supabase миграции, Railway `DB_BACKEND`).

## Nested tasks

| Order | Task folder |
|-------|-------------|
| 1 | [`task-m2-02-06-t01-gap-02-title-multilingual-transport`](./task-m2-02-06-t01-gap-02-title-multilingual-transport/README.md) |
| 2 | [`task-m2-02-06-t02-gap-03-summary-transport-and-storage`](./task-m2-02-06-t02-gap-03-summary-transport-and-storage/README.md) |
| 3 | [`task-m2-02-06-t03-gap-04-origin-gpt-orchestrator-payload`](./task-m2-02-06-t03-gap-04-origin-gpt-orchestrator-payload/README.md) |
| 4 | [`task-m2-02-06-t04-gap-06-live-story-context-persist-or-contract`](./task-m2-02-06-t04-gap-06-live-story-context-persist-or-contract/README.md) |
| 5 | [`task-m2-02-06-t05-gap-10-pytest-logging-lifespan-hardening`](./task-m2-02-06-t05-gap-10-pytest-logging-lifespan-hardening/README.md) |
| 6 | [`task-m2-02-06-t06-gap-11-db-backend-ops-warning-doc-sync`](./task-m2-02-06-t06-gap-11-db-backend-ops-warning-doc-sync/README.md) |
| 7 | [`task-m2-02-06-t07-gap-02-03-simulation-runner-intake-payload-parity`](./task-m2-02-06-t07-gap-02-03-simulation-runner-intake-payload-parity/README.md) |
| 8 | [`task-m2-02-06-t08-gap-02-03-04-testclient-simulation-canvas-intake`](./task-m2-02-06-t08-gap-02-03-04-testclient-simulation-canvas-intake/README.md) |
| 9 | [`task-m2-02-06-t09-gap-07-08-hosted-supabase-migration-ops`](./task-m2-02-06-t09-gap-07-08-hosted-supabase-migration-ops/README.md) |
| 10 | [`task-m2-02-06-t10-gap-11-railway-db-backend-supabase-env`](./task-m2-02-06-t10-gap-11-railway-db-backend-supabase-env/README.md) |

## AC / DoD (story level)
- [x] Каждый подтаск T01–T06 доведён до DoD; артефакты процесса в папках `task-m2-02-06-t0*`.
- [x] Строки §16 (GAP-02/03/04/06/10/11) в `data-model-vs-bootstrap-000-full-init-2026-05-08.md` синхронизированы с кодом.
- [x] `bullrun-launch-index.md` — статусы T01–T06 и story обновлены (🔵 до коммитов/приёмки).
- [x] Подтаски T07–T08 (final tails): исполнение и закрытие AC в README (`simulation_runner`, `test_e2e_simulation_canvas_intake.py`).
- [ ] Подтаски T09–T10 (final tails): ops-чеклисты hosted миграций / Railway; исполнение и закрытие AC в README.

---

## Таблица: gap → task → файлы → статус

| Gap (§16) | Task (README) | Целевые файлы / артефакты | Статус |
|-----------|---------------|---------------------------|--------|
| GAP-02 | [`task-m2-02-06-t01-gap-02-title-multilingual-transport`](./task-m2-02-06-t01-gap-02-title-multilingual-transport/README.md) | `intake/domain/services`, `db_*`, SQL, `api-orchestrator.md` | Done (impl) |
| GAP-03 | [`task-m2-02-06-t02-gap-03-summary-transport-and-storage`](./task-m2-02-06-t02-gap-03-summary-transport-and-storage/README.md) | `narrative_summary_json`, сервис, репозитории, bootstrap/migration | Done (impl) |
| GAP-04 | [`task-m2-02-06-t03-gap-04-origin-gpt-orchestrator-payload`](./task-m2-02-06-t03-gap-04-origin-gpt-orchestrator-payload/README.md) | `api-orchestrator.md`; gateway origin уже был | Done (impl) |
| GAP-06 | [`task-m2-02-06-t04-gap-06-live-story-context-persist-or-contract`](./task-m2-02-06-t04-gap-06-live-story-context-persist-or-contract/README.md) | `narrative_consistency_notes`, сервис, DDL | Done (impl) |
| GAP-10 | [`task-m2-02-06-t05-gap-10-pytest-logging-lifespan-hardening`](./task-m2-02-06-t05-gap-10-pytest-logging-lifespan-hardening/README.md) | `tests/conftest.py` autouse `configure_logging` | Done (impl) |
| GAP-11 | [`task-m2-02-06-t06-gap-11-db-backend-ops-warning-doc-sync`](./task-m2-02-06-t06-gap-11-db-backend-ops-warning-doc-sync/README.md) | §16 + `asgi_app` WARNING + `test_config_loading.py`; cross M2-09-05 T02 | Done (impl) |

### Final tails (раздел анализа «Незакрытые хвосты — финальный прогон»)

| Gap / хвост | Task (README) | Целевые файлы / артефакты | Статус |
|-------------|---------------|---------------------------|--------|
| GAP-02/03 (раннер не шлёт поля) | [`task-m2-02-06-t07`](./task-m2-02-06-t07-gap-02-03-simulation-runner-intake-payload-parity/README.md) | `tests/simulation_runner.py` | Done (impl) |
| GAP-02/03/04 (верификация без сервера) | [`task-m2-02-06-t08`](./task-m2-02-06-t08-gap-02-03-04-testclient-simulation-canvas-intake/README.md) | `tests/test_e2e_simulation_canvas_intake.py`, sandbox JSON; `pyproject.toml` (`pythonpath` + `tests`) | Done (impl) |
| GAP-07 + GAP-08 (hosted DB) | [`task-m2-02-06-t09`](./task-m2-02-06-t09-gap-07-08-hosted-supabase-migration-ops/README.md) | ops-чеклист в папке таска; `supabase/migrations/20260510_1400_m2_02_bootstrap_geo_embedding_nullable.sql` | Todo |
| GAP-11 (Railway env) | [`task-m2-02-06-t10`](./task-m2-02-06-t10-gap-11-railway-db-backend-supabase-env/README.md) | Railway Variables; cross M2-09-05 T02 | Todo |

«Done (impl)» = реализация и доки в ветке готовы; **этап 10 коммитов** — по `git-commit-prompt.md` после явного согласования оператора.
