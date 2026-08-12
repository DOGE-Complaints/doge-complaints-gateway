# task-gw-rc-02-t03

## Meta
- **Story:** [STORY-GW-RC-02](../STORY-GW-RC-02-type-canonical-on-read.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000031
- **Skill declared:** python-pro
- **Depends on:** T02

## Purpose
При первом появлении неизвестного raw `type` — append **один раз** в накопительный файл `{LOG_DEBUG_DIR}/unknown_issue_types.jsonl` для ручного обновления enum оператором. Без `LOG_DEBUG_DIR` — только дефолт `IMPROVEMENT`, без файла.

## Code Facts
- Аналог per-story JSONL — [`logging_setup.py:36-74`](../../../../../../../src/core/logging_setup.py#L36-L74) `StoryDebugLogger`
- `LOG_DEBUG_DIR` на Railway ephemeral — [`server-env-quickstart.md:82`](../../../../../../../docs/runtime-docs/server-env-quickstart.md)
- `AppConfig.log_debug_dir` — [`schema.py`](../../../../../../../src/core/config/schema.py) (EnvSpec `LOG_DEBUG_DIR`)

## Acceptance / DoD
- Traces parent AC: observability для unknown type (дополнение к AC-3)
- Формат JSONL: `ts`, `raw_type`, `issue_id`, `normalized_to` (`IMPROVEMENT`)
- Dedupe: одна запись на distinct `raw_type` (per process + check existing file lines)
- При `LOG_DEBUG_DIR` unset — no-op, без ошибок
- Unit test с tmp `LOG_DEBUG_DIR`
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- Новый `src/core/projection/read_type_telemetry.py` (или расширение `logging_setup.py`)
- Wire из `canonicalize_issue_type_on_read()` при unknown branch

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/ -q -k unknown_issue_type
```
