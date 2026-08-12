## Task workspace — `task-m2-18-02-t09-zone-d-story-repository-contract`

- Story: [`../STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md`](../STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md)
- Decision Ref: [`../../../../../../requirements/39-cross-layer-contract-testing.md`](../../../../../../requirements/39-cross-layer-contract-testing.md) — Zone **D**

---
**Приоритет:** P1  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000020`  
---

## Task: tests — StoryRepository protocol — 3 implementations parity

### Цель
StoryRepository protocol — 3 implementations parity (Zone **D**). Offline contract tests per REQ-39.

### Факты из кода
1. `StoryRepository` Protocol — `domain/contracts.py` / `repositories.py`.
2. InMemory, Sqlite, Supabase implementations.

### Gap / Проблема
In-memory lacks SQL constraints; cross-backend parity untested.

### AC/DoD
- [x] (P0) D-01..D-04 parametrized per REQ-39 §D.
- [x] (P1) SQLite in-memory URL; Supabase optional skip in contract file.

### Где менять код
- `tests/test_story_repository_contract.py` (new)

### Out of scope
Live Supabase required tests.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_story_repository_contract.py
```
