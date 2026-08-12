## Task workspace — `task-m2-06-06-t04-factory-di-read-store-wiring`

- Story: [`../STORY-M2-06-06-tallinn-issues-read-api-req24.md`](../STORY-M2-06-06-tallinn-issues-read-api-req24.md)
- Decision Ref: REQ-24 §5; GAP-24-04

---
**Приоритет:** P0  
**Сложность:** S  
**Оценка времени:** ~45 min  
**Статус:** ready  
**Wave:** `pkg-000019`  
---

## Task: implement — factory and DI read store wiring

### Цель
Провести `IssueProjectionReadStore` через `ServiceFactory` → `build_api_dependencies()` → `ApiDependencies`.

### Факты из кода
1. [`factory.py`](../../../../../../../src/core/application/factory.py) — `get_issue_projection_service`, нет `get_issue_projection_store` для read.
2. [`service_factory.py`](../../../../../../../src/core/infrastructure/service_factory.py) L55 — `issue_projection_store` (write).
3. [`dependencies.py`](../../../../../../../src/core/api/dependencies.py) — `ApiDependencies` без `issue_projection_read_store`.
4. REQ-24 §5.2 — `get_issue_projection_store() -> IssueProjectionReadStore` (имя в REQ; write store уже `IssueProjectionStore` — read может reuse same instance if stores implement both).

### Gap / Проблема
**GAP-24-04:** handlers не получают read store через DI.

### AC/DoD
- [ ] (P0) `ServiceFactory` Protocol + `DefaultServiceFactory.get_issue_projection_read_store()` (или alias к write store instance implementing read methods).
- [ ] (P0) `ApiDependencies.issue_projection_read_store: IssueProjectionReadStore`.
- [ ] (P0) `build_api_dependencies()` заполняет поле для in_memory / sqlite / supabase.
- [ ] (P1) Test `build_api_dependencies()` не падает.

### Где менять код
- [`src/core/application/factory.py`](../../../../../../../src/core/application/factory.py)
- [`src/core/infrastructure/service_factory.py`](../../../../../../../src/core/infrastructure/service_factory.py)
- [`src/core/api/dependencies.py`](../../../../../../../src/core/api/dependencies.py)
- [`src/core/infrastructure/providers.py`](../../../../../../../src/core/infrastructure/providers.py) (если нужен wiring)

### Out of scope
- Handlers (T05)
- Store method bodies (T02–T03)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -c "from core.api.dependencies import build_api_dependencies; d=build_api_dependencies(); assert hasattr(d,'issue_projection_read_store'); print('ok')"
```
