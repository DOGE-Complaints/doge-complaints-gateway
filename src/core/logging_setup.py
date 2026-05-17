from __future__ import annotations

import json
import logging
from contextvars import ContextVar
from datetime import UTC, datetime
from pathlib import Path
from threading import Lock
from typing import Any, Protocol

_current_trace_id: ContextVar[str | None] = ContextVar("trace_id", default=None)
_current_story_id: ContextVar[str | None] = ContextVar("story_id", default=None)


class StoryPipelineDebugLog(Protocol):
    def log(self, stage: str, event: str, data: dict[str, Any]) -> None: ...


class _ContextDefaultsFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "trace_id"):
            record.trace_id = _current_trace_id.get() or "-"
        if not hasattr(record, "story_id"):
            record.story_id = _current_story_id.get() or "-"
        return True


class StoryDebugLogger:
    """REQ-37: per-story JSON Lines debug trace at {debug_dir}/{story_id}.jsonl."""

    def __init__(self, story_id: str, debug_dir: str | None) -> None:
        self._story_id = story_id
        self._debug_dir = debug_dir.strip() if debug_dir and debug_dir.strip() else None
        self._file = None
        self._lock = Lock()

    def log(self, stage: str, event: str, data: dict[str, Any]) -> None:
        if self._debug_dir is None or self._file is None:
            return
        record = {
            "ts": datetime.now(UTC).isoformat(timespec="milliseconds").replace(
                "+00:00", "Z"
            ),
            "stage": stage,
            "event": event,
            "story_id": self._story_id,
            "data": data,
        }
        line = json.dumps(record, ensure_ascii=False) + "\n"
        with self._lock:
            self._file.write(line)
            self._file.flush()

    def __enter__(self) -> StoryDebugLogger:
        if self._debug_dir is not None:
            path = Path(self._debug_dir)
            path.mkdir(parents=True, exist_ok=True)
            self._file = (path / f"{self._story_id}.jsonl").open(
                "a", encoding="utf-8"
            )
        return self

    def __exit__(self, *args: object) -> None:
        if self._file is not None:
            self._file.close()
            self._file = None


def open_story_debug_logger(story_id: str, debug_dir: str | None) -> StoryDebugLogger:
    return StoryDebugLogger(story_id, debug_dir)


def set_log_context(*, trace_id: str | None = None, story_id: str | None = None) -> None:
    if trace_id is not None:
        _current_trace_id.set(trace_id)
    if story_id is not None:
        _current_story_id.set(story_id)


def clear_log_context() -> None:
    _current_trace_id.set(None)
    _current_story_id.set(None)


def log_runtime_exception(
    logger: logging.Logger,
    exc: BaseException,
    *,
    stage: str,
    trace_id: str | None = None,
    story_id: str | None = None,
    **extra_fields: Any,
) -> None:
    """Emit a single structured exception event for runtime diagnostics."""
    if trace_id is not None:
        _current_trace_id.set(trace_id)
    if story_id is not None:
        _current_story_id.set(story_id)
    logger.exception(
        "runtime.exception",
        extra={
            "stage": stage,
            "exception_type": type(exc).__name__,
            "message": str(exc),
            "stack": True,
            **extra_fields,
        },
    )


def configure_logging(log_level: str, *, log_format: str = "text", log_debug_dir: str | None = None) -> None:
    # Pytest often skips ASGI lifespan → this may not run; see docs/runtime-docs/testing/pytest-logging-without-asgi-lifespan.md
    del log_debug_dir  # per-story JSONL via StoryDebugLogger; independent of LOG_LEVEL (REQ-37)
    level = getattr(logging, log_level.upper(), logging.INFO)
    if log_format.strip().lower() == "json":
        fmt = '{"ts":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","msg":"%(message)s","trace_id":"%(trace_id)s","story_id":"%(story_id)s"}'
    else:
        fmt = "%(asctime)s %(levelname)-8s %(name)s %(message)s [trace_id=%(trace_id)s story_id=%(story_id)s]"

    root = logging.getLogger()
    root.setLevel(level)
    for handler in list(root.handlers):
        root.removeHandler(handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(logging.Formatter(fmt))
    stream_handler.addFilter(_ContextDefaultsFilter())
    root.addHandler(stream_handler)

    logging.getLogger("uvicorn.access").propagate = False
    logging.getLogger(__name__).info(
        "logging.configured",
        extra={"configured_level": log_level.upper(), "log_format": log_format.lower()},
    )
