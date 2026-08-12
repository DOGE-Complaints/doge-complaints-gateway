## Task workspace — `task-m2-04-05-t06-orchestrator-canonical-projection-wire`

- Story: [`../STORY-M2-04-05-civic-canonical-signal-pipeline.md`](../STORY-M2-04-05-civic-canonical-signal-pipeline.md)
- Decision Ref: REQ-34 §3 (`cluster_orchestrator.py`); gap-interview G-09 cascade
- Depends on: T02 (signal API), T04 (projection), T05 (gate)

## Task: implement — orchestrator wires canonical signals and cluster stories to issue create

### Цель
Упростить signal cache policy до canonical-only; перед `create_issue` загрузить member stories, выбрать dominant, передать в projection bridge; убрать `signal_source` branching.

### Факты из кода
1. [`src/core/application/cluster_orchestrator.py`](../../../../../../../src/core/application/cluster_orchestrator.py) L22–30 — `_signal_policy` maps keyword/hybrid.
2. L48 — `get_signals_for_story(story, signal_source)`.
3. L240–246 — `IssueCreateCommand` без dominant/canonical context; bridge uses keyword aggregate text only.
4. [`src/core/cluster/engine.py`](../../../../../../../src/core/cluster/engine.py) L177 — `signal_source: str = "canonical"` field on engine.

### Gap / Проблема
Orchestrator still supports deprecated signal modes and does not pass cluster stories for canonical projection (G-09 cascade table).

### AC/DoD
- [x] (P0) `_get_or_compute_signals` uses canonical-only policy key (e.g. `v2.canonical` only).
- [x] (P0) `_create_issue_for_cluster` loads all `member_story_ids` records and calls updated bridge/policy from T04.
- [x] (P0) Promotion gate from T05 receives canonical types for member stories.
- [x] (P1) Remove dead `_signal_policy` branches for `keyword`/`hybrid`/`narrative`.
- [x] (P1) `tests/test_story_cluster_orchestrator.py` updated mocks for new `get_signals_for_story` signature.

### Где менять код
- [`src/core/application/cluster_orchestrator.py`](../../../../../../../src/core/application/cluster_orchestrator.py)
- [`tests/test_story_cluster_orchestrator.py`](../../../../../../../tests/test_story_cluster_orchestrator.py)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_story_cluster_orchestrator.py tests/test_e2e_story_cluster_issue_pipeline.py -q --tb=short
```
