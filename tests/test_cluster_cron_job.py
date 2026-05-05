from __future__ import annotations

from dataclasses import dataclass
from time import sleep
from typing import cast

from core.application import StoryClusterOrchestrator
from core.scheduler import ClusterCronJob


@dataclass
class _Repo:
    ready_count: int = 0

    def list_stories_ready_for_clustering(self) -> list[object]:
        return [object() for _ in range(self.ready_count)]


class _OrchestratorStub:
    def __init__(self, repo: _Repo, *, issue_ids: list[str] | None = None) -> None:
        self.story_repository = repo
        self.calls = 0
        self.issue_ids = issue_ids if issue_ids is not None else ["issue-1"]

    def process_all_pending(self) -> list[str]:
        self.calls += 1
        return list(self.issue_ids)


def test_cluster_cron_job_start_stop_runs_loop() -> None:
    repo = _Repo(ready_count=2)
    orchestrator = _OrchestratorStub(repo)
    job = ClusterCronJob(
        orchestrator=cast(StoryClusterOrchestrator, orchestrator),
        interval_s=1,
        min_size_guard=2,
    )
    job.start()
    sleep(1.2)
    job.stop()
    assert orchestrator.calls >= 1


def test_cluster_cron_job_respects_min_size_guard() -> None:
    repo = _Repo(ready_count=1)
    orchestrator = _OrchestratorStub(repo, issue_ids=[])
    job = ClusterCronJob(
        orchestrator=cast(StoryClusterOrchestrator, orchestrator),
        interval_s=1,
        min_size_guard=2,
    )
    job.start()
    sleep(1.2)
    job.stop()
    # Cron no longer pre-checks repository size; min-size guard is handled
    # inside StoryClusterOrchestrator.process_all_pending().
    assert orchestrator.calls >= 1


def test_cluster_cron_job_start_is_idempotent() -> None:
    repo = _Repo(ready_count=2)
    orchestrator = _OrchestratorStub(repo)
    job = ClusterCronJob(
        orchestrator=cast(StoryClusterOrchestrator, orchestrator),
        interval_s=1,
        min_size_guard=2,
    )
    job.start()
    job.start()
    sleep(1.2)
    job.stop()
    assert orchestrator.calls >= 1
