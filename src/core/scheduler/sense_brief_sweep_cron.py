"""GW-REQ57-03: cron-class sense-brief sweep (ClusterCronJob precedent)."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from threading import Event, Lock, Thread
from time import monotonic

from core.application.sense_brief_sweep import SenseBriefSweepService
from core.logging_setup import log_runtime_exception

logger = logging.getLogger(__name__)


@dataclass
class SenseBriefSweepCronJob:
    """Periodic re-nudge for pending/failed Issues (reuse nudge client; no ready overwrite)."""

    sweep_service: SenseBriefSweepService
    interval_s: int
    _stop_event: Event = field(default_factory=Event, init=False, repr=False)
    _run_lock: Lock = field(default_factory=Lock, init=False, repr=False)
    _thread: Thread | None = field(default=None, init=False, repr=False)

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = Thread(
            target=self._run_loop, name="sense-brief-sweep-cron", daemon=True
        )
        self._thread.start()
        logger.info(
            "sense_brief_sweep.cron_started",
            extra={"interval_s": self.interval_s},
        )

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=max(self.interval_s, 1))
        logger.info("sense_brief_sweep.cron_stopped")

    def run_once(self) -> None:
        """Exposed for tests / manual tick."""
        with self._run_lock:
            self._execute_run()

    def _run_loop(self) -> None:
        while not self._stop_event.wait(max(self.interval_s, 1)):
            with self._run_lock:
                self._execute_run()

    def _execute_run(self) -> None:
        run_started = monotonic()
        run_id = f"sense-brief-sweep-{int(run_started * 1000)}"
        logger.info(
            "sense_brief_sweep.cron_run_start run_id=%s",
            run_id,
            extra={"run_id": run_id},
        )
        try:
            result = self.sweep_service.run_once()
            elapsed_ms = int((monotonic() - run_started) * 1000)
            logger.info(
                "sense_brief_sweep.cron_run_end run_id=%s eligible_count=%s "
                "nudged_count=%s skipped_ready_count=%s duration_ms=%s",
                run_id,
                result.eligible_count,
                result.nudged_count,
                result.skipped_ready_count,
                elapsed_ms,
                extra={
                    "run_id": run_id,
                    "eligible_count": result.eligible_count,
                    "nudged_count": result.nudged_count,
                    "skipped_ready_count": result.skipped_ready_count,
                    "duration_ms": elapsed_ms,
                },
            )
        except Exception as exc:  # noqa: BLE001
            elapsed_ms = int((monotonic() - run_started) * 1000)
            log_runtime_exception(
                logger,
                exc,
                stage="sense_brief_sweep.cron",
                run_id=run_id,
                duration_ms=elapsed_ms,
            )
