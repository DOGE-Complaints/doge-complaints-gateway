from __future__ import annotations

import logging
from contextvars import ContextVar
from datetime import UTC, datetime
from pathlib import Path
from threading import Lock
from typing import Any

_current_trace_id: ContextVar[str | None] = ContextVar("trace_id", default=None)
_current_story_id: ContextVar[str | None] = ContextVar("story_id", default=None)


class _ContextDefaultsFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "trace_id"):
            record.trace_id = _current_trace_id.get() or "-"
        if not hasattr(record, "story_id"):
            record.story_id = _current_story_id.get() or "-"
        return True


class StoryDebugFileHandler(logging.Handler):
    """Writes log records into story-scoped DEBUG files."""

    def __init__(self, log_debug_dir: Path) -> None:
        super().__init__(level=logging.DEBUG)
        self._base_dir = log_debug_dir
        self._lock = Lock()
        self._format = logging.Formatter(
            "%(asctime)s %(levelname)-8s %(name)s %(message)s [trace_id=%(trace_id)s story_id=%(story_id)s]"
        )

    def emit(self, record: logging.LogRecord) -> None:
        story_id = _current_story_id.get()
        trace_id = _current_trace_id.get()
        if not story_id or not trace_id:
            return
        date_dir = self._base_dir / "stories" / datetime.now(UTC).date().isoformat()
        date_dir.mkdir(parents=True, exist_ok=True)
        file_path = date_dir / f"{trace_id[:8]}-{story_id[:8]}.log"
        line = self._format.format(record)
        with self._lock:
            with file_path.open("a", encoding="utf-8") as fp:
                fp.write(f"{line}\n")


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

    if log_level.upper() == "DEBUG" and log_debug_dir:
        debug_handler = StoryDebugFileHandler(Path(log_debug_dir))
        debug_handler.addFilter(_ContextDefaultsFilter())
        root.addHandler(debug_handler)

    logging.getLogger("uvicorn.access").propagate = False
    logging.getLogger(__name__).info(
        "logging.configured",
        extra={"configured_level": log_level.upper(), "log_format": log_format.lower()},
    )
