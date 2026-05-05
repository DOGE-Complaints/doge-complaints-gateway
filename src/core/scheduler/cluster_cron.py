from __future__ import annotations

import logging
from dataclasses import dataclass, field
from threading import Event, Lock, Thread

from core.application import StoryClusterOrchestrator

logger = logging.getLogger(__name__)


@dataclass
class ClusterCronJob:
    orchestrator: StoryClusterOrchestrator
    interval_s: int
    min_size_guard: int
    _stop_event: Event = field(default_factory=Event, init=False, repr=False)
    _run_lock: Lock = field(default_factory=Lock, init=False, repr=False)
    _thread: Thread | None = field(default=None, init=False, repr=False)

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = Thread(target=self._run_loop, name="cluster-cron-job", daemon=True)
        self._thread.start()
        logger.info(
            "cluster.cron_started",
            extra={"interval_s": self.interval_s, "min_size_guard": self.min_size_guard},
        )

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=max(self.interval_s, 1))
        logger.info("cluster.cron_stopped")

    def _run_loop(self) -> None:
        while not self._stop_event.wait(max(self.interval_s, 1)):
            with self._run_lock:
                try:
                    issue_ids = self.orchestrator.process_all_pending()
                    logger.info(
                        "cluster.cron_run",
                        extra={
                            "issued_count": len(issue_ids),
                            "issue_ids": issue_ids,
                            "min_size_guard": self.min_size_guard,
                        },
                    )
                except Exception as exc:  # noqa: BLE001
                    logger.exception(
                        "cluster.cron_error",
                        extra={"error": str(exc)},
                    )
