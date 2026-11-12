# 04. Supabase Persistence Layer

## Концепция

Persistence через Supabase реализована без Supabase SDK. Используется прямой HTTP клиент (`httpx`) к PostgREST REST API — стандартному API, которое Supabase предоставляет для всех таблиц.

Почему без SDK: меньше зависимостей, полный контроль над запросами, легко тестировать.

**PostgREST pattern:** каждая таблица доступна как REST endpoint `/rest/v1/<table_name>`. CRUD операции через HTTP verbs: GET (select), POST (insert/upsert), PATCH (update), DELETE.

## Реализация в проекте

**Файл:** `src/core/infrastructure/db_supabase.py`

### `SupabaseDatabase` — HTTP клиент

```python
@dataclass(frozen=True)
class SupabaseDatabase:
    base_url: str          # https://<ref>.supabase.co
    service_role_key: str  # service_role key (не anon key!)
    timeout_s: float = 15.0

    @classmethod
    def from_http(cls, supabase_url: str, service_role_key: str, timeout_s: float = 15.0) -> SupabaseDatabase:
        # валидация URL и key
        return cls(base_url=supabase_url.rstrip("/"), ...)
```

### Auth headers

Каждый запрос несёт два заголовка с одним и тем же service role key:

```python
def _headers(self, *, prefer: str | None = None) -> dict[str, str]:
    return {
        "apikey": self.service_role_key,
        "Authorization": f"Bearer {self.service_role_key}",
        "Content-Type": "application/json",
        **({"Prefer": prefer} if prefer else {}),
    }
```

`apikey` требует PostgREST для идентификации. `Authorization: Bearer` требует RLS policies.

Используй `service_role` key (не `anon`) — service role bypasses RLS и нужен для серверных операций.

### Центральный HTTP primitiv

```python
def _request(self, *, method, path, params=None, json_body=None, prefer=None) -> Any:
    with httpx.Client(timeout=self.timeout_s) as client:
        response = client.request(
            method=method,
            url=f"{self.base_url}{path}",
            headers=self._headers(prefer=prefer),
            params=params,
            json=json_body,
        )
    response.raise_for_status()
    return response.json() if response.text.strip() else None
```

При ошибке логирует status_code и первые 300 символов body, затем пробрасывает исключение.

### CRUD паттерны

**INSERT / UPSERT:**
```python
self._request(
    method="POST",
    path="/rest/v1/stories",
    json_body={"story_id": record.story_id, ...},
    prefer="resolution=merge-duplicates",  # ← upsert по PK
)
```

**SELECT:**
```python
rows = self._request(
    method="GET",
    path="/rest/v1/stories",
    params={"story_id": f"eq.{story_id}", "limit": "1"},
)
return _story_from_row(rows[0]) if rows else None
```

**UPDATE:**
```python
self._request(
    method="PATCH",
    path="/rest/v1/stories",
    params={"story_id": f"eq.{story_id}"},
    json_body={"lifecycle_status": status.value},
)
```

PostgREST фильтры: `eq.`, `gt.`, `lt.`, `gte.`, `lte.`, `in.(v1,v2)`, `is.null`.

### Таблицы (полный список)

Проверяется в `required_tables_ready()`:

| Таблица | Назначение |
|---------|-----------|
| `stories` | Все поля StoryRecord |
| `idempotency_keys` | Дедупликация intake запросов |
| `story_embeddings` | Векторные эмбеддинги историй |
| `doge_issues` | DOGEIssue projections |
| `doge_issue_embeddings` | Эмбеддинги issues |
| `issue_candidates` | Кандидаты на promotion |
| `review_audit_log` | Аудит promotion решений |
| `issue_story_links` | Связь issue ↔ stories |
| `story_signals` | GPT-сигналы по историям |
| `cluster_memberships` | Принадлежность историй к кластерам |

### Healthcheck и readiness

```python
def healthcheck(self) -> bool:
    # GET /rest/v1/?limit=1 — базовая связь
    try:
        self._request(method="GET", path="/rest/v1/", params={"limit": "1"})
        return True
    except Exception:
        return False

def required_tables_ready(self) -> bool:
    # GET каждой таблицы с limit=1
    ...

def required_columns_ready(self) -> bool:
    # GET с explicit SELECT column list — проверяет наличие колонок
    ...

def required_stories_intake_v2_columns_ready(self) -> bool:
    # narrative_title_json, narrative_description_json, narrative_session_language
    ...

def service_role_policy_probe(self) -> bool:
    # POST в stories с dummy record — проверяет RLS для service_role
    ...
```

5 уровней проверки при старте. Все результаты попадают в `ApiDependencies.db_checks` → `/ready` endpoint.

---

## Bootstrap: SQL Schema

**Файл:** `supabase/bootstrap/000_full_init.sql`

Полная инициализация нового Supabase проекта. Включает все таблицы, индексы, RLS policies.

Применение через Supabase Dashboard → SQL Editor → выполнить содержимое файла.

### Migrations

**Директория:** `supabase/migrations/`

Файлы именуются по шаблону `YYYYMMDD_HHMM_description.sql`:

```
20260423_1500_init_db_wave.sql
20260423_1510_rls_db_wave.sql
20260427_1600_story_first_schema_parity.sql
20260505_1258_rename_to_doge_issues.sql
20260510_1400_m2_02_bootstrap_geo_embedding_nullable.sql
20260511_1200_m2_02_stories_narrative_extensions.sql
20260513_1200_m2_02_07_intake_v2_narrative.sql
20260515_1200_submitter_identity_issuer_not_null.sql
20260517_1200_issue_story_links_story_idx.sql
20260523_1200_req42_story_signals.sql
20260523_1210_req43_stories_institution_json.sql
```

Миграции применяются вручную через Supabase SQL Editor в хронологическом порядке. Нет Alembic, нет `supabase migration apply` — только SQL файлы + ручной запуск.

---

## Переменные окружения для Supabase

```bash
DB_BACKEND=supabase
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_SERVICE_ROLE=<service_role_key>
```

Нельзя использовать anon key — service_role нужен для обхода RLS и серверных операций.

---

## Шаги репликации в новом проекте

### 1. Создать Supabase проект

1. Зарегистрироваться на supabase.com
2. Создать новый проект
3. Получить `Project URL` и `service_role` key из Settings → API

### 2. Применить bootstrap SQL

```sql
-- В Supabase Dashboard → SQL Editor:
-- Скопировать содержимое supabase/bootstrap/000_full_init.sql и выполнить
```

Если bootstrap уже выполнен ранее — применять только миграции из `supabase/migrations/` в порядке имён.

### 3. Создать `.env`

```bash
DB_BACKEND=supabase
SUPABASE_URL=https://<your-project-ref>.supabase.co
SUPABASE_SERVICE_ROLE=<your-service-role-key>
APP_PROFILE=demo
API_BASE_URL=https://your-domain.com
```

### 4. Проверить connectivity

```bash
make check-env   # показывает DB_BACKEND и SUPABASE_URL
make serve       # стартует сервер, логи покажут:
                 # startup.persistence_backend backend=supabase db_ready=True
```

Или тест напрямую:

```bash
python3.11 -m pytest tests/integration/supabase/test_supabase_dotenv_connectivity.py -v
```

### 5. Создать `SupabaseMyRepository` для нового сервиса

```python
class SupabaseMyRepository:
    def __init__(self, db: SupabaseDatabase):
        self._db = db

    def save(self, record: MyRecord) -> None:
        self._db._request(
            method="POST",
            path="/rest/v1/my_table",
            json_body=_my_record_to_row(record),
            prefer="resolution=merge-duplicates",
        )

    def get(self, id: str) -> MyRecord | None:
        rows = self._db._request(
            method="GET",
            path="/rest/v1/my_table",
            params={"id": f"eq.{id}", "limit": "1"},
        )
        return _my_record_from_row(rows[0]) if rows else None
```

### 6. Добавить SQL migration

```sql
-- supabase/migrations/YYYYMMDD_HHMM_my_feature.sql
CREATE TABLE IF NOT EXISTS my_table (
    id TEXT PRIMARY KEY,
    data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE my_table ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_full" ON my_table FOR ALL TO service_role USING (true);
```

### Pitfalls

- **Service role vs anon key**: service role bypasses RLS — никогда не отдавай его клиентам. Только для серверной стороны
- **PostgREST returns list**: `GET` всегда возвращает список `[{...}]`, даже с `limit=1`. Всегда проверяй `if rows else None`
- **Upsert**: `prefer="resolution=merge-duplicates"` вместе с POST и наличием уникального constraint / PK — иначе будет дублирование
- **JSONB поля**: PostgREST может вернуть JSONB либо как dict, либо как строку в зависимости от версии. Всегда проверяй `isinstance(raw, dict)` перед `json.loads()`
- **RLS**: если `service_role_policy_probe()` возвращает False — значит RLS policy для service_role не создана. Добавь: `CREATE POLICY "service_role_full" ON stories FOR ALL TO service_role USING (true)`
- **`db_ready=False` при старте**: сервер всё равно поднимется, но `/ready` вернёт degraded. Это intentional — не crashloop, но сигнализирует оператору
