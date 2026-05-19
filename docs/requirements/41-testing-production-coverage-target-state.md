# 41. Целевое состояние тестового покрытия — гарантия продакшн-сценариев

Дата: 2026-05-18  
Статус: requirements — ready for tasking  
Зависит от: REQ-39, REQ-28 (cron scheduler), REQ-35 (geo filter), REQ-40 (geo propagation)  
Область: `doge-complaints-gateway`

---

## 1. Контекст и цель

Текущая тест-система (412 тестов) покрывает бизнес-логику в рамках `FastAPI TestClient` — in-process HTTP без реального сетевого стека, без реальных сетевых задержек и без временно-зависимых сценариев кластеризации. Живая интеграция с Supabase (`tests/integration/supabase/`) требует внешних секретов и пропускается по умолчанию.

**Цель REQ-41**: определить целевое состояние тестового покрытия, при котором прохождение тест-сьюта является надёжной гарантией работоспособности в продакшн-сценариях — включая реальную HTTP точку входа, задержку сбора данных для кластеризации, асинхронное получение issues с фильтрацией и RLS-политики.

**Ключевой принцип**: тест верифицирует продакшн-сценарий, если он исполняет ту же кодовую ветку, что и продакшн, включая конфигурацию, транспорт, timing и I/O-адаптеры.

**Модель запуска реального HTTP-сервера**: тесты против реального HTTP-стека исполняются против локального сервера, запускаемого пользователем вручную:
```bash
uvicorn core.api.asgi_app:app --host 127.0.0.1 --port 8000
```
Тесты получают URL через env var `LOCAL_SERVER_URL` (default: `http://127.0.0.1:8000`). Без переменной — `pytest.skip`. Это обеспечивает реальный HTTP/1.1 стек (uvicorn + starlette routing + middleware), недоступный через `TestClient`.

---

## 2. Продакшн-сценарии — полный реестр

| ID | Сценарий | Текущий статус | Целевой статус |
|----|----------|----------------|----------------|
| PS-01 | Тест-клиент отправляет intake-запросы из sandbox canvas на реальный HTTP endpoint | ❌ Не покрыт | ✅ Local server smoke test (`LOCAL_SERVER_URL` + sandbox canvas) |
| PS-02 | Intake принимает payload, сохраняет story с geo | ✅ TestClient | ✅ Уже покрыт (REQ-33/35) |
| PS-03 | Stories накапливаются в БД за реальный временной интервал | ⚠️ sleep(1.2) mock | ✅ Cron timing E2E с реальной задержкой |
| PS-04 | `CLUSTER_CRON_INTERVAL_S` срабатывает → кластеризация запускается | ⚠️ Unit-тест с заглушкой | ✅ Full-stack cron + в-memory pipeline |
| PS-05 | `CLUSTER_MIN_SIZE` threshold — кластер не создаётся до порога | ✅ TestClient | ✅ Уже покрыт (REQ-39 J-01) |
| PS-06 | Кластер достиг порога → issue создаётся в `doge_issues` | ✅ TestClient | ✅ Уже покрыт (REQ-39 J-02) |
| PS-07 | `GET /tallinn/issues` без фильтров → все PUBLISHED issues | ✅ TestClient | ✅ Уже покрыт (REQ-24) |
| PS-08 | `GET /tallinn/issues?status=PUBLISHED` — статус-фильтр | ✅ TestClient | ✅ Уже покрыт |
| PS-09 | `GET /tallinn/issues?geo_district=põhja-tallinn` — geo-фильтр | ✅ TestClient | ✅ Уже покрыт (REQ-35) |
| PS-10 | `GET /tallinn/issues?bbox=...` — bbox-фильтр с null-safety | ✅ TestClient | ✅ Уже покрыт (REQ-39 M-06) |
| PS-11 | Параллельный intake от N пользователей — нет дублей | ❌ Не покрыт | ✅ Concurrent intake test |
| PS-12 | Idempotency-key повторный запрос — 202 без дубля story | ✅ TestClient | ✅ Уже покрыт |
| PS-13 | RLS-политика блокирует неавторизованный доступ к `doge_issues` | ⚠️ DDL-тест (offline) | ✅ Live Supabase RLS exec |
| PS-14 | Полный Supabase roundtrip: intake → cluster → issue → GET | ⚠️ Skip без секретов | ✅ CI-секреты + обязательный в prod |
| PS-15 | `policy_version = m3.doge_issue_derivation.v1` в продакшн-записи | ✅ SQLite SQL | ✅ Уже покрыт (REQ-39 J-03) |
| PS-16 | geo из story propagates в issue `payload_json.geo` | ✅ in-memory | ✅ Уже покрыт (REQ-40) |
| PS-17 | `CLUSTER_READINESS_THRESHOLD` — partial readiness не промоутит | ✅ TestClient | ✅ Уже покрыт (REQ-39 J-01 variant) |
| PS-18 | Railway env var injection — конфиг читается из env, не из .env | ⚠️ conftest блокирует dotenv | ✅ Isolated env-only test |
| PS-19 | Реальный HTTP-стек — uvicorn routing, ASGI middleware, response headers | ❌ Не покрыт | ✅ Local server smoke test (`LOCAL_SERVER_URL`) |
| PS-20 | API-ответ соответствует OpenAPI schema (runtime) | ✅ openapi_runtime_compliance | ✅ Уже покрыт |
| PS-21 | `X-Trace-Id` / `X-Request-Id` заголовки round-trip | ✅ trace_propagation | ✅ Уже покрыт (REQ-37) |
| PS-22 | PII-scrubbing в логах при intake | ✅ observability test | ✅ Уже покрыт (REQ-37) |
| PS-23 | Sandbox — все 130 canvas-сценариев проходят E2E | ✅ test_e2e_sandbox_full_pipeline | ✅ Уже покрыт (REQ-39 N-01..N-06) |
| PS-24 | Embedding policy version persisted для stories | ✅ versioning test | ✅ Уже покрыт |
| PS-25 | `required_columns_ready()` блокирует запуск при missing migration | ⚠️ Offline DDL check | ✅ Live Supabase migration state check |

---

## 3. Пробелы целевого состояния — детальный реестр

### GAP-41-01: Нет теста реальной HTTP точки входа с sandbox-данными (PS-01, PS-19)

**Описание**: Все 412 тестов используют `FastAPI TestClient` — in-process вызов ASGI-приложения без реального сетевого стека. Проблемы, которые тест-сьюта не обнаруживает: uvicorn-специфичное поведение (keep-alive, chunked encoding, connection errors), starlette middleware при реальном HTTP, response headers (Server, Content-Length), connection timeout handling.

Дополнительно: `tests/simulation_runner.py` — готовый CLI для отправки canvas-сценариев на реальный сервер — не интегрирован в pytest и не верифицирует response по сравнению с ожидаемым состоянием системы.

**Источник тестовых данных**: `tests/sandbox/dogestonia_simulation_canvas_v0_1.json`  
— 130 сценариев, 4 группы: `infrastructure`, `environment`, `digital`, `conflict`  
— Каждый сценарий конвертируется в intake payload через `_scenario_to_payload()` из `simulation_runner.py`

**Целевое решение**:
- `tests/smoke/test_local_server_smoke.py` — выполняется против локального uvicorn, запущенного пользователем вручную
- Транспорт: `httpx.Client(base_url=LOCAL_SERVER_URL)` — реальный TCP-сокет
- Импортирует `_scenario_to_payload` из `tests.simulation_runner` для конвертации canvas → payload
- Guard: `pytest.skip("LOCAL_SERVER_URL not set")` если env var отсутствует; `pytest.skip("server not reachable")` если сервер не отвечает на `/health`

**Что проверяется (не доступно через TestClient)**:
- Реальный HTTP response: `Content-Type: application/json`, `Server: uvicorn`
- `X-Request-Id` header через реальный middleware stack
- HTTP статус коды через полный ASGI → uvicorn → TCP цикл

**Тесты**:
- LS-01: `GET /health` → 200, тело содержит `"status"`
- LS-02: `POST /intake/stories` — payload из первого canvas-сценария (группа `infrastructure`) → 202, `data.story_id` присутствует
- LS-03: `POST /intake/stories` × 4 — по одному сценарию из каждой группы (`infrastructure`, `environment`, `digital`, `conflict`) → все 202
- LS-04: `GET /tallinn/issues` → 200, `Content-Type: application/json`
- LS-05: `POST /intake/stories` с невалидным payload (пустой `narrative.original_text`) → 422, error envelope корректный
- LS-06: `X-Request-Id` header присутствует в response при intake

**Связь с simulation_runner.py**:  
`simulation_runner.py` — CLI для ручного прогона всех 130 сценариев против любого сервера (prod/staging). Smoke-тест использует тот же `_scenario_to_payload()` и те же данные, но интегрирован в pytest с явными assertions.

**Метрики сложности**: Низкая (httpx + импорт из simulation_runner) / Важность: Критическая

---

### GAP-41-02: Нет теста временного окна кластеризации (PS-03, PS-04)

**Описание**: `test_cluster_cron_job.py` использует `OrchestratorStub` с `sleep(1.2)` — кластеризация подменена заглушкой. Реальный сценарий: stories поступают через intake, cron срабатывает через `CLUSTER_CRON_INTERVAL_S`, `StoryClusterOrchestrator.process_all_pending()` исполняется с реальной БД, issue создаётся в `doge_issues`.

**Целевое решение**:
- `tests/test_cron_clustering_timing_contract.py` (in-memory backend)
- Параметризация: `CLUSTER_CRON_INTERVAL_S=1`, `CLUSTER_MIN_SIZE=1`
- Сценарий: intake двух stories → ждём `1.2 * interval_s` → проверяем `doge_issues` не пуст
- Использует `get_api_dependencies().story_cluster_orchestrator` — реальный orchestrator, не stub
- Cron запускается через ASGI lifespan (TestClient context) — не вручную

**Метрики сложности**: Средняя (требует синхронизации с threading) / Важность: Высокая

**Тесты**:
- CT-01: `CLUSTER_CRON_INTERVAL_S=1` → после `sleep(1.5)` с 2 stories → в `doge_issues` ≥ 1 issue
- CT-02: До истечения interval (sleep=0.3) → `doge_issues` пуст
- CT-03: Cron disabled (`CLUSTER_CRON_ENABLED=false`) → issue не создаётся даже после `sleep(1.5)`

---

### GAP-41-03: Нет теста параллельного intake (PS-11)

**Описание**: Нет ни одного теста с конкурентными запросами. Продакшн-сценарий: 10+ пользователей отправляют intake одновременно — нет race condition в idempotency_keys, нет duplicate stories.

**Целевое решение**:
- `tests/test_concurrent_intake_contract.py`
- `concurrent.futures.ThreadPoolExecutor` с N=5 воркерами, каждый POST `/intake/stories`
- Уникальные `external_user_id` и `idempotency_key` на каждый запрос
- Проверка: ровно N story_ids, все уникальны, нет HTTP ошибок

**Метрики сложности**: Средняя (ThreadPoolExecutor + TestClient thread-safety) / Важность: Средняя

**Тесты**:
- CC-01: 5 параллельных intake → ровно 5 уникальных story_ids
- CC-02: 5 параллельных intake с одинаковым `idempotency-key` → ровно 1 story (idempotency under concurrency)

---

### GAP-41-04: Нет верификации Railway env injection (PS-18)

**Описание**: `conftest.py:_block_dotenv_leakage` автоматически подставляет `DB_BACKEND=in_memory` — это блокирует утечку prod-конфига, но не верифицирует, что конфиг корректно читается из Railway env vars без .env файла.

**Целевое решение**:
- `tests/test_config_env_only_contract.py`
- Запуск `load_app_config()` в изолированном subprocess без `.env` файла
- Параметры передаются только через `env=` аргумент
- Проверяет что все обязательные поля читаются из чистого env, без .env fallback

**Метрики сложности**: Низкая / Важность: Средняя

**Тесты**:
- CE-01: `load_app_config()` с полным env dict (без .env) → возвращает валидный `AppConfig`
- CE-02: `load_app_config()` с отсутствующим обязательным полем → поднимает `ConfigError`
- CE-03: `CLUSTER_CRON_ENABLED=false` читается корректно из env

---

### GAP-41-05: Live Supabase RLS — пропускается в CI (PS-13, PS-25)

**Описание**: `tests/integration/supabase/test_rls_policy_validation.py` требует `SUPABASE_TEST_URL` и пропускается без него. В CI нет Railway-stage для обязательного запуска live-тестов.

**Целевое решение**:
- CI pipeline stage `integration-live`: triggered on merge to `main`, requires `SUPABASE_TEST_URL` GitHub Secret
- Тесты: `test_rls_policy_validation.py`, `test_supabase_live_full_pipeline_roundtrip.py`, `test_supabase_required_columns_ready_live.py`
- Guard: `pytest.mark.live_integration` marker + отдельный pytest command в CI
- `required_columns_ready()` live check: проверяет что все geo и embedding колонки присутствуют в Supabase

**Метрики сложности**: Средняя (CI pipeline + секреты) / Важность: Критическая для prod safety

---

### GAP-41-06: Нет async HTTP клиента для чтения issues после sandbox intake (расширение PS-07..PS-10)

**Описание**: Все тесты `GET /tallinn/issues` используют синхронный `TestClient`. Продакшн SPA-клиент использует `fetch` (async HTTP). Специфика: async-клиент может получить chunked response, иной порядок chunks, connection reuse behavior.

**Источник данных**: те же canvas-сценарии из `tests/sandbox/dogestonia_simulation_canvas_v0_1.json` — после intake нескольких сценариев через `httpx.Client` (синхронно) запускается кластеризация и затем async-чтение результатов.

**Целевое решение**:
- `tests/smoke/test_local_server_async_read.py` с `httpx.AsyncClient` против `LOCAL_SERVER_URL`
- Fixture: предварительно отправляет 5 сценариев из группы `infrastructure` через sync `httpx.Client`, запускает `GET /tallinn/issues` для проверки что issues доступны
- Guard: `pytest.skip` если `LOCAL_SERVER_URL` не задан
- `pytest-asyncio` (проверить наличие в `pyproject.toml`)

**Тесты**:
- AC-01: `GET /tallinn/issues` через `httpx.AsyncClient` → 200 с корректным JSON
- AC-02: `GET /tallinn/issues?status=PUBLISHED` через `httpx.AsyncClient` → список (пустой допустим — главное 200)
- AC-03: 3 параллельных `asyncio.gather` GET запроса → все 200, тела одинаковы

**Метрики сложности**: Низкая (httpx.AsyncClient + pytest-asyncio, сервер тот же что GAP-41-01) / Важность: Средняя

---

## 4. Приоритизированный план реализации

| Приоритет | GAP | Тест-файл | Блокировки |
|-----------|-----|-----------|------------|
| P0 — Critical | GAP-41-01 | `tests/smoke/test_local_server_smoke.py` | Локальный сервер запущен вручную (`LOCAL_SERVER_URL`) |
| P0 — Critical | GAP-41-05 | CI stage `integration-live` | `SUPABASE_TEST_URL` + GitHub secret `SUPABASE_TEST_SERVICE_ROLE_KEY` (runner env: `SUPABASE_TEST_SERVICE_ROLE`) |
| P1 — High | GAP-41-02 | `tests/test_cron_clustering_timing_contract.py` | Thread-safety с TestClient + реальный ASGI lifespan |
| P2 — Medium | GAP-41-03 | `tests/test_concurrent_intake_contract.py` | ThreadPoolExecutor + TestClient thread-safety |
| P2 — Medium | GAP-41-06 | `tests/smoke/test_local_server_async_read.py` | Локальный сервер (тот же что GAP-41-01) + pytest-asyncio |
| P3 — Low | GAP-41-04 | `tests/test_config_env_only_contract.py` | — |

---

## 5. Критерии приемки (AC)

- **AC-41-1**: `tests/smoke/test_local_server_smoke.py` создан; тесты LS-01..LS-06 проходят при запущенном `uvicorn` на `LOCAL_SERVER_URL`; пропускаются (`pytest.skip`) если сервер не запущен
- **AC-41-2**: Cron timing тест создан; CT-01 проходит в < 5s; CT-03 верифицирует что `CLUSTER_CRON_ENABLED=false` предотвращает кластеризацию
- **AC-41-3**: Concurrent intake тест создан; CC-01 и CC-02 стабильно проходят (нет flaky race conditions)
- **AC-41-4**: `tests/smoke/test_local_server_async_read.py` создан; AC-01..AC-03 проходят при запущенном локальном сервере
- **AC-41-5**: CI pipeline имеет отдельный stage `integration-live`; live-тесты обязательны при merge в `main`
- **AC-41-6**: Config env-only тест создан; CE-01..CE-03 проходят без `.env` файла
- **AC-41-7**: Все существующие 412 тестов продолжают проходить (нет регрессий)
- **AC-41-8**: `docs/solution architecture/13-testing-and-quality-architecture.md` обновлён с Layer 6 (Local Real HTTP) и gap-статусом каждого PS-* сценария

---

## 6. Текущее состояние vs целевое — сводная таблица

| Категория | Сейчас | Целевое состояние |
|-----------|--------|-------------------|
| Offline тесты (без сервера) | 412 | ~418 (+6 по GAP-41-02..04) |
| Local server smoke тесты | 0 | 6 LS + 3 AC (GAP-41-01, GAP-41-06) |
| Реальный HTTP-стек покрытие | 0% | 100% через `LOCAL_SERVER_URL` тесты |
| Cron timing (full-stack) | Заглушка | Реальный cron + in-memory pipeline |
| Concurrency | 0 тестов | 2 теста (CC-01, CC-02) |
| Live Supabase (CI) | Skip (opt-in) | Обязательный на merge в `main` |
| RLS policy live check | Skip (opt-in) | Обязательный на merge в `main` |
| Env-only config | Blokdotenv fixture | Isolated subprocess CE-01..CE-03 |
| Продакшн-сценарии покрыты | 15/25 (60%) | 25/25 (100%) |

---

## 7. Зависимости и внешние предусловия

### Для Local Server тестов (GAP-41-01, GAP-41-06)

**Источник данных**: `tests/sandbox/dogestonia_simulation_canvas_v0_1.json` (130 сценариев).  
**Конвертация**: `_scenario_to_payload()` из `tests/simulation_runner.py` — уже существует, импортируется smoke-тестами напрямую.

Перед прогоном smoke (в т.ч. async AC-01..AC-03) установите dev extras (`pytest-asyncio` в `[project.optional-dependencies] dev`):
```bash
# из корня doge-complaints-gateway/
pip install -e ".[dev]"
```

Пользователь запускает сервер вручную перед прогоном тест-слоя:
```bash
# из корня doge-complaints-gateway/
APP_PROFILE=demo DB_BACKEND=in_memory CLUSTER_CRON_ENABLED=false \
  .venv/bin/python -m uvicorn core.api.asgi_app:app --host 127.0.0.1 --port 8000
```
Затем в отдельном терминале:
```bash
LOCAL_SERVER_URL=http://127.0.0.1:8000 .venv/bin/python -m pytest tests/smoke/ -v
```

Без `LOCAL_SERVER_URL` все smoke-тесты пропускаются (`pytest.skip`) — offline suite не ломается.

**Полный ручной прогон всех 130 сценариев** (существующий инструмент):
```bash
GATEWAY_URL=http://127.0.0.1:8000 GATEWAY_API_TOKEN=dev \
  SIMULATION_CANVAS_PATH=tests/sandbox/dogestonia_simulation_canvas_v0_1.json \
  .venv/bin/python tests/simulation_runner.py
```
Smoke-тесты дополняют `simulation_runner.py`: используют те же данные и `_scenario_to_payload()`, но добавляют pytest assertions и интегрируются в CI.

### Live Supabase CI (GAP-41-05)

**GitHub repository secrets** (Settings → Secrets and variables → Actions):

| GitHub Secret | Runner env var (в workflow) | Назначение |
|---------------|----------------------------|------------|
| `SUPABASE_TEST_URL` | `SUPABASE_TEST_URL` | PostgREST base URL тестового проекта |
| `SUPABASE_TEST_SERVICE_ROLE_KEY` | `SUPABASE_TEST_SERVICE_ROLE` | service_role key (тесты читают env `SUPABASE_TEST_SERVICE_ROLE`) |

Workflow: [`.github/workflows/integration-live.yml`](../../.github/workflows/integration-live.yml). Архитектура: [`13-testing-and-quality-architecture.md`](../solution%20architecture/13-testing-and-quality-architecture.md) §6.

### Остальные зависимости

- `pytest-asyncio` — в `pyproject.toml` dev extras; установка: `pip install -e ".[dev]"` (offline CI: `test-offline.yml` уже использует этот шаг)
- `httpx` — уже в зависимостях через FastAPI/TestClient
- `CLUSTER_CRON_INTERVAL_S=1` — только для timing-тестов; в prod: 60–300s
