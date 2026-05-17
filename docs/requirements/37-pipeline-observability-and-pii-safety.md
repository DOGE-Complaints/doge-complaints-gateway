# REQ-37: Pipeline Observability and PII Safety

**Статус:** Реализовано (STORY-M2-09-07, 2026-05-17)  
**Источник:** Gap-интервью 2026-05-13, G-05, G-06  
**Приоритет:** P2  
**Связанные SA:** SA-11  

---

## 1. Контекст

### G-05: Per-story debug-файл

Документация (req-trace-debug-§2.1 п.4) требует per-story трассировки. Сейчас все истории смешаны в одном общем логе — при диагностике "почему история не прошла pipeline" нужно фильтровать по `trace_id` в общем потоке. При большом объёме это неудобно.

### G-06: PII redaction

`api/logging.py` осторожно не логирует `narrative_original_text`, но нет единой функции-гаранта. Любой `logger.info(f"... {story.narrative_original_text}")` добавленный разработчиком вызовет утечку PII без системного контроля.

---

## 2. Требования

### 2.1 Per-story debug files — `StoryDebugLogger`

**Триггер:** наличие env var `LOG_DEBUG_DIR` (независимо от `LOG_LEVEL`). При отсутствии — файлы не создаются.

**Путь файла:** `{LOG_DEBUG_DIR}/{story_id}.jsonl`

**Формат: JSON Lines** — одна JSON-запись на строку:
```json
{"ts": "2026-05-13T12:00:00.000Z", "stage": "intake", "event": "story_accepted", "story_id": "...", "data": {"lifecycle": "READY_FOR_PROFILE", "language": "ru", "session_language": "ru", "has_canonical_type": true}}
{"ts": "...", "stage": "geo", "event": "resolved", "story_id": "...", "data": {"provider": "TallinnOpenCageStub", "normalized_label": "Tallinn, EE", "confidence": 0.88, "admin_settlement": "tallinn"}}
{"ts": "...", "stage": "signals", "event": "inferred", "story_id": "...", "data": {"civic_domain": "roads", "failure_pattern": "broken_infrastructure", "civic_weight": "recurring_issue"}}
{"ts": "...", "stage": "cluster", "event": "assigned", "story_id": "...", "data": {"cluster_id": "...", "lens": "civic_domain_micro", "key": "roads_infrastructure", "is_new": false}}
{"ts": "...", "stage": "promotion", "event": "gate_result", "story_id": "...", "data": {"readiness_score": 82, "threshold": 70, "canonical_type_gate": "pass", "promoted": true, "issue_id": "..."}}
```

**Покрытие — 5 этапов:**

| Stage | Событие | Ключевые данные |
|-------|---------|-----------------|
| `intake` | `story_accepted` | lifecycle, language, session_language, has_canonical_type |
| `geo` | `resolved` / `skipped` | provider, normalized_label, confidence, admin levels |
| `signals` | `inferred` | итоговый signals dict |
| `cluster` | `assigned` / `created` | cluster_id, lens, cluster_key, is_new |
| `promotion` | `gate_result` | readiness_score, threshold, canonical_type gate result, promoted |

**Реализация:**
```python
# logging_setup.py
class StoryDebugLogger:
    def __init__(self, story_id: str, debug_dir: str | None):
        self._story_id = story_id
        self._debug_dir = debug_dir
        self._file = None

    def log(self, stage: str, event: str, data: dict) -> None:
        if self._debug_dir is None or self._file is None:
            return
        record = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "stage": stage,
            "event": event,
            "story_id": self._story_id,
            "data": data,
        }
        self._file.write(json.dumps(record, ensure_ascii=False) + "\n")

    def __enter__(self): ...   # открыть файловый хендлер
    def __exit__(self, ...): ...  # закрыть
```

Инстанциируется в `application/services.py`, передаётся downstream через параметры.

### 2.2 `redact_pii()` — флаг-зависимая редакция

```python
# api/logging.py
def redact_pii(text: str, contains_pii: bool) -> str:
    """Return '[REDACTED]' if PII flag is set, otherwise full text."""
    if contains_pii:
        return "[REDACTED]"
    return text
```

**Правило:** любой код который логирует поля нарратива (`original_text`, `title`, `description`) обязан пропускать их через `redact_pii(text, story.privacy.contains_pii)`.

**Применяется в:**
- `StoryDebugLogger.log()` при логировании текстовых полей
- `application/services.py` в любых `logger.*` вызовах
- Всех местах где `narrative_original_text` попадает в лог

---

## 3. Новый env var

| Env var | Тип | Описание |
|---------|-----|----------|
| `LOG_DEBUG_DIR` | `str \| None` | Путь к директории для per-story debug файлов. Если не задан — файлы не создаются. |

Добавить в `config/schema.py` как optional env var.

---

## 4. Cascade — файлы для изменения

| Файл | Изменение |
|------|-----------|
| `logging_setup.py` | Новый `StoryDebugLogger` класс |
| `api/logging.py` | Новая функция `redact_pii(text, contains_pii)` |
| `config/schema.py` | Новый `LOG_DEBUG_DIR: str \| None` |
| `application/services.py` | Инстанцировать `StoryDebugLogger`, передавать downstream; применять `redact_pii` |
| `geo/service.py` | Принять `debug_logger`, логировать resolution result |
| `profile/enrichment.py` | Принять `debug_logger`, логировать signal inference result |
| `cluster/engine.py` | Принять `debug_logger`, логировать cluster assignment |
| `promotion/gates.py` | Принять `debug_logger`, логировать gate result |
| `example.env` | `# LOG_DEBUG_DIR=./debug_logs` (закомментировано по умолчанию) |

---

## 5. Acceptance Criteria

- [x] При `LOG_DEBUG_DIR=./debug_logs` → файл `./debug_logs/{story_id}.jsonl` создаётся при обработке истории
- [x] Файл содержит записи для всех 5 этапов pipeline
- [x] При `LOG_DEBUG_DIR` не задан → файлы не создаются (нет ошибок)
- [x] `redact_pii("text", contains_pii=True)` → `"[REDACTED]"`
- [x] `redact_pii("text", contains_pii=False)` → `"text"`
- [x] История с `privacy.contains_pii=True` → `original_text` не появляется в логах в открытом виде
- [x] `LOG_DEBUG_DIR` независим от `LOG_LEVEL` — файлы создаются даже при `LOG_LEVEL=INFO`
