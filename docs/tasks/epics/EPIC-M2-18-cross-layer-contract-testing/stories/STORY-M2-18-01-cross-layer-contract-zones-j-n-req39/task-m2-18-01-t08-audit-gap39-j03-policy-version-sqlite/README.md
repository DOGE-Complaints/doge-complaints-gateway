## Task workspace — `task-m2-18-01-t08-audit-gap39-j03-policy-version-sqlite`

- Story: [`../STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md`](../STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md)
- Decision Ref: [`../../../../../../analysis/audit-req39-cross-layer-contract-testing-2026-05-18.md`](../../../../../../analysis/audit-req39-cross-layer-contract-testing-2026-05-18.md) §6 GAP-39-J03-PRIVATE; Zone J

---
**Приоритет:** P2  
**Сложность:** S  
**Оценка времени:** ~1 ч  
**Статус:** ready  
**Wave:** audit override (`run_mode=story18_audit_req39_followup`)  
---

## Task: tests — J-03 policy_version without private `_rows` access

### Цель
Заменить хрупкий доступ `getattr(store, "_rows")` в `test_j03_new_issue_has_m3_policy_version` на проверку через SQLite store (или иной публичный контракт).

### Почему это важно (риск)
Смена внутренней структуры `InMemoryIssueProjectionStore` ломает тест без изменения поведения pipeline; `policy_version` не возвращается через `list_projections()`.

### Факты из кода
1. [`test_clustering_pipeline_contract.py`](../../../../../../../tests/test_clustering_pipeline_contract.py) L72–76 — `test_j03_new_issue_has_m3_policy_version` читает `_rows`.
2. Аудит рекомендует **Вариант B:** SQLite roundtrip `SELECT policy_version FROM doge_issues`.

### Gap / Проблема
**AUDIT-GAP-39-J03-PRIVATE:** implementation brittleness on in-memory private dict.

### AC/DoD
- [ ] (P0) J-03 assert `policy_version == "m3.doge_issue_derivation.v1"` через SQLite-backed path (или эквивалент без `_rows`).
- [ ] (P1) InMemory-only path для J-03 удалён или помечен deprecated в комментарии — предпочтение SQLite в contract suite.
- [ ] (P0) `tests/test_clustering_pipeline_contract.py` green.

### Где менять код
- [`tests/test_clustering_pipeline_contract.py`](../../../../../../../tests/test_clustering_pipeline_contract.py)

### Out of scope
- Добавление `get_policy_version()` в Protocol (дорого; только если SQLite path недостаточен).
- `pkg-000020` edits.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_clustering_pipeline_contract.py -k j03
```
