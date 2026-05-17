from __future__ import annotations

import logging
from dataclasses import dataclass, field
from time import monotonic
from threading import Event, Lock, Thread

from core.application import StoryClusterOrchestrator
from core.logging_setup import log_runtime_exception

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
                run_started = monotonic()
                run_id = f"cron-{int(run_started * 1000)}"
                ready_count = -1
                repo = getattr(self.orchestrator, "story_repository", None)
                if repo is not None and hasattr(repo, "list_stories_ready_for_clustering"):
                    try:
                        ready_count = len(repo.list_stories_ready_for_clustering())
                    except Exception:
                        ready_count = -1
                logger.info(
                    "cluster.cron_run_start run_id=%s ready_count=%s min_size_guard=%s",
                    run_id,
                    ready_count,
                    self.min_size_guard,
                    extra={
                        "run_id": run_id,
                        "ready_count": ready_count,
                        "min_size_guard": self.min_size_guard,
                    },
                )
                try:
                    issue_ids = self.orchestrator.process_all_pending()
                    elapsed_ms = int((monotonic() - run_started) * 1000)
                    logger.info(
                        "cluster.cron_run_end run_id=%s ready_count=%s processed_count=%s created_issue_count=%s failed_count=%s duration_ms=%s",
                        run_id,
                        ready_count,
                        len(issue_ids),
                        len(issue_ids),
                        0,
                        elapsed_ms,
                        extra={
                            "run_id": run_id,
                            "ready_count": ready_count,
                            "processed_count": len(issue_ids),
                            "created_issue_count": len(issue_ids),
                            "failed_count": 0,
                            "duration_ms": elapsed_ms,
                            "last_story_id": "-",
                            "last_cluster_id": "-",
                            "issued_count": len(issue_ids),
                            "issue_ids": issue_ids,
                            "min_size_guard": self.min_size_guard,
                        },
                    )
                except Exception as exc:  # noqa: BLE001
                    elapsed_ms = int((monotonic() - run_started) * 1000)
                    log_runtime_exception(
                        logger,
                        exc,
                        stage="cluster.cron",
                        run_id=run_id,
                        duration_ms=elapsed_ms,
                    )
                    logger.info(
                        "cluster.cron_run_end run_id=%s ready_count=%s processed_count=%s created_issue_count=%s failed_count=%s duration_ms=%s",
                        run_id,
                        ready_count,
                        0,
                        0,
                        1,
                        elapsed_ms,
                        extra={
                            "run_id": run_id,
                            "ready_count": ready_count,
                            "processed_count": 0,
                            "created_issue_count": 0,
                            "failed_count": 1,
                            "duration_ms": elapsed_ms,
                            "last_story_id": "-",
                            "last_cluster_id": "-",
                        },
                    )
