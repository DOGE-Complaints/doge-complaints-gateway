# 32. API Security: Rate Limiting и Production Token

> **Назначение документа.** Спецификация требований к защите intake API от злоупотреблений и замены demo-токена на production-grade аутентификацию. Документ написан по методологии analysis.mdc — каждое утверждение верифицировано по фактическому состоянию кода.
>
> **Связь с другими документами:**
> - MVP-аудит (`docs/mvp-readiness-tallinn-audit.md`) P0-T5, P0-T6 — этот документ их специфицирует
> - req19 (`19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md`) — контракт intake API

---

## 1. Текущее состояние кода (аудит 2026-05-07)

### 1.1 Аутентификация

`src/core/api/security.py` реализует `ServiceTokenAuth` — service-to-service токен:

```python
# security.py:16-62
def extract_service_token(headers: Mapping[str, str]) -> str | None:
    auth = h.get("authorization")
    if auth and auth.lower().startswith("bearer "):
        return auth[7:].strip()
    return h.get("x-service-token")

def require(self, headers: Mapping[str, str]) -> None:
    got = extract_service_token(headers)
    if not got:
        raise UnauthorizedError("Missing service API token.")
    if not secrets.compare_digest(got, self._expected):  # timing-safe ✅
        raise UnauthorizedError("Invalid service API token.")
```

`secrets.compare_digest` — timing-safe сравнение, это правильно.

Токен читается из env: `src/core/config/schema.py:407-410`:

```python
service_api_token = _get_value(source, "SERVICE_API_TOKEN")
if profile is DeploymentProfile.PILOT and service_api_token is None:
    raise ConfigError("SERVICE_API_TOKEN is required for APP_PROFILE='pilot'...")
```

В `APP_PROFILE=demo` (`doge-complaints-gateway/.env:1`) — токен не обязателен (нет строгой проверки). Текущее значение:

```
SERVICE_API_TOKEN=111.444.555.888.555.444.111-Tallinn-demo-token
```

Формат предсказуем: структура читаема, не криптографически случайная.

### 1.2 Rate limiting: отсутствует

`src/core/api/handlers.py` — grep по "rate_limit", "throttle", "slowapi", "limit" возвращает ноль совпадений. Никакого rate limiting нет ни в middleware, ни в endpoint-декораторах.

Зарегистрированные маршруты (`src/core/api/asgi_app.py`):
```
POST /intake/stories    ← единственный mutable endpoint, без rate limit
```

### 1.3 Deployment profile

`.env:1`:
```
APP_PROFILE=demo
```

В `demo` профиле `SERVICE_API_TOKEN` не обязателен. Это означает, что если токен из `.env` убрать — сервис продолжит работать без аутентификации.

### 1.4 Риск: манипуляция кластерами через flood

Без rate limiting любой обладатель токена может подать произвольное количество stories с одинаковыми canonical_labels. При `CLUSTER_MIN_SIZE=1` и `min_stories=2` в `PromotionGatePolicy` — двух историй достаточно для создания issue (score=60 при threshold=60). Это позволяет создавать false issues в любом кластере за секунды.

---

## 2. Требования

### 2.1 Production-grade Service Token (P0)

#### 2.1.1 Смена токена

Текущий `111.444.555.888.555.444.111-Tallinn-demo-token` — **не использовать в production**. Заменить на криптографически случайный токен.

Генерация рекомендуемым способом:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(48))"
# пример вывода: "dT7xKq2mNpL8vFhE3wRz5yJbCu1aQiXo9sGnYkPwVlMjHtAeUfBc6D"
```

48 байт (64 символа в base64url) — 384 бит энтропии. Неугадываемо.

#### 2.1.2 Где хранить

| Среда | Хранение | Запрещено |
|-------|----------|-----------|
| Production | Secret manager (Supabase vault, env injection в CI/CD) | Хардкод в `.env` в репо |
| Development | `.env.local` (в `.gitignore`) | `.env` в git |
| Demo/staging | Отдельный короткоживущий токен, ротируется перед каждым мероприятием | Единый токен для всех стендов |

**Немедленное действие:** убрать `SERVICE_API_TOKEN` из `.env` в репозитории. Добавить `.env.example` с placeholder:

```bash
# .env.example
SERVICE_API_TOKEN=replace_with_cryptographically_random_token_from_secret_manager
```

#### 2.1.3 APP_PROFILE для production

Сменить `APP_PROFILE=demo` → `APP_PROFILE=pilot` в production `.env`. В `pilot` режиме `SERVICE_API_TOKEN` обязателен (`schema.py:408-410`), сервис не запустится без него.

### 2.2 Rate Limiting на POST /intake/stories (P0)

#### 2.2.1 Целевые пороги

| Метрика | Значение | Обоснование |
|---------|----------|-------------|
| Per user_id (submitter_external_user_id) | 10 stories / 10 min | Один гражданин не может подавать flood |
| Per IP (за NGINX/proxy) | 30 requests / min | Защита от boto-атак |
| Global burst | 100 stories / min | Защита инфраструктуры |

Значения конфигурируемы через env vars: `RATE_LIMIT_PER_USER`, `RATE_LIMIT_PER_IP`, `RATE_LIMIT_GLOBAL`.

#### 2.2.2 Реализация: FastAPI middleware

Рекомендуемый подход — `slowapi` (обёртка над `limits` для FastAPI/Starlette):

```python
# src/core/api/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# В asgi_app.py:
from slowapi.middleware import SlowAPIMiddleware
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# В handlers.py:
@limiter.limit("10/10minutes", key_func=lambda req: _get_submitter_id(req))
@app.post("/intake/stories")
async def intake_story(request: Request, ...):
    ...
```

#### 2.2.3 Rate limit response

При превышении — `429 Too Many Requests`:

```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many submissions. Please wait before submitting again.",
  "retry_after_seconds": 120
}
```

`Retry-After` header обязателен.

#### 2.2.4 Rate limit для идентификации по user_id

`submitter_external_user_id` приходит в `StoryIntakeRequest`. Использовать его как ключ rate limit если присутствует, иначе — IP:

```python
def _get_rate_key(request: Request) -> str:
    body = request.state.parsed_body  # если доступно до rate check
    if hasattr(body, "submitter_external_user_id"):
        return f"user:{body.submitter_external_user_id}"
    return f"ip:{get_remote_address(request)}"
```

### 2.3 Переключение на APP_PROFILE=pilot (P1)

Смена профиля влечёт:
- `SERVICE_API_TOKEN` становится обязательным
- Сервис не запустится без токена (fail-fast на старте)
- Строгая проверка всех required env vars

**Что нужно проверить перед переключением:**
1. Все env vars, обязательные в `pilot` — присутствуют в secret manager
2. Supabase URL + keys настроены (не demo SQLite)
3. `CLUSTER_ACTIVE_LENSES` переключен на civic (из req30 §13.5)

### 2.4 Audit logging для security events (P1)

Текущее состояние: `handlers.py` логирует `log_api_event` для intake — частично. Security events не структурированы отдельно.

Добавить structured logging для:

```python
# При 401/403:
logger.warning("api.auth_failure", extra={"ip": ..., "endpoint": ..., "reason": ...})

# При 429:
logger.warning("api.rate_limited", extra={"key": ..., "endpoint": ..., "limit": ...})

# При успешном intake:
# уже есть через log_api_event — ✅
```

---

## 3. Acceptance Criteria

**AC-32-1 — Token security:**
`SERVICE_API_TOKEN` в `.env` заменён на placeholder. Реальный токен длиной ≥ 32 байт случайной энтропии, хранится вне репозитория.

**AC-32-2 — APP_PROFILE:**
`APP_PROFILE=pilot` в production `.env`. Запуск без `SERVICE_API_TOKEN` завершается с `ConfigError`.

**AC-32-3 — Rate limiting активен:**
11-й `POST /intake/stories` от одного submitter_id в пределах 10 минут возвращает `429` с `Retry-After` header.

**AC-32-4 — Rate limit response format:**
429 response содержит JSON с `error="rate_limit_exceeded"` и `retry_after_seconds`.

**AC-32-5 — Legitimate traffic unaffected:**
1 submission per minute от уникального submitter_id проходит нормально.

---

## 4. Файлы, требующие изменений

| Файл | Изменение |
|------|-----------|
| `.env` | Убрать реальный токен, заменить placeholder; `APP_PROFILE=pilot` |
| `.env.example` (новый) | Шаблон с документированными env vars без реальных значений |
| `src/core/api/rate_limit.py` (новый) | `Limiter` конфигурация, `_get_rate_key` |
| `src/core/api/asgi_app.py` | Подключить `SlowAPIMiddleware`, добавить state.limiter |
| `src/core/api/handlers.py` | Декораторы `@limiter.limit(...)` на `POST /intake/stories`; security event logging |
| `src/core/config/schema.py` | Env vars `RATE_LIMIT_PER_USER`, `RATE_LIMIT_PER_IP` (опционально) |
| `pyproject.toml` / `requirements.txt` | Добавить `slowapi` зависимость |

---

## 5. Что остаётся за рамками этого документа

- User-level authentication (GPT/IdP) — сервис намеренно не верифицирует user identity, только service-to-service (security.py:34)
- DDoS protection на инфраструктурном уровне (Cloudflare, NGINX) — OPS задача
- JWT / OAuth для citizen-facing API — пост-MVP
- Secrets rotation policy — OPS/DevOps задача

*Методология: analysis.mdc — все утверждения верифицированы по файлам кода.*
