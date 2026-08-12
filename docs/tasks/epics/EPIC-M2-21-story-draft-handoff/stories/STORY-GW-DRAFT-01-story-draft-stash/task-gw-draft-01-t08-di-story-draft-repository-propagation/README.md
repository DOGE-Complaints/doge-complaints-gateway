# task-gw-draft-01-t08-di-story-draft-repository-propagation

## Meta
- **Story:** [STORY-GW-DRAFT-01](../STORY-GW-DRAFT-01-story-draft-stash.md)
- **Type:** fix (tests)
- **Status:** 🟢 Done
- **Package:** audit override (not in pkg-000043)
- **Skill declared:** python-pro
- **Wave:** audit override (`run_mode=gw_draft_01_audit_followup`)
- **Depends on:** T02 (structural DI change)
- **Audit ref:** [`audit-gw-draft-01-story-draft-stash-2026-07-03`](../../../../../../analysis/audit-gw-draft-01-story-draft-stash-2026-07-03.md) **R1**

## Purpose
Восстановить зелёный `test_di_service_factory.py` после добавления обязательного поля `story_draft_repository` в `DefaultServiceFactory` (change-propagation miss T02).

## Code Facts
- `DefaultServiceFactory.story_draft_repository` — обязательное поле без default — [`service_factory.py:51`](../../../../../../../src/core/infrastructure/service_factory.py#L51)
- `_factory()` в тестах не передаёт `story_draft_repository` — [`tests/test_di_service_factory.py:15-25`](../../../../../../../tests/test_di_service_factory.py#L15)
- Симптом: `TypeError: __init__() missing 1 required positional argument: 'story_draft_repository'` во **всех 10** тестах файла
- Fix: импорт `InMemoryStoryDraftRepository` из [`repositories.py`](../../../../../../../src/core/infrastructure/repositories.py), передать в `DefaultServiceFactory(...)`
- Единственный прямой вызов `DefaultServiceFactory(...)` в тестах — этот файл (grep)

## Acceptance / DoD
- `pytest -q tests/test_di_service_factory.py` → 10 passed
- Production-код **не** менять (только тесты)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P6)

## Where to change
- [`tests/test_di_service_factory.py`](../../../../../../../tests/test_di_service_factory.py)

## Out of scope
Story gate full-unit (T09); GW-DRAFT-02 user-auth (G1)

## Verification commands
```bash
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_di_service_factory.py
```
