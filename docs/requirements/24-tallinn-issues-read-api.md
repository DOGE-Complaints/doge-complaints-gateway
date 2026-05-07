# Requirements: Tallinn Issues Read API

Дата: 2026-04-28 (обновлён 2026-04-29)  
Статус: requirements — ready for tasking  
Фокус: чтение уже кластеризованных issues из таблицы через HTTP  
Связано: `docs/analysis/api-demo-tallinn-issues-read-endpoints.md` (исходный анализ)  
Потребитель: `spa-app` в режиме `VITE_LIFE_REALITY_MODE=GFL-DRIVEN`

---

## 1. Контекст и цель

### 1.1 Что уже работает

Stories принимаются через `POST /intake/stories`, кластеризуются, проходят promotion pipeline и сохраняются как issue-проекции в таблицу `spa_issue_projections` через `IssueCreateService.create_issue()`. Все три backend-реализации (in_memory, sqlite, supabase) поддерживают **запись**.

### 1.2 Чего не хватает

HTTP-эндпоинтов для чтения issues — нет ни одного. Нет read-методов в store-классах. SPA не может получить данные с бекенда.

### 1.3 Что должно появиться

```
GET /tallinn/issues                — список кластеризованных issues, фильтры по статусу / типу / меткам
GET /tallinn/issues/{issue_id}     — один issue по ID
```

Оба эндпоинта — **публичные** (без авторизации), читают данные напрямую из таблицы `tallinn_issues_projections`.

---

## 2. DB-слой

### 2.1 Переименование таблицы

Таблица `spa_issue_projections` переименовывается в `tallinn_issues_projections`.

**Почему:** название `spa_issue_projections` — артефакт ранней реализации, отражающий технический слой, а не домен. `tallinn_issues_projections` согласуется с namespace `/tallinn/issues` и отражает назначение: projection кластеризованных issues для Таллинна.

**Почему view не нужен:**

Gateway читает через Python с ключом `service_role`, который обходит RLS на любой таблице. SPA не ходит в Supabase напрямую — только через gateway HTTP API. View давал бы пользу только при прямом JS-клиентском доступе с `anon` ключом, который не предусмотрен в нашей архитектуре. Читаем прямо из `tallinn_issues_projections`.

**Схема таблицы (не изменяется, только имя):**

```sql
CREATE TABLE tallinn_issues_projections (
    issue_id        TEXT PRIMARY KEY,
    status          TEXT NOT NULL,
    payload_json    TEXT NOT NULL,  -- полный JSON от SpaIssueProjection.to_public_dict()
    policy_version  TEXT NOT NULL,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
)
```

В Supabase: `payload_json` — тип `jsonb`. RLS включён, доступ — только `service_role`.

**Supabase migration (rename):**

```sql
-- supabase/migrations/YYYYMMDD_rename_spa_issue_projections.sql
alter table public.spa_issue_projections rename to tallinn_issues_projections;

-- обновить RLS политику
drop policy if exists projections_service_role_all on public.spa_issue_projections;
create policy tallinn_projections_service_role_all
    on public.tallinn_issues_projections
    for all
    to service_role
    using (true)
    with check (true);
```

**Bootstrap (`000_full_init.sql`):** заменить все вхождения `spa_issue_projections` на `tallinn_issues_projections`, включая `CREATE TABLE`, `CREATE INDEX`, `ALTER TABLE ... enable row level security`, `CREATE POLICY`.

**SQLite (`db_sqlite.py` — `ensure_schema()`):** заменить `spa_issue_projections` → `tallinn_issues_projections` в DDL и во всех SQL-запросах (write-методы тоже затрагиваются).

### 2.2 View `issues_dashboard` — zombie, запланировать удаление

`issues_dashboard` существует в Supabase bootstrap (`000_full_init.sql`) и миграции (`20260427_1615_spa_issues_dashboard_view.sql`). Создавался под паттерн "SPA читает Supabase JS client напрямую" — этот паттерн не реализован и не планируется.

**Факты:**
- ни один Python handler его не читает (grep `src/` → 0 результатов)
- единственный потребитель — integration test (`test_spa_projection_supabase_roundtrip.py`)
- содержит дублирующие плоские поля (`title_en`, `type`, ...) + полный `payload_json` — избыточность
- отсутствует в SQLite schema

> ⚠️ `issues_dashboard` — zombie view. Не блокирует реализацию этого требования. Удаляется отдельно.

---

## 3. Python store-слой

### 3.1 Protocol `IssueProjectionReadStore`

Добавить в `src/core/application/issue_create.py` рядом с существующими `IssueProjectionStore`, `IssueStoryLinkStore`:

```python
class IssueProjectionReadStore(Protocol):
    def list_projections(
        self,
        *,
        status: list[str] | None = None,
        issue_type: str | None = None,
        labels: list[str] | None = None,
    ) -> list[dict[str, object]]:
        """Return list of projection payloads matching filters.

        Each item is SpaIssueProjection.to_public_dict() shape.
        No filters → return all. status: OR. labels: OR (any match).
        """

    def get_projection(self, issue_id: str) -> dict[str, object] | None:
        """Return single projection payload by issue_id, or None."""
```

### 3.2 `InMemoryIssueProjectionStore` — добавить методы

Файл: `src/core/infrastructure/repositories.py`

```python
def list_projections(
    self,
    *,
    status: list[str] | None = None,
    issue_type: str | None = None,
    labels: list[str] | None = None,
) -> list[dict[str, object]]:
    assert self._rows is not None
    result = []
    for row in self._rows.values():
        payload = row["payload"]
        if status and row["status"] not in status:
            continue
        if issue_type and payload.get("type") != issue_type:
            continue
        if labels and not any(l in payload.get("labels", []) for l in labels):
            continue
        result.append(dict(payload))
    return result

def get_projection(self, issue_id: str) -> dict[str, object] | None:
    assert self._rows is not None
    row = self._rows.get(issue_id)
    return dict(row["payload"]) if row else None
```

### 3.3 `SqliteIssueProjectionStore` — добавить методы

Файл: `src/core/infrastructure/db_sqlite.py`. Читает напрямую из `tallinn_issues_projections`.

```python
def list_projections(
    self,
    *,
    status: list[str] | None = None,
    issue_type: str | None = None,
    labels: list[str] | None = None,
) -> list[dict[str, object]]:
    query = "SELECT status, payload_json FROM tallinn_issues_projections ORDER BY created_at DESC"
    params: list[str] = []
    if status:
        placeholders = ",".join("?" * len(status))
        query = (
            f"SELECT status, payload_json FROM tallinn_issues_projections "
            f"WHERE status IN ({placeholders}) ORDER BY created_at DESC"
        )
        params = list(status)
    rows = self.db.connection.execute(query, params).fetchall()
    result = []
    for row in rows:
        payload = json.loads(str(row["payload_json"]))
        if issue_type and payload.get("type") != issue_type:
            continue
        if labels and not any(l in payload.get("labels", []) for l in labels):
            continue
        result.append(payload)
    return result

def get_projection(self, issue_id: str) -> dict[str, object] | None:
    row = self.db.connection.execute(
        "SELECT payload_json FROM tallinn_issues_projections WHERE issue_id = ?",
        (issue_id,),
    ).fetchone()
    if row is None:
        return None
    return json.loads(str(row["payload_json"]))
```

> Фильтры `type` и `labels` — post-fetch в Python: SQLite хранит `payload_json` как TEXT, JSON-операторы в SQL недоступны.

### 3.4 `SupabaseIssueProjectionStore` — добавить методы

Файл: `src/core/infrastructure/db_supabase.py`. Читает напрямую из `tallinn_issues_projections`.

```python
def list_projections(
    self,
    *,
    status: list[str] | None = None,
    issue_type: str | None = None,
    labels: list[str] | None = None,
) -> list[dict[str, object]]:
    conditions: list[str] = []
    params: dict[str, object] = {}
    if status:
        conditions.append("status = ANY(%(status)s)")
        params["status"] = list(status)
    if issue_type:
        conditions.append("payload_json->>'type' = %(issue_type)s")
        params["issue_type"] = issue_type
    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    query = f"SELECT status, payload_json FROM tallinn_issues_projections {where} ORDER BY created_at DESC"
    with self.db._connect() as conn, conn.cursor() as cur:
        cur.execute(query, params)
        rows = cur.fetchall()
    result = []
    for row in rows:
        payload: dict[str, object] = row["payload_json"]  # psycopg десериализует jsonb → dict
        if labels and not any(l in payload.get("labels", []) for l in labels):
            continue
        result.append(payload)
    return result

def get_projection(self, issue_id: str) -> dict[str, object] | None:
    with self.db._connect() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT payload_json FROM tallinn_issues_projections WHERE issue_id = %(issue_id)s",
            {"issue_id": issue_id},
        )
        row = cur.fetchone()
    if row is None:
        return None
    return row["payload_json"]
```

> `labels` — post-fetch в Python для унификации с SQLite. Supabase технически позволяет `@>` оператор jsonb, но единообразие важнее оптимизации на текущем масштабе.

---

## 4. API-слой

### 4.1 Handlers

Добавить в `src/core/api/handlers.py`:

```python
def handle_tallinn_issues_list(
    dependencies: ApiDependencies,
    *,
    status: list[str] | None = None,
    issue_type: str | None = None,
    labels: list[str] | None = None,
    trace_id: str | None = None,
) -> dict[str, Any]:
    resolved_trace_id = ensure_trace_id(trace_id)
    try:
        issues = dependencies.issue_projection_read_store.list_projections(
            status=status, issue_type=issue_type, labels=labels
        )
        return build_success_envelope(
            data={"issues": issues}, trace_id=resolved_trace_id
        ).as_dict()
    except Exception as exc:  # noqa: BLE001
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        return envelope.as_dict()


def handle_tallinn_issue_get(
    dependencies: ApiDependencies,
    *,
    issue_id: str,
    trace_id: str | None = None,
) -> tuple[dict[str, Any], int]:
    resolved_trace_id = ensure_trace_id(trace_id)
    try:
        projection = dependencies.issue_projection_read_store.get_projection(issue_id)
        if projection is None:
            return (
                build_error_envelope(
                    ValueError(f"Issue not found: {issue_id}"), trace_id=resolved_trace_id
                ).as_dict(),
                404,
            )
        return (
            build_success_envelope(
                data={"issue": projection}, trace_id=resolved_trace_id
            ).as_dict(),
            200,
        )
    except Exception as exc:  # noqa: BLE001
        envelope = build_error_envelope(exc, trace_id=resolved_trace_id)
        log_error(envelope)
        return envelope.as_dict(), 500
```

### 4.2 Routes — `asgi_app.py`

CORS middleware (добавить **до** регистрации маршрутов):

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # для demo/pilot; в production — конкретный origin
    allow_methods=["GET"],
    allow_headers=["x-trace-id"],
)
```

Обновить `PUBLIC_ROUTES`:

```python
PUBLIC_ROUTES: tuple[str, ...] = (
    "/health",
    "/ready",
    "/demo/auth-page",
    "/intake/stories",
    "/tallinn/issues",           # NEW
)
```

Новые маршруты:

```python
from core.api.handlers import handle_tallinn_issues_list, handle_tallinn_issue_get

@app.get("/tallinn/issues")
async def tallinn_issues_list(
    request: Request,
    status: list[str] | None = Query(default=None),
    type: str | None = Query(default=None),
    labels: list[str] | None = Query(default=None),
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload = handle_tallinn_issues_list(
        deps,
        status=status,
        issue_type=type,      # query param 'type' → внутренний 'issue_type'
        labels=labels,
        trace_id=_read_trace_id(request),
    )
    return JSONResponse(content=payload, status_code=200)


@app.get("/tallinn/issues/{issue_id}")
async def tallinn_issue_get(
    issue_id: str,
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload, status_code = handle_tallinn_issue_get(
        deps,
        issue_id=issue_id,
        trace_id=_read_trace_id(request),
    )
    return JSONResponse(content=payload, status_code=status_code)
```

### 4.3 Query parameter контракт

| Параметр | Тип FastAPI | Повторяется | Пример | Логика |
|----------|-------------|-------------|--------|--------|
| `status` | `list[str]` | да | `?status=NEW&status=VERIFIED` | OR |
| `type`   | `str`       | нет | `?type=complaint` | точное совпадение |
| `labels` | `list[str]` | да | `?labels=bureaucracy&labels=infrastructure` | OR |

Без параметров — возвращает все issues.

### 4.4 Response envelope

**Список (GET /tallinn/issues):**
```json
{
  "trace_id": "uuid",
  "data": {
    "issues": [
      {
        "id": "...", "status": "NEW", "type": "complaint",
        "labels": ["infrastructure"],
        "title": {"et": "...", "ru": "...", "en": "..."},
        "summary": {"et": "...", "ru": "...", "en": "..."},
        "description": {"et": "...", "ru": "...", "en": "..."}
      }
    ]
  }
}
```

**Один issue (GET /tallinn/issues/{id}, 200):**
```json
{
  "trace_id": "uuid",
  "data": { "issue": { "id": "...", ... } }
}
```

**Не найден (404):**
```json
{
  "trace_id": "uuid",
  "error": { "code": "DOMAIN_ERROR", "type": "domain", "message": "Issue not found: ..." }
}
```

---

## 5. Dependencies wiring

### 5.1 `ApiDependencies` — добавить поле

Файл: `src/core/api/dependencies.py`:

```python
from core.application.issue_create import IssueProjectionReadStore

@dataclass
class ApiDependencies:
    # ... существующие поля ...
    issue_projection_read_store: IssueProjectionReadStore
```

### 5.2 `build_api_dependencies` — провести store

Добавить метод `get_issue_projection_store()` в `ServiceFactory` Protocol и `DefaultServiceFactory`:

```python
# в factory.py / ServiceFactory Protocol:
def get_issue_projection_store(self) -> IssueProjectionReadStore: ...

# в service_factory.py / DefaultServiceFactory:
def get_issue_projection_store(self) -> IssueProjectionReadStore:
    return self.issue_projection_store

# в build_api_dependencies():
issue_projection_read_store = service_factory.get_issue_projection_store()
```

---

## 6. Порядок реализации (task sequence)

Каждый шаг компилируется и тестируется независимо:

| # | Задача | Файлы | Проверка |
|---|--------|-------|---------|
| 1 | Rename: `spa_issue_projections` → `tallinn_issues_projections` в bootstrap + SQLite DDL + все write-методы store | `000_full_init.sql`, `db_sqlite.py`, `db_supabase.py`, `repositories.py` | сервис стартует, write-путь (`POST /intake/stories`) работает |
| 2 | Supabase migration: rename таблицы + пересоздать RLS policy | `supabase/migrations/YYYYMMDD_rename_spa_issue_projections.sql` | migration применяется без ошибок |
| 3 | Protocol: добавить `IssueProjectionReadStore` | `issue_create.py` | mypy/pyright не ругается |
| 4 | InMemory store: `list_projections`, `get_projection` | `repositories.py` | unit test: empty → [], after save → item |
| 5 | SQLite store: `list_projections`, `get_projection` | `db_sqlite.py` | unit test с реальным SQLite файлом |
| 6 | Supabase store: `list_projections`, `get_projection` | `db_supabase.py` | integration test (skip без env) |
| 7 | Factory: `get_issue_projection_store()` | `factory.py`, `service_factory.py` | нет ошибок импорта |
| 8 | Dependencies: провести `issue_projection_read_store` | `dependencies.py` | тест `build_api_dependencies()` |
| 9 | Handlers: `handle_tallinn_issues_list`, `handle_tallinn_issue_get` | `handlers.py` | unit test с mock deps |
| 10 | Routes + CORS: зарегистрировать маршруты | `asgi_app.py` | `GET /tallinn/issues` → HTTP 200 |

**Шаг 1 — самый опасный** (rename затрагивает write-путь). Делать в одном PR с шагом 2 миграцией. Smoke test write-пути после каждого backend-перехода.

---

## 7. Acceptance criteria

### AC-1: таблица `tallinn_issues_projections` существует

SQLite:
```python
row = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='tallinn_issues_projections'"
).fetchone()
assert row is not None
```

Supabase:
```sql
SELECT tablename FROM pg_tables WHERE schemaname='public' AND tablename='tallinn_issues_projections';
-- 1 строка
```

### AC-2: write-путь не сломан после rename

```
POST /intake/stories  (с CLUSTER_MIN_SIZE=1)
→ 200 { "story_id": "..." }
# нет ошибок "no such table: spa_issue_projections"
```

### AC-3: GET /tallinn/issues — пустой store

```
GET /tallinn/issues
→ 200 { "data": { "issues": [] }, "trace_id": "..." }
```

### AC-4: GET /tallinn/issues — после intake + promotion

```
POST /intake/stories (с CLUSTER_MIN_SIZE=1)
GET /tallinn/issues
→ 200 { "data": { "issues": [ { "id": "...", "status": "NEW", "type": "...", ... } ] } }
```

Все обязательные поля присутствуют: `id`, `status`, `type`, `labels`, `title`, `summary`, `description`.

### AC-5: фильтр по status

```
GET /tallinn/issues?status=NEW&status=VERIFIED
→ все issues в ответе имеют status IN ["NEW", "VERIFIED"]
```

### AC-6: фильтр по type

```
GET /tallinn/issues?type=complaint
→ все issues в ответе имеют type == "complaint"
```

### AC-7: GET /tallinn/issues/{id} найден

```
GET /tallinn/issues/{existing_id}
→ 200 { "data": { "issue": { "id": "<existing_id>", ... } } }
```

### AC-8: GET /tallinn/issues/{id} не найден

```
GET /tallinn/issues/nonexistent
→ 404 { "error": { "code": "DOMAIN_ERROR", ... } }
```

### AC-9: CORS

```
OPTIONS /tallinn/issues
Origin: http://localhost:5173
→ 200 с Access-Control-Allow-Origin: *
```

---

## 8. Wire format issue payload

Из `SpaIssueProjection.to_public_dict()` (`src/core/projection/dto.py`):

| Поле | Тип | Обязательность |
|------|-----|----------------|
| `id` | `string` | обязательное |
| `status` | `"NEW"\|"VERIFIED"\|"IN_REVIEW"\|"ARCHIVED"` | обязательное |
| `type` | `"complaint"\|"observation"\|"absurdity"\|"system_bug"` | обязательное |
| `labels` | `string[]` | обязательное (может быть `[]`) |
| `title` | `{et, ru, en}` | обязательное |
| `summary` | `{et, ru, en}` | обязательное |
| `description` | `{et, ru, en}` | обязательное |
| `institution` | `string\|null` | опциональное |
| `created_at` | `ISO8601 string\|null` | опциональное |
| `arweave_txid` | `string\|null` | опциональное |
| `image_txid` | `string\|null` | опциональное |
| `image_hash` | `string\|null` | опциональное |

---

## 9. Out of scope

| Что | Почему |
|-----|--------|
| Авторизация на эндпоинтах | публичный read, no auth required |
| Пагинация | не нужна в MVP |
| Полнотекстовый поиск | client-side в SPA |
| `GRANT SELECT to anon` на таблицу | gateway читает через `service_role`, прямой JS-клиентский доступ не предусмотрен |
| Удаление `issues_dashboard` view | отдельный cleanup task, не блокирует этот feature |
| Удаление `spa_issue_projection_embeddings` | отдельный cleanup task (см. `docs/analysis/api-demo-tallinn-issues-read-endpoints.md` раздел 11) |
| Изменение SPA-кода | покрыто `spa-app/docs/analysis/reality-mode-data-source-switch.md` |
