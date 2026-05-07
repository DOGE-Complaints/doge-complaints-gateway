# 28. Cron-планировщик кластеризации — отвязка от intake

Дата: 2026-05-05  
Статус: решение принято — готово к задачированию  
Supersedes: текущий синхронный вызов в `handle_story_intake()` → `process_story(story_id)`  
Связано: `20-post-demo-orchestration-and-scheduled-jobs.md`, `25-clustering-engine-target-state-spec.md`

---

## 1. Контекст и проблема

Сейчас кластеризация запускается синхронно в теле каждого `POST /intake/stories`. Это означает:

- При 0–7 историях в очереди: полный пересчёт выполняется, ничего не создаётся, результат выброшен
- При N историях в очереди: каждый intake пересчитывает все N
- Если clustering упадёт — intake вернёт 500, story не сохранится (нет транзакционного разделения)
- Истории в `READY_FOR_PROFILE` "зависают" без обработки, если поток intake прекращается

**Решение:** intake только сохраняет story. Кластеризация запускается отдельно по расписанию.

---

## 2. Целевая модель

```
POST /intake/stories
  └── save story → advance lifecycle → return {story_id, status}
                          (кластеризация НЕ вызывается)

Background ClusterCronJob (каждые CLUSTER_CRON_INTERVAL_S секунд)
  └── count READY_FOR_PROFILE
       ├── < CLUSTER_MIN_SIZE  → пропустить
       └── >= CLUSTER_MIN_SIZE → process_all_pending()
               └── cluster → create issues → mark CLUSTERED
```

---

## 3. Новый метод: `process_all_pending()`

**Файл:** `src/core/application/cluster_orchestrator.py`

Новый метод на `StoryClusterOrchestrator`, дополняющий существующий `process_story(story_id)`:

```python
def process_all_pending(self) -> list[str]:
    """
    Кластеризовать все READY_FOR_PROFILE stories за один прогон.
    Возвращает список созданных issue_id (может быть пустым).
    """
```

**Алгоритм:**

1. Загрузить все `READY_FOR_PROFILE` stories → `ready_stories`
2. Если `len(ready_stories) < min_size_guard` → вернуть `[]` (нет смысла кластеризовать)
3. Извлечь сигналы для каждой story → `profiles`
4. Вычислить `memberships` по всем активным линзам (один вызов `clustering_engine.memberships()`)
5. Сгруппировать по `primary_lens`: `cluster_id → [story_ids]`
6. Для каждого уникального кластера:
   a. Вычислить `readiness_score`
   b. Попробовать `issue_create_service.create_issue(...)` — если gates не пройдут или кластер уже существует, продолжить следующий
   c. При успехе: пометить все member stories как `CLUSTERED`
7. Вернуть список созданных `issue_id`

**Почему один прогон, а не вызов `process_story()` N раз:** текущий `process_story()` загружает `list_stories_ready_for_clustering()` каждый раз — при N историях это N полных сканов. `process_all_pending()` делает один скан для всего батча.

**`min_size_guard`:** опциональный параметр (по умолчанию берётся из конфига `CLUSTER_MIN_SIZE`). Позволяет не запускать дорогой пересчёт, если историй ещё недостаточно.

---

## 4. Background cron job

**Файл:** `src/core/scheduler/cluster_cron.py` (новый)

```python
@dataclass
class ClusterCronJob:
    orchestrator: StoryClusterOrchestrator
    interval_s: int          # CLUSTER_CRON_INTERVAL_S
    min_size_guard: int      # CLUSTER_MIN_SIZE

    def start(self) -> None:
        """Запустить фоновый поток. Вызывается при старте ASGI app."""

    def stop(self) -> None:
        """Остановить поток. Вызывается при shutdown ASGI app."""
```

**Механизм:** `threading.Thread(daemon=True)` + `threading.Event` для остановки. Никаких внешних зависимостей (Redis, Celery, APScheduler) — только stdlib.

**Цикл:**
```
while not stop_event.wait(interval_s):
    try:
        count = count_ready_for_profile()  # быстрый COUNT(*) без полного scan
        if count >= min_size_guard:
            issue_ids = orchestrator.process_all_pending()
            log("cluster.cron_run", issued=len(issue_ids))
    except Exception:
        log("cluster.cron_error", ...)  # не падаем, продолжаем цикл
```

**Идемпотентность:** гарантируется существующим lifecycle-механизмом. `CLUSTERED` stories исключаются из `list_stories_ready_for_clustering()`. Повторный запуск cron до появления новых stories ничего не создаст.

**Concurrent runs:** при `interval_s` > времени выполнения батча конкурентных запусков не будет. Если нужна явная защита — простой `threading.Lock` в `ClusterCronJob.run()`.

---

## 5. Интеграция в ASGI app

**Файл:** `src/core/api/asgi_app.py`

FastAPI поддерживает lifespan-хуки:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    cron_job = build_cluster_cron_job()   # из service factory
    cron_job.start()
    yield
    cron_job.stop()

app = FastAPI(lifespan=lifespan)
```

`build_cluster_cron_job()` читает конфигурацию и создаёт `ClusterCronJob` с нужным оркестратором.

---

## 6. Изменения в `handle_story_intake()`

**Файл:** `src/core/api/handlers.py`

Убрать:
```python
issue_id = dependencies.story_cluster_orchestrator.process_story(story.story_id)
```

Оставить только сохранение story и возврат ответа. Логи `story_intake_cluster_triggered_issue` / `story_intake_cluster_no_issue` — перенести в `ClusterCronJob`.

**Response contract не меняется:** `{story_id, status}` — intake возвращает то же самое.

---

## 7. Новые env vars

| Переменная | Тип | Дефолт | Описание |
|------------|-----|--------|----------|
| `CLUSTER_CRON_INTERVAL_S` | int (>0) | `60` | Интервал между запусками cron в секундах |
| `CLUSTER_CRON_ENABLED` | bool | `true` | Позволяет отключить cron без изменения кода (удобно для тестов) |

Добавить в `ENV_SCHEMA` в `src/core/config/schema.py` и в `AppConfig`.

---

## 8. Влияние на тесты

- `handle_story_intake` тесты: убрать проверки на `process_story()` call — intake больше не запускает кластеризацию
- Добавить unit-тесты для `process_all_pending()`: пустая очередь, < min_size, >= min_size → создаёт issue
- Добавить тест для `ClusterCronJob`: start/stop, guard condition, idempotency (повторный запуск = 0 новых issues)
- Тесты e2e, которые проверяют issue creation через intake, нужно обновить: либо вызывать `process_all_pending()` напрямую, либо ждать cron-тика

---

## 9. Порядок реализации

| # | Задача | Файлы |
|---|--------|-------|
| 1 | Добавить `CLUSTER_CRON_INTERVAL_S`, `CLUSTER_CRON_ENABLED` в config schema | `config/schema.py` |
| 2 | Реализовать `process_all_pending()` в `StoryClusterOrchestrator` | `application/cluster_orchestrator.py` |
| 3 | Создать `ClusterCronJob` с start/stop/run | `scheduler/cluster_cron.py` (новый) |
| 4 | Добавить lifespan hook в ASGI app | `api/asgi_app.py` |
| 5 | Убрать `process_story()` из `handle_story_intake()` | `api/handlers.py` |
| 6 | Обновить тесты | `tests/` |
| 7 | Smoke: `POST /intake/stories` создаёт story, cron создаёт issue | e2e проверка |

---

## 10. Acceptance criteria

**AC-28-1:** `POST /intake/stories` не вызывает кластеризацию. Возвращает `{story_id, status}` без задержки от clustering.

**AC-28-2:** `process_all_pending()` при `< CLUSTER_MIN_SIZE` историй возвращает `[]` и не создаёт issue.

**AC-28-3:** `process_all_pending()` при `>= CLUSTER_MIN_SIZE` историй создаёт issue и помечает member stories `CLUSTERED`.

**AC-28-4:** Повторный вызов `process_all_pending()` без новых stories возвращает `[]` (idempotency).

**AC-28-5:** `ClusterCronJob` запускается при старте app и останавливается при shutdown без ошибок.

**AC-28-6:** При `CLUSTER_CRON_ENABLED=false` cron не стартует, сервис работает в режиме "intake only".
