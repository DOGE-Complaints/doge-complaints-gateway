# Requirements: Tallinn Issues API

Дата: 2026-04-28 (обновлён 2026-05-17)  
Статус: requirements — ready for tasking  
Фокус: чтение кластеризованных issues + расширенная фильтрация + ручное создание issue оператором  
Связано: `docs/analysis/api-demo-tallinn-issues-read-endpoints.md` (исходный анализ); поглощает REQ-39 (gap 2026-05-17)  
Потребитель: `spa-app` в режиме `VITE_LIFE_REALITY_MODE=GFL-DRIVEN`; оператор (demo curation)

**Зависимость: REQ-40** (`40-geo-propagation-to-issue-projection.md`) — geo-фильтры (§4.4, AC-14 – AC-19) требуют наличия `geo` в `payload_json`. REQ-40 должен быть выполнен до реализации geo-фильтров.

---

## 1. Контекст и цель

### 1.1 Что уже работает

Stories принимаются через `POST /intake/stories`, кластеризуются, проходят promotion pipeline и сохраняются как issue-проекции в таблицу `spa_issue_projections` через `IssueCreateService.create_issue()`. Все три backend-реализации (in_memory, sqlite, supabase) поддерживают **запись**.

### 1.2 Чего не хватает

HTTP-эндпоинтов для чтения issues — нет ни одного. Нет read-методов в store-классах. SPA не может получить данные с бекенда.

### 1.3 Что должно появиться

```
GET  /tallinn/issues                — список кластеризованных issues, фильтры по статусу / типу / меткам
GET  /tallinn/issues/{issue_id}     — один issue по ID
POST /tallinn/issues                — ручное создание issue оператором (Bearer protected)
```

GET-эндпоинты — **публичные** (без авторизации), читают данные из `doge_issues` (см. §2.1 / REQ-27).  
`POST /tallinn/issues` — **protected** (Bearer token), оператор создаёт issue напрямую без clustering pipeline.

---

## 2. DB-слой

### 2.1 Переименование таблицы

> ⚠️ **Superseded by REQ-27** (`27-doge-issue-domain-rename.md`, 2026-05-05).  
> Финальное имя таблицы — **`doge_issues`**, не `tallinn_issues_projections`.  
> Rationale: `doge_issues` — доменный объект первого класса, не технический слой. Подробнее: REQ-27 §1.  
> Endpoint namespace `/tallinn/issues` **остаётся** — это публичный URL, не имя таблицы (REQ-27 §5).

Таблица `spa_issue_projections` переименована в **`doge_issues`** (реализовано в `20260505_1258_rename_to_doge_issues.sql`).

**Схема таблицы (не изменяется, только имя):**

```sql
CREATE TABLE doge_issues (
    issue_id        TEXT PRIMARY KEY,
    status          TEXT NOT NULL,
    payload_json    TEXT NOT NULL,  -- полный JSON от DOGEIssue.to_public_dict()
    policy_version  TEXT NOT NULL,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
)
```

В Supabase: `payload_json` — тип `jsonb`. RLS включён, доступ — только `service_role`.  
Политика: `doge_issues_service_role_all` (создана в миграции `20260505_1258_rename_to_doge_issues.sql`).

**Статус реализации:** выполнено. SQLite DDL — `db_sqlite.py:ensure_schema()`. Supabase — `/rest/v1/doge_issues`.

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
        # Категориальные фильтры
        status: list[str] | None = None,
        issue_type: str | None = None,
        labels: list[str] | None = None,
        institution: str | None = None,
        # Временны́е фильтры
        created_after: str | None = None,   # ISO8601; включительно
        created_before: str | None = None,  # ISO8601; включительно
        # Geo — пространственный (bbox)
        geo_lat_min: float | None = None,
        geo_lat_max: float | None = None,
        geo_lon_min: float | None = None,
        geo_lon_max: float | None = None,
        # Geo — идентификаторы адреса
        geo_district: list[str] | None = None,
        geo_settlement: list[str] | None = None,
        geo_region: list[str] | None = None,
        geo_country: list[str] | None = None,
        geo_postal_code: list[str] | None = None,
    ) -> list[dict[str, object]]:
        """Return list of projection payloads matching all active filters.

        Each item is DOGEIssue.to_public_dict() shape (REQ-40: includes geo sub-object).
        No filters → return all.
        status / labels / geo_district / geo_settlement / geo_region / geo_country /
        geo_postal_code: OR within each parameter.
        issue_type / institution: exact match.
        bbox (geo_lat_min/max + geo_lon_min/max): AND with each other and with address filters.
        Issues without geo field: excluded when any geo filter is active.
        """

    def get_projection(self, issue_id: str) -> dict[str, object] | None:
        """Return single projection payload by issue_id, or None."""
```

### 3.1.1 Порядок применения фильтров

```
1. status          → SQL WHERE status IN (...)                   — эффективно
2. created_after   → SQL WHERE created_at >= ?                  — лексикографический ISO8601
3. created_before  → SQL WHERE created_at <= ?                  — лексикографический ISO8601
4. Python post-fetch loop (per-item):
   a. issue_type     — payload.get("type") != issue_type
   b. labels         — OR: any(l in payload["labels"] for l in labels)
   c. institution    — payload.get("institution") != institution
   d. geo_district   — OR: normalize_geo_token(payload["geo"]["district"])
   e. geo_settlement — OR: normalize_geo_token
   f. geo_region     — OR: normalize_geo_token
   g. geo_country    — OR: normalize_geo_token
   h. geo_postal_code— OR: normalize_geo_token
   i. bbox           — AND: geo_lat_min ≤ lat ≤ geo_lat_max AND geo_lon_min ≤ lon ≤ geo_lon_max
   j. null-safety    — issue без поля "geo" → исключить при любом активном geo-фильтре
```

### 3.1.2 Нормализация geo-строк

Использовать `normalize_geo_token()` из `src/core/geo/scope.py:15`:

```python
def normalize_geo_token(value: str | None) -> str:
    if value is None:
        return ""
    return "".join(ch for ch in value.strip().lower() if ch.isalnum())
```

Пример: `?geo_district=põhja-tallinn` → `"phjatallinn"` совпадает с `geo.district = "Põhja-Tallinn"` → `"phjatallinn"`.

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

Файл: `src/core/infrastructure/db_sqlite.py`. Читает напрямую из **`doge_issues`** (REQ-27).

> Псевдокод ниже исторический; в runtime заменить `tallinn_issues_projections` → `doge_issues`.

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

Файл: `src/core/infrastructure/db_supabase.py`. Читает напрямую из **`doge_issues`** (REST `/rest/v1/doge_issues`).

> Псевдокод ниже исторический; в runtime заменить `tallinn_issues_projections` → `doge_issues`.

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


def handle_tallinn_issue_create(
    dependencies: ApiDependencies,
    *,
    body: dict[str, Any],
    trace_id: str | None = None,
) -> tuple[dict[str, Any], int]:
    """Manual operator creation. Bearer protected (enforced at route level)."""
    resolved_trace_id = ensure_trace_id(trace_id)
    try:
        cluster_id = body.get("cluster_id", "")
        story_ids = body.get("story_ids", [])
        title = body.get("title", {})
        issue_type = body.get("type", "complaint")
        issue_id = dependencies.issue_create_service.create_manual_issue(
            cluster_id=cluster_id,
            story_ids=story_ids,
            title=title,
            issue_type=issue_type,
        )
        return (
            build_success_envelope(
                data={"issue_id": issue_id}, trace_id=resolved_trace_id
            ).as_dict(),
            201,
        )
    except (KeyError, ValueError) as exc:
        return build_error_envelope(exc, trace_id=resolved_trace_id).as_dict(), 400
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
    allow_methods=["GET", "POST"],
    allow_headers=["x-trace-id", "authorization"],
)
```

Обновить `PUBLIC_ROUTES`:

```python
PUBLIC_ROUTES: tuple[str, ...] = (
    "/health",
    "/ready",
    "/demo/auth-page",
    "/intake/stories",
    "/tallinn/issues",           # NEW — GET только; POST через require_service_auth
)
```

Новые маршруты:

```python
from core.api.handlers import handle_tallinn_issues_list, handle_tallinn_issue_get, handle_tallinn_issue_create

@app.get("/tallinn/issues")
async def tallinn_issues_list(
    request: Request,
    # категориальные
    status: list[str] | None = Query(default=None),
    type: str | None = Query(default=None),
    labels: list[str] | None = Query(default=None),
    institution: str | None = Query(default=None),
    # временны́е
    created_after: str | None = Query(default=None),
    created_before: str | None = Query(default=None),
    # geo — bbox
    geo_lat_min: float | None = Query(default=None),
    geo_lat_max: float | None = Query(default=None),
    geo_lon_min: float | None = Query(default=None),
    geo_lon_max: float | None = Query(default=None),
    # geo — address
    geo_district: list[str] | None = Query(default=None),
    geo_settlement: list[str] | None = Query(default=None),
    geo_region: list[str] | None = Query(default=None),
    geo_country: list[str] | None = Query(default=None),
    geo_postal_code: list[str] | None = Query(default=None),
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload = handle_tallinn_issues_list(
        deps,
        status=status,
        issue_type=type,          # query param 'type' → внутренний 'issue_type'
        labels=labels,
        institution=institution,
        created_after=created_after,
        created_before=created_before,
        geo_lat_min=geo_lat_min,
        geo_lat_max=geo_lat_max,
        geo_lon_min=geo_lon_min,
        geo_lon_max=geo_lon_max,
        geo_district=geo_district,
        geo_settlement=geo_settlement,
        geo_region=geo_region,
        geo_country=geo_country,
        geo_postal_code=geo_postal_code,
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


@app.post("/tallinn/issues", dependencies=[Depends(require_service_auth)])
async def tallinn_issue_create(
    request: Request,
    body: dict[str, Any],
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload, status_code = handle_tallinn_issue_create(
        deps,
        body=body,
        trace_id=_read_trace_id(request),
    )
    return JSONResponse(content=payload, status_code=status_code)
```

### 4.3 Query parameter контракт

#### Категориальные фильтры

| Параметр | Тип FastAPI | Повторяется | Пример | Логика |
|----------|-------------|-------------|--------|--------|
| `status` | `list[str]` | да | `?status=NEW&status=PUBLISHED` | OR |
| `type`   | `str`       | нет | `?type=INCIDENT` | exact match |
| `labels` | `list[str]` | да | `?labels=infrastructure&labels=waste` | OR |
| `institution` | `str` | нет | `?institution=Tallinna Kommunaalamet` | exact match, case-sensitive |

#### Временны́е фильтры

| Параметр | Тип FastAPI | Пример | Логика |
|----------|-------------|--------|--------|
| `created_after`  | `str` | `?created_after=2026-01-01T00:00:00Z` | `created_at >= value` (ISO8601 лексикографически) |
| `created_before` | `str` | `?created_before=2026-12-31T23:59:59Z` | `created_at <= value` |

#### Geo-фильтры — режим A: пространственный (bbox)

Прямоугольник координат WGS84 — аналог «зума» Google Maps.

| Параметр | Тип FastAPI | Пример | Логика |
|----------|-------------|--------|--------|
| `geo_lat_min` | `float` | `?geo_lat_min=59.43` | нижняя граница широты (south) |
| `geo_lat_max` | `float` | `?geo_lat_max=59.46` | верхняя граница широты (north) |
| `geo_lon_min` | `float` | `?geo_lon_min=24.72` | левая граница долготы (west) |
| `geo_lon_max` | `float` | `?geo_lon_max=24.77` | правая граница долготы (east) |

Условие: `geo_lat_min ≤ issue.geo.lat ≤ geo_lat_max AND geo_lon_min ≤ issue.geo.lon ≤ geo_lon_max`

#### Geo-фильтры — режим B: идентификаторы адреса

Фильтрация по admin-иерархии из `StoryGeoSnapshot` (REQ-40). Нормализация через `normalize_geo_token()`.

| Параметр | Тип FastAPI | Повторяется | Соответствует | Логика |
|----------|-------------|-------------|---------------|--------|
| `geo_district`    | `list[str]` | да | `geo.district`    | OR |
| `geo_settlement`  | `list[str]` | да | `geo.settlement`  | OR |
| `geo_region`      | `list[str]` | да | `geo.region`      | OR |
| `geo_country`     | `list[str]` | да | `geo.country`     | OR |
| `geo_postal_code` | `list[str]` | да | `geo.postal_code` (Phase 3) | OR |

#### Комбинирование и null-safety

- Все указанные параметры — AND между группами (режим A AND режим B AND категориальные AND временны́е).
- Issues без поля `"geo"` в payload — **исключаются** при любом активном geo-фильтре.
- Пустое значение (`?geo_district=`) — игнорируется как отсутствующий параметр.
- Без параметров — возвращает все issues.

**Полный пример запроса:**
```
GET /tallinn/issues
  ?status=NEW&status=PUBLISHED
  &type=INCIDENT
  &labels=infrastructure&labels=waste
  &institution=Tallinna%20Kommunaalamet
  &created_after=2026-01-01T00:00:00Z
  &created_before=2026-12-31T23:59:59Z
  &geo_lat_min=59.43&geo_lat_max=59.46
  &geo_lon_min=24.72&geo_lon_max=24.77
  &geo_district=Kalamaja
  &geo_settlement=Tallinn
  &geo_region=Harju%20maakond
  &geo_country=EE
  &geo_postal_code=10411
```

### 4.4 Response envelope

**Список (GET /tallinn/issues):**
```json
{
  "trace_id": "uuid",
  "data": {
    "issues": [
      {
        "id": "issue:abc123",
        "status": "PUBLISHED",
        "type": "INCIDENT",
        "labels": ["infrastructure", "safety"],
        "title": {"et": "Katki tänav", "ru": "Сломанная дорога", "en": "Broken road"},
        "summary": {"et": "...", "ru": "...", "en": "..."},
        "description": {"et": "...", "ru": "...", "en": "..."},
        "institution": null,
        "created_at": "2026-05-17T10:00:00Z",
        "geo": {
          "lat": 59.4372,
          "lon": 24.7453,
          "label": "Kalamaja, Tallinn",
          "district": "Põhja-Tallinn",
          "settlement": "Tallinn",
          "region": "Harju maakond",
          "country": "EE"
        }
      },
      {
        "id": "issue:xyz999",
        "status": "NEW",
        "type": "IMPROVEMENT",
        "labels": ["waste"],
        "title": {"et": "...", "ru": "...", "en": "..."},
        "summary": {"et": "...", "ru": "...", "en": "..."},
        "description": {"et": "...", "ru": "...", "en": "..."}
        // поле "geo" отсутствует — story была без location_query
      }
    ]
  }
}
```

> `"geo"` присутствует только если у доминантной истории кластера был `location_query` (REQ-40). Поле отсутствует — не `null`. SPA проверяет: `if (issue.geo)`.


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

**Создан POST /tallinn/issues (201):**
```json
{
  "trace_id": "uuid",
  "data": { "issue_id": "issue:..." }
}
```

**POST без Bearer (401):**
```json
{ "detail": "Unauthorized" }
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
| 1 | Rename: `spa_issue_projections` → **`doge_issues`** (REQ-27 supersedes промежуточное имя `tallinn_issues_projections`) | `20260505_1258_rename_to_doge_issues.sql`, `db_sqlite.py`, `db_supabase.py`, `repositories.py` | AC-1, AC-2; write-путь (`POST /intake/stories`) |
| 2 | Supabase migration: rename + RLS policy для `doge_issues` | `supabase/migrations/20260505_1258_rename_to_doge_issues.sql` | migration применяется без ошибок |
| 3 | Protocol: добавить `IssueProjectionReadStore` | `issue_create.py` | mypy/pyright не ругается |
| 4 | InMemory store: `list_projections`, `get_projection` | `repositories.py` | unit test: empty → [], after save → item |
| 5 | SQLite store: `list_projections`, `get_projection` | `db_sqlite.py` | unit test с реальным SQLite файлом |
| 6 | Supabase store: `list_projections`, `get_projection` | `db_supabase.py` | integration test (skip без env) |
| 7 | Factory: `get_issue_projection_store()` | `factory.py`, `service_factory.py` | нет ошибок импорта |
| 8 | Dependencies: провести `issue_projection_read_store` | `dependencies.py` | тест `build_api_dependencies()` |
| 9 | Handlers: `handle_tallinn_issues_list`, `handle_tallinn_issue_get` | `handlers.py` | unit test с mock deps |
| 10 | Routes + CORS: зарегистрировать GET маршруты | `asgi_app.py` | `GET /tallinn/issues` → HTTP 200 |
| 11 | `IssueCreateService.create_manual_issue()` + `POST /tallinn/issues` route (Bearer) | `issue_create.py`, `handlers.py`, `asgi_app.py` | POST без Bearer → 401; POST с Bearer + payload → 201 |
| 12 | OpenAPI spec: добавить все три эндпоинта | `docs/runtime-docs/api-reference/openapi.yaml` | spec валидируется |
| **Phase 2: Geo filters (требует REQ-40)** | | | |
| 13 | `IssueProjectionReadStore` Protocol — расширить сигнатуру (все geo + time параметры) | `issue_create.py` | mypy не ругается |
| 14 | InMemory store: `list_projections()` — добавить все фильтры (§3.1.1) | `repositories.py` | unit tests geo-фильтров |
| 15 | SQLite store: то же | `db_sqlite.py` | unit tests |
| 16 | Supabase store: то же | `db_supabase.py` | integration test (skip без env) |
| 17 | Handler `handle_tallinn_issues_list()` — принять все параметры | `handlers.py` | |
| 18 | Route `GET /tallinn/issues` — добавить все Query параметры | `asgi_app.py` | `?geo_lat_min=59.43&geo_lat_max=59.46&...` работает |

**Шаг 1 — самый опасный** (rename затрагивает write-путь). Делать в одном PR с шагом 2 миграцией. Smoke test write-пути после каждого backend-перехода.

**Phase 2 (шаги 13–18) начинать только после выполнения REQ-40** (geo в payload).

---

## 7. Acceptance criteria

### AC-1: таблица `doge_issues` существует

> ℹ️ Имя таблицы изменено per REQ-27 (`doge_issues`, не `tallinn_issues_projections`).

SQLite:
```python
row = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='doge_issues'"
).fetchone()
assert row is not None
```

Supabase:
```sql
SELECT tablename FROM pg_tables WHERE schemaname='public' AND tablename='doge_issues';
-- 1 строка
```

### AC-2: write-путь работает с таблицей `doge_issues`

```
POST /intake/stories  (с CLUSTER_MIN_SIZE=1)
→ 202 { "data": { "story_id": "..." } }
# запись появляется в doge_issues; нет ошибок "no such table"
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

### AC-10: POST /tallinn/issues без Bearer → 401

```
POST /tallinn/issues
Content-Type: application/json
(без Authorization header)
→ 401
```

### AC-11: POST /tallinn/issues с Bearer + валидным payload → 201 + issue_id

```json
POST /tallinn/issues
Authorization: Bearer <token>
{
  "cluster_id": "cluster:test-1",
  "story_ids": ["story-a", "story-b"],
  "title": {"et": "Katki tänav", "ru": "Сломанная дорога", "en": "Broken road"},
  "type": "complaint"
}
→ 201 { "data": { "issue_id": "issue:..." }, "trace_id": "..." }
```

### AC-12: Issue созданный через POST появляется в GET /tallinn/issues

```
POST /tallinn/issues (Bearer, valid payload) → issue_id
GET /tallinn/issues
→ issue с этим issue_id присутствует в data.issues
```

### AC-13: OpenAPI spec содержит все три эндпоинта

```
docs/runtime-docs/api-reference/openapi.yaml
→ paths содержит /tallinn/issues (GET), /tallinn/issues/{issue_id} (GET), /tallinn/issues (POST)
→ POST помечен securitySchemes: Bearer
```

### AC-14: Bbox-фильтр возвращает только issues в зоне (требует REQ-40)

```
GET /tallinn/issues?geo_lat_min=59.43&geo_lat_max=59.46&geo_lon_min=24.72&geo_lon_max=24.77
→ все issues в ответе имеют geo.lat ∈ [59.43, 59.46] и geo.lon ∈ [24.72, 24.77]
→ issues вне bbox не возвращаются
→ issues без поля "geo" не возвращаются
```

### AC-15: Issues без geo исключаются при активном geo-фильтре (требует REQ-40)

```
GET /tallinn/issues?geo_district=Kesklinn
→ ответ не содержит issues без поля "geo"
```

### AC-16: Address-фильтр по district — case-insensitive нормализованный (требует REQ-40)

```
GET /tallinn/issues?geo_district=põhja-tallinn
→ возвращает issues с geo.district == "Põhja-Tallinn"
   (normalize_geo_token("põhja-tallinn") == normalize_geo_token("Põhja-Tallinn"))
```

### AC-17: Множественные значения geo_district — OR (требует REQ-40)

```
GET /tallinn/issues?geo_district=Kalamaja&geo_district=Kesklinn
→ issues из обоих районов в ответе
```

### AC-18: Комбинирование bbox + address — AND (требует REQ-40)

```
GET /tallinn/issues?geo_lat_min=59.43&geo_lat_max=59.46&geo_lon_min=24.72&geo_lon_max=24.77&geo_district=Kesklinn
→ только issues удовлетворяющие ОБОИМ условиям
```

### AC-19: created_after / created_before

```
GET /tallinn/issues?created_after=2026-05-01T00:00:00Z&created_before=2026-05-31T23:59:59Z
→ только issues с created_at в мае 2026
→ issues до и после — не возвращаются
```

### AC-20: Пустые geo-параметры игнорируются

```
GET /tallinn/issues?geo_district=
→ эквивалентно GET /tallinn/issues (без фильтра)
→ возвращает все issues
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
| Авторизация на GET-эндпоинтах | публичный read, no auth required (POST защищён отдельно через Bearer) |
| Пагинация | не нужна в MVP |
| Полнотекстовый поиск | client-side в SPA |
| `GRANT SELECT to anon` на таблицу | gateway читает через `service_role`, прямой JS-клиентский доступ не предусмотрен |
| Удаление `issues_dashboard` view | отдельный cleanup task, не блокирует этот feature |
| Удаление `spa_issue_projection_embeddings` | отдельный cleanup task (см. `docs/analysis/api-demo-tallinn-issues-read-endpoints.md` раздел 11) |
| Изменение SPA-кода | покрыто `spa-app/docs/analysis/reality-mode-data-source-switch.md` |
| `POST /issues` (путь без `/tallinn/`) | REQ-39 использовал этот путь с Bearer — конфликт с namespace; canonical путь — `/tallinn/issues` |
| Geo propagation pipeline | REQ-40 (`40-geo-propagation-to-issue-projection.md`) |
| Пространственный SQL-индекс (PostGIS, R-tree) | не нужен при demo-масштабе |
| Centroid geo по всем story кластера | Phase 2 post-demo (в REQ-40 §2) |
| `geo_postal_code` наполнение данными | Phase 3 post-demo (в REQ-40 §6) |
| GeoJSON / Polygon boundaries | beyond MVP |
