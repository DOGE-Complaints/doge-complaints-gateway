## Task workspace — `task-m2-04-05-t04-canonical-issue-type-and-labels`

- Story: [`../STORY-M2-04-05-civic-canonical-signal-pipeline.md`](../STORY-M2-04-05-civic-canonical-signal-pipeline.md)
- Decision Ref: REQ-34 §2.5; gap-interview G-09
- Dependency: REQ-36 — interim `select_dominant_story(stories)` until `alpha_score()` exists

## Task: implement — issue type and labels from canonical cluster stories

### Цель
Заменить keyword `_derive_issue_type` / `_derive_labels` на чтение `narrative_canonical_type` dominant story и union `narrative_canonical_labels` всех stories кластера.

### Факты из кода
1. [`src/core/projection/extraction_policy.py`](../../../../../../../src/core/projection/extraction_policy.py) L46–47, L81–100 — keyword corpus matching (EN-biased).
2. [`src/core/projection/enums.py`](../../../../../../../src/core/projection/enums.py) L14–19 — `DOGEIssueType`: `IMPROVEMENT`, `SERVICE_REQUEST`, `INCIDENT`.
3. [`src/core/application/issue_create.py`](../../../../../../../src/core/application/issue_create.py) `StoryPromotionProjectionBridge.build_projection_input` — передаёт только `promoted_title` + `story_ids`, aggregate text keyword path.
4. Gap-interview §G-09 names `issue_create.py`; verified SSOT for derive helpers is `extraction_policy.py`.

### Gap / Проблема
ET/RU clusters get default `IMPROVEMENT` / empty labels despite GPT canonical fields on `StoryRecord` (G-09).

### AC/DoD
- [x] (P0) Удалены `_derive_issue_type` / `_derive_labels` keyword helpers.
- [x] (P0) `StoryToProjectionPolicy.build_draft` (or successor) accepts `dominant_story: StoryRecord` and `cluster_stories: tuple[StoryRecord, ...]`.
- [x] (P0) `issue_type` = mapped `dominant_story.narrative_canonical_type` with fallback documented (e.g. `observation` → `IMPROVEMENT` per enum map in task acceptance).
- [x] (P0) `labels` = `list(dict.fromkeys(...))` over all `narrative_canonical_labels` (order preserved, no top-N cap).
- [x] (P1) `select_dominant_story(stories)` helper with interim heuristic: max `len(canonical_labels)`, tie-break `story_id`; document REQ-36 replacement.
- [x] (P1) Unit tests for ET/RU labels union without English words in narrative text.

### Где менять код
- [`src/core/projection/extraction_policy.py`](../../../../../../../src/core/projection/extraction_policy.py)
- [`src/core/application/issue_create.py`](../../../../../../../src/core/application/issue_create.py) — bridge passes stories into policy
- New tests under `tests/test_projection_canonical_derivation.py` or extend existing projection tests

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_story_promotion_projection_bridge.py tests/test_unit_domain_flows_supabase_wave.py -q --tb=short -k projection
```
