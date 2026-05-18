from __future__ import annotations

import logging

import pytest

from core.logging_setup import configure_logging


def test_configure_logging_sets_root_level() -> None:
    """REQ-39 F-01: configure_logging sets root logger level."""
    configure_logging("DEBUG")
    try:
        assert logging.getLogger().level == logging.DEBUG
    finally:
        logging.getLogger().setLevel(logging.WARNING)
        logging.getLogger().handlers.clear()


def test_configure_logging_debug_messages_captured() -> None:
    """REQ-39 F-02: DEBUG records reach a handler after configure_logging."""
    configure_logging("DEBUG")
    messages: list[str] = []

    class _CaptureHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            messages.append(record.getMessage())

    logger = logging.getLogger("core.test")
    capture = _CaptureHandler()
    logger.addHandler(capture)
    try:
        logger.debug("test debug message")
        assert "test debug message" in messages
    finally:
        logger.removeHandler(capture)
        logging.getLogger().handlers.clear()
        logging.getLogger().setLevel(logging.WARNING)


def test_configure_logging_removes_old_handlers() -> None:
    """REQ-39 F-03: re-config replaces handlers (no duplicate streams)."""
    root = logging.getLogger()
    root.addHandler(logging.NullHandler())
    configure_logging("INFO")
    try:
        assert len(root.handlers) == 1
        assert isinstance(root.handlers[0], logging.StreamHandler)
    finally:
        root.handlers.clear()
        root.setLevel(logging.WARNING)
