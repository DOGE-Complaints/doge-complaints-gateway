# 11. Cross-cutting: Security, Config, Observability

## Security baseline (demo-safe)
- service-role never exposed to public route path;
- auth middleware chain at API boundary;
- strict input validation and output shaping;
- secret redaction in logs;
- `identity_issuer` обязательный — eID gate на intake (HTTP 400 без него);
- no debug mode in runtime.

## PII Safety — `redact_pii()` (G-06)

```python
# api/logging.py
def redact_pii(text: str, contains_pii: bool) -> str:
    if contains_pii:
        return "[REDACTED]"
    return text
```

Применяется везде где `narrative_original_text` попадает в лог. Флаг `privacy.contains_pii` из intake payload управляет поведением.

## Config governance
- centralized config module (env schema + defaults);
- explicit env contract for demo/pilot profiles;
- feature flags for pilot adapters (wallet, blockchain, tokenization).

## Observability
- structured logging with `trace_id`;
- health endpoints (`/health`, `/health/detailed`);
- metrics:
  - intake throughput
  - clustering latency
  - issue promotion success rate
  - projection contract violations
  - (post-demo) scheduled job / automation runs: success rate, duration, last error (см. `16-automation-orchestration-and-scheduled-jobs.md`, EPIC-M2-11)

## Per-story Debug Files — `StoryDebugLogger` (G-05)

Активируется при наличии env var `LOG_DEBUG_DIR` (независимо от `LOG_LEVEL`).

- Путь: `{LOG_DEBUG_DIR}/{story_id}.jsonl`
- Формат: JSON Lines — одна запись на событие
- Покрытие: все 5 этапов pipeline (intake, geo, signals, cluster, promotion)

```python
# logging_setup.py
class StoryDebugLogger:
    def __init__(self, story_id: str, debug_dir: str | None): ...
    def log(self, stage: str, event: str, data: dict) -> None: ...
    # context manager: открывает/закрывает файловый хендлер
```

Инстанциируется в `application/services.py`, передаётся downstream (geo, signals, cluster, promotion).

**Новый env var:** `LOG_DEBUG_DIR: str | None` — опциональный, не задан = файлы не создаются.

## Решения интервью (2026-05-13)
Подробно: REQ-37, `docs/analysis/gap-interview-decisions-2026-05-13.md` G-05/G-06

## Failure strategy
- fail-closed for unsafe operations;
- fail-soft for optional enrichments;
- retry with backoff for external adapters;
- dead-letter pattern reserved for pilot async jobs.
