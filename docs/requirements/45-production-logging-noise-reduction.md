# REQ-45: Production logging — снижение шума и stdout/stderr split

**Статус:** requirements — ready for tasking  
**Источник:** `docs/analysis/analysis-logging-production-observability-2026-05-25.md`  
**Приоритет:** P2  
**Тип:** code patch (1 файл) + test update (1 строка) + docs (1 файл)  
**Зависит от:** REQ-37 (per-story debug logging — реализован, не затрагивается)  
**Серверная сторона:** `src/core/logging_setup.py` только; domain/application/infra слои не затрагиваются

---

## 1. Контекст

Аудит logging-системы (`analysis-logging-production-observability-2026-05-25.md`) выявил три проблемы в `src/core/logging_setup.py:configure_logging()`:

**P-1 — весь поток идёт в stderr.** `logging.StreamHandler()` без аргумента → `sys.stderr`. На Railway все логи — включая нормальный бизнес-поток (`story_intake_created`, `intake.persistence_save_done`) — отображаются с префиксом `[err]` (красные). Оператор не может отличить реальные ошибки от успешных событий.

**P-2 — httpx/httpcore не подавлены.** При `LOG_LEVEL=DEBUG` каждый HTTP-запрос к Supabase генерирует 4–6 строк от `httpx` и `httpcore` (уровни DEBUG/INFO). Они полностью перекрывают бизнес-логи. Пример:
```
DEBUG httpx._client - HTTP Request: POST https://xxx.supabase.co/rest/v1/stories "HTTP/1.1 201 Created"
DEBUG httpcore._sync.connection_pool - acquire connection waiting=0 connections=1
```

**P-3 — LOG_FORMAT=json не задокументирован** как production-рекомендация, хотя код его поддерживает (`logging_setup.py:117`).

REQ-37 (per-story debug logging через `StoryDebugLogger`, файлы `{LOG_DEBUG_DIR}/{story_id}.jsonl`) — полностью реализован, работает, не затрагивается этим REQ.

---

## 2. Текущее состояние

### 2.1 `configure_logging()` — релевантный фрагмент (`logging_setup.py:112-136`)

```python
def configure_logging(log_level: str, *, log_format: str = "text", log_debug_dir: str | None = None) -> None:
    del log_debug_dir
    level = getattr(logging, log_level.upper(), logging.INFO)
    # ...
    stream_handler = logging.StreamHandler()          # ← без аргумента = sys.stderr
    stream_handler.setLevel(level)
    stream_handler.setFormatter(logging.Formatter(fmt))
    stream_handler.addFilter(_ContextDefaultsFilter())
    root.addHandler(stream_handler)
    logging.getLogger("uvicorn.access").propagate = False  # ← только access подавлен
    # httpx, httpcore — не подавлены
```

### 2.2 Тест, который нужно обновить (`test_logging_setup.py:41-51`)

```python
def test_configure_logging_removes_old_handlers() -> None:
    root = logging.getLogger()
    root.addHandler(logging.NullHandler())
    configure_logging("INFO")
    try:
        assert len(root.handlers) == 1                  # ← станет 2 после split
        assert isinstance(root.handlers[0], logging.StreamHandler)
    finally:
        root.handlers.clear()
        root.setLevel(logging.WARNING)
```

---

## 3. Целевое состояние

### 3.1 Изменение A: suppress httpx/httpcore

В `configure_logging()`, после `root.addHandler(stream_handler)` / после добавления обоих хендлеров (если split реализован):

**Добавить две строки:**
```python
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
```

**Что даёт:** httpx и httpcore будут логировать только при HTTP-ошибках (WARNING+). Весь DEBUG/INFO шум ("I sent this request", "connection pool") исчезает. При `LOG_LEVEL=DEBUG` бизнес-логи снова читаемы.

### 3.2 Изменение B: stdout/stderr split

**Добавить новый класс-filter рядом с `_ContextDefaultsFilter`:**

```python
class _LevelBelowWarningFilter(logging.Filter):
    """Pass only DEBUG and INFO records — for stdout channel of split handler."""
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno < logging.WARNING
```

**Заменить единственный `stream_handler` на два хендлера:**

**Было:**
```python
stream_handler = logging.StreamHandler()   # sys.stderr
stream_handler.setLevel(level)
stream_handler.setFormatter(logging.Formatter(fmt))
stream_handler.addFilter(_ContextDefaultsFilter())
root.addHandler(stream_handler)
```

**Стало:**
```python
import sys
formatter = logging.Formatter(fmt)

# DEBUG + INFO → stdout (Railway: без [err] prefix)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(level)
stdout_handler.addFilter(_LevelBelowWarningFilter())
stdout_handler.setFormatter(formatter)
stdout_handler.addFilter(_ContextDefaultsFilter())
root.addHandler(stdout_handler)

# WARNING / ERROR / CRITICAL → stderr (Railway: правильный [err] prefix)
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.WARNING)
stderr_handler.setFormatter(formatter)
stderr_handler.addFilter(_ContextDefaultsFilter())
root.addHandler(stderr_handler)
```

**Что даёт:**

| Уровень | Куда | На Railway |
|---------|------|-----------|
| DEBUG, INFO | stdout | без `[err]` — чистый вывод |
| WARNING, ERROR, CRITICAL | stderr | `[err]` — корректный сигнал |

Бизнес-события `story_intake_created`, `intake.persistence_save_done`, `story.persistence_commit_ack` — нормальный INFO поток — перестают показываться красным.

### 3.3 Изменение C: clarify `del log_debug_dir` comment

Обновить комментарий в сигнатуре `configure_logging()`:

**Было:**
```python
    # Pytest often skips ASGI lifespan → this may not run; see docs/...
    del log_debug_dir  # per-story JSONL via StoryDebugLogger; independent of LOG_LEVEL (REQ-37)
```

**Стало:**
```python
    # log_debug_dir принимается для API-симметрии: lifespan передаёт deps.config.log_debug_dir
    # не задумываясь. configure_logging() его не использует — per-story файлы создаются
    # в StoryDebugLogger внутри services.py и cluster_orchestrator.py (REQ-37).
    del log_debug_dir
```

### 3.4 Изменение D: обновить тест (1 строка)

В `tests/test_logging_setup.py`, функция `test_configure_logging_removes_old_handlers`:

**Было:**
```python
assert len(root.handlers) == 1
assert isinstance(root.handlers[0], logging.StreamHandler)
```

**Стало:**
```python
assert len(root.handlers) == 2
assert all(isinstance(h, logging.StreamHandler) for h in root.handlers)
```

### 3.5 Изменение E: документировать в quickstart (docs-only)

В `docs/runtime-docs/server-env-quickstart.md`, раздел §3 "Переменные окружения" — добавить параграф после таблицы DB_BACKEND:

**Добавить:**

```markdown
### Production logging — рекомендации

| Переменная | Production значение | Почему |
|-----------|--------------------|----|
| `LOG_LEVEL` | `INFO` | При `DEBUG` httpx/httpcore генерируют шум на каждый Supabase запрос |
| `LOG_FORMAT` | `json` | Structured logs для Railway / Datadog / Loki / любого log-агрегатора |
| `LOG_DEBUG_DIR` | *(не задавать)* | Только для краткосрочной диагностики |

**`LOG_FORMAT=json`** — каждая строка становится валидным JSON:
```json
{"ts":"2026-05-25T10:01:23","level":"INFO","logger":"core.api","msg":"story_intake_created","trace_id":"abc","story_id":"def"}
```

**`LOG_DEBUG_DIR` на Railway:** файлы создаются в ephemeral filesystem контейнера — исчезают при каждом редеплое. Для краткосрочной диагностики: добавить переменную, отправить тестовую историю, забрать JSONL через Railway shell.
```

---

## 4. Файлы для изменения

| Файл | Изменение | Строки |
|------|-----------|--------|
| `src/core/logging_setup.py` | Новый `_LevelBelowWarningFilter` класс | +4 |
| `src/core/logging_setup.py` | `configure_logging()`: заменить 1 StreamHandler на 2, suppress httpx/httpcore, уточнить комментарий | ~+15 / -5 |
| `tests/test_logging_setup.py` | `test_configure_logging_removes_old_handlers`: `len == 1` → `len == 2`, проверить оба хендлера | 2 строки |
| `docs/runtime-docs/server-env-quickstart.md` | Добавить §Production logging section | +15 |

Код вне `logging_setup.py` не изменяется: `services.py`, `cluster_orchestrator.py`, `handlers.py`, `api/logging.py`, domain/infra слои — не затронуты.

---

## 5. Acceptance Criteria

- [ ] `configure_logging("INFO")` → `root.handlers` содержит ровно 2 хендлера, оба `StreamHandler`
- [ ] Один хендлер направлен в `sys.stdout`, второй в `sys.stderr`
- [ ] `logging.INFO`-сообщения попадают только в stdout-хендлер (не в stderr)
- [ ] `logging.WARNING`-сообщения попадают только в stderr-хендлер
- [ ] `logging.getLogger("httpx").level == logging.WARNING` после вызова `configure_logging()`
- [ ] `logging.getLogger("httpcore").level == logging.WARNING` после вызова `configure_logging()`
- [ ] `test_configure_logging_removes_old_handlers` — обновлён и проходит
- [ ] Все остальные тесты в `tests/test_logging_setup.py` и `tests/test_req37_pipeline_observability_pii.py` — без регрессий
- [ ] Тест-суит целиком: 430 passed (или больше если добавлены новые тесты)
- [ ] `docs/runtime-docs/server-env-quickstart.md` содержит секцию с рекомендациями `LOG_LEVEL=INFO`, `LOG_FORMAT=json`

---

## 6. Не в scope этого REQ

- Изменения в `application/services.py`, `cluster_orchestrator.py`, `geo/service.py`, `profile/enrichment.py` — `StoryDebugLogger` работает, не трогать
- Изменения в domain/infra слоях — DB, contracts, handlers
- Persistent per-story logs в облаке (S3, Supabase Storage) — product backlog
- Изменения в OpenAPI schema или `API_REFERENCE.md`
- Изменения в `uvicorn.error` logger propagation (с stdout/stderr split startup INFO messages автоматически попадут в stdout без `[err]`)
