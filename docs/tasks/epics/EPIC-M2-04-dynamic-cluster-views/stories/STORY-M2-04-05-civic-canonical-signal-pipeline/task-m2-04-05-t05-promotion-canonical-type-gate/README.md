## Task workspace — `task-m2-04-05-t05-promotion-canonical-type-gate`

- Story: [`../STORY-M2-04-05-civic-canonical-signal-pipeline.md`](../STORY-M2-04-05-civic-canonical-signal-pipeline.md)
- Decision Ref: REQ-34 §2.4; gap-interview G-04 gate logic

## Task: implement — promotion readiness gate on canonical_type

### Цель
Не промотировать кластер в Issue, если ни у одной story нет `narrative_canonical_type` в `{complaint, system_bug}` (REQ-34 readiness gate).

### Факты из кода
1. [`src/core/promotion/gates.py`](../../../../../../../src/core/promotion/gates.py) L14–31 — только `min_readiness_score` и `min_stories`.
2. [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py) — `StoryRecord.narrative_canonical_type: str | None`.
3. Intake test accepts `canonical_type: "complaint"` ([`tests/test_story_intake_contract.py`](../../../../../../../tests/test_story_intake_contract.py)); many fixtures use `"infrastructure"` — gate allowlist must match product decision in REQ-34, not fixture vocabulary.

### Gap / Проблема
Clusters of weakly typed observations promote to SPA noise (G-04 gate, REQ-34 §2.4).

### AC/DoD
- [x] (P0) `evaluate_promotion_gates` (or wrapper) rejects when no story in cluster has `canonical_type` in allowlist `{complaint, system_bug}` (normalize case/strip).
- [x] (P0) Reason code documented, e.g. `no_actionable_canonical_type`.
- [x] (P0) Test: cluster stories all `observation` (or `infrastructure` if not in allowlist) → gate `passed=False`.
- [x] (P0) Test: at least one `complaint` → gate can pass (other gates permitting).
- [x] (P1) Orchestrator / promotion service passes story records or canonical types into gate evaluator.

### Где менять код
- [`src/core/promotion/gates.py`](../../../../../../../src/core/promotion/gates.py)
- [`src/core/promotion/service.py`](../../../../../../../src/core/promotion/service.py) or call sites — wire story lookup
- [`tests/test_promotion_gates.py`](../../../../../../../tests/test_promotion_gates.py) or new test module

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/ -q --tb=short -k promotion_gate
```
