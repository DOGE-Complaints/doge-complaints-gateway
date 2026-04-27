# Operations Playbook (deploy + env + keys)

## Контекст и управленческий вопрос

Ключевой вопрос:  
**как запускать текущий runtime предсказуемо и безопасно, и какие решения принимать при инцидентах до появления real DB/chain интеграций?**

## Run now (current runtime)

### Boundary contract (API vs demo static)

- API runtime boundary обслуживается через `FastAPI` entrypoint `src/core/api/asgi_app.py`.
- Demo static boundary (`demo/auth-page`) публикуется отдельными static routes:
  - `GET /demo/auth-page`
  - `GET /demo/auth-page/styles.css`
- Текущий operating mode: **combined delivery в одном ASGI процессе (API + demo static)**.
- Target mode (planned): split delivery (отдельный frontend/static host + API runtime).

### 1) Bootstrap environment (обязательный минимум)

Для текущего `src/core` baseline используются:

- `API_BASE_URL` (required)
- `APP_PROFILE` (`demo`/`pilot`, default `demo`)
- `REQUEST_TIMEOUT_S` (default `15`)
- `LOG_LEVEL` (default `INFO`)
- `FF_WALLET_ADAPTER`
- `FF_BLOCKCHAIN_ADAPTER`
- `FF_TOKENIZATION_PIPELINE`
- `SERVICE_API_TOKEN` (обязателен для strict-protected режима)

Источники: `src/core/config/schema.py`, `src/core/api/security.py`, `src/core/infrastructure/providers.py`.

### 2) Current secrets posture

- `SERVICE_API_TOKEN` хранить в secret storage/CI variables, не в репозитории.
- Запуск auth-disabled режима допустим только в контролируемом demo/non-production контуре.
- В rollout checklist явно фиксировать факт `auth enabled/disabled`.

### 3) Как включить strict Bearer gate

1. Выставить `SERVICE_API_TOKEN=<strong-secret>`.
2. Передавать token через:
   - `Authorization: Bearer <strong-secret>`
   - или `X-Service-Token: <strong-secret>`
3. Подтвердить проверкой:
   - `python3 -m pytest tests/test_api_security_and_ops.py tests/test_error_envelope_contract.py -q`

### 4) Smoke checks для регрессионного контроля

Текущие operation handlers (`src/core/api/handlers.py`):

- `handle_health` → `GET /health`
- `handle_readiness` → `GET /ready`
- `handle_protected_status` → `GET /protected/status`
- `handle_metrics` → `GET /metrics`
- `handle_story_intake` → `POST /intake/stories`

Readiness semantics:

- `GET /ready` возвращает `data.status` (`ready`/`degraded`)
- дополнительно возвращает `data.db`:
  - `backend`
  - `ready`
  - `checks` (словари probe-флагов)

Рекомендуемый smoke/regression набор:

- `python3 -m pytest tests/test_bootstrap_smoke.py tests/test_api_security_and_ops.py tests/test_http_transport_smoke.py tests/test_http_intake_endpoint.py tests/test_e2e_story_cluster_issue_pipeline.py tests/test_trace_propagation.py -q`

### 5) Incident classes и тактика реакции

#### A) Auth incidents

- Симптомы: `UNAUTHORIZED`, рост `auth_failures`.
- Первые проверки:
  - задан ли `SERVICE_API_TOKEN`,
  - совпадает ли значение с вызывающей стороной,
  - корректен ли заголовок Bearer/X-Service-Token.

#### B) Adapter incidents (demo/pilot stubs)

- Симптомы: непредсказуемость интеграционных вызовов на adapter surfaces.
- Действия:
  - сверить `adapter_runtime_flags(config)` в `src/core/adapters/registry.py`,
  - при необходимости вернуть `APP_PROFILE=demo`.

#### C) Geo degradation

- Симптомы: рост `resolve_misses` / `intake_degraded_geo`.
- Действия:
  - проверить retry/callback behavior (`src/core/geo/chain.py`),
  - оценить cache/provider counters (`src/core/geo/metrics.py`).

### 6) Rollback decision baseline (current)

- Если проблема в auth конфигурации — rollback через восстановление корректного секрета и повтор smoke checks.
- Если проблема в profile/flags — rollback до ранее стабильного профиля (`demo`) и базовых defaults.
- Если проблема в geo/adapters — переход в degraded runtime mode с документированным ограничением функционала.

## After DB/Arweave integration (future extensions)

### DB extension runbook (planned)

- Ввести DB connection contract в `AppConfig`.
- Добавить preflight checks:
  - connectivity,
  - migration version compatibility.
- Ввести rollback для migration wave (backup/restore или controlled down migrations).

### Arweave extension runbook (planned)

- Ввести chain-specific env/secrets и key lifecycle policy.
- Добавить lifecycle monitoring:
  - sign,
  - broadcast,
  - finality reconciliation.
- Подготовить emergency switch обратно на stub adapters.

## Gaps / risks

- Нет отдельного deployment playbook для split delivery (API и static как независимые сервисы).
- Нет formalized escalation matrix (SRE/on-call ownership).
- Secret rotation и key audit trails не оформлены как отдельный operational standard.
