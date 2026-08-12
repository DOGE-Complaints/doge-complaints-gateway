## Task workspace — `task-m2-09-07-t02-story-debug-logger-jsonl`

- Story: [`../STORY-M2-09-07-pipeline-observability-and-pii-safety.md`](../STORY-M2-09-07-pipeline-observability-and-pii-safety.md)
- Decision Ref: REQ-37 §2.1, §3; G-05

---
**Приоритет:** P0  
**Сложность:** M  
**Оценка времени:** 1–2 ч  
**Статус:** ready  
**Wave:** `pkg-000016`  
---

## Task: implement — `StoryDebugLogger` JSONL per story

### Цель
Реализовать `StoryDebugLogger` с путём `{LOG_DEBUG_DIR}/{story_id}.jsonl`, JSON Lines, context manager; активировать при `log_debug_dir` **без** требования `LOG_LEVEL=DEBUG`.

### Факты из кода
1. [`logging_setup.py`](../../../../../../../src/core/logging_setup.py) L23–45 — `StoryDebugFileHandler`: path `stories/{date}/{trace[:8]}-{story[:8]}.log`.
2. L105–108 — handler attached only when `log_level.upper() == "DEBUG" and log_debug_dir`.
3. [`schema.py`](../../../../../../../src/core/config/schema.py) L105–108 — `LOG_DEBUG_DIR` EnvSpec **уже есть**; `log_debug_dir` on AppConfig.
4. [`example.env`](../../../../../../../example.env) — **нет** строки `LOG_DEBUG_DIR` (rg 0).

### Gap / Проблема
**GAP-37-01:** нет `StoryDebugLogger`; interim handler wrong format/path/gating.  
**GAP-37-02 (partial):** schema done; `example.env` + runtime behavior missing.

### AC/DoD
- [ ] (P0) `StoryDebugLogger` with `log(stage, event, data)` writing JSONL.
- [ ] (P0) File path `{debug_dir}/{story_id}.jsonl`.
- [ ] (P0) `configure_logging` / factory: enable when `log_debug_dir` set regardless of `LOG_LEVEL`.
- [ ] (P1) `# LOG_DEBUG_DIR=./debug_logs` in `example.env`.
- [ ] (P1) Refactor or deprecate `StoryDebugFileHandler` in favor of REQ-37 path.

### Где менять код
- [`src/core/logging_setup.py`](../../../../../../../src/core/logging_setup.py)
- [`example.env`](../../../../../../../example.env)

### Out of scope
- Pipeline stage payloads (T03–T05)
- Changes to `schema.py` unless test gap found

### Команды проверки
```bash
cd doge-complaints-gateway && LOG_DEBUG_DIR=/tmp/doge-debug python3 -c "from core.logging_setup import StoryDebugLogger; print(StoryDebugLogger)"
```
