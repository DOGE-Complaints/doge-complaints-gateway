## Task workspace — `task-m2-02-07-t02-domain-storyrecord-v2-fields`

- Story: [`../STORY-M2-02-07-multilingual-intake-contract-v2.md`](../STORY-M2-02-07-multilingual-intake-contract-v2.md)
- Decision Ref: REQ-33 §3; gap-interview G-01

## Task: implement — StoryRecord v2 fields and service mapping

### Цель
Согласовать доменную модель и `StoryIntakeService.create_story` с v2 narrative: dict-поля title/description/summary/session_language; `submitter_identity_issuer: str` без `None`.

### Факты из кода
1. [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py) — `narrative_title_hint` + `narrative_title_hint_et/ru/en`; `submitter_identity_issuer: str | None`.
2. [`src/core/application/services.py`](../../../../../../../src/core/application/services.py) — маппинг в `create_story` из `request.narrative.title_hint*` (около L144–147).

### Gap / Проблема
Intake v2 без смены `StoryRecord` не сохранит description/session_language и оставит optional eID.

### AC/DoD
- [ ] (P0) `StoryRecord`: `narrative_title`, `narrative_description`, `narrative_summary` (optional), `narrative_session_language`; удалены `narrative_title_hint*`.
- [ ] (P0) `submitter_identity_issuer: str` (NOT NULL в домене).
- [ ] (P0) `create_story` / update paths маппят v2 `Narrative` → `StoryRecord`.
- [ ] (P1) Зависимые read paths (`cluster_orchestrator`, логи) не ссылаются на удалённые поля без правки.

### Где менять код
- [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py)
- [`src/core/application/services.py`](../../../../../../../src/core/application/services.py)
- при необходимости [`src/core/application/cluster_orchestrator.py`](../../../../../../../src/core/application/cluster_orchestrator.py)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_story_repository_lifecycle.py tests/test_issue_create_service.py -q --tb=short
```
