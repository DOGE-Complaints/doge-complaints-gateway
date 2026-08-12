## Task workspace — `task-gw-l10n-01-t02-manual-post-preserve-i18n-title`

- Story: [`../STORY-GW-L10N-01-projection-content-i18n-preservation.md`](../STORY-GW-L10N-01-projection-content-i18n-preservation.md)
- Depends on: T01 (cluster projection path shares extraction_policy)
- Decision Ref: backlog T02; parent AC «Манульный POST сохраняет i18n-title»

---
**Priority:** P0  
**Complexity:** S  
**Estimate:** ~45 min  
**Status:** ready  
**Wave:** `pkg-000027`  
**Skill declared:** python-pro  
---

## Task: fix — manual `POST /tallinn/issues` preserve i18n title

### Цель
Манульный `POST /tallinn/issues`: сохранять переданный i18n-`title` без флэттена через `_promoted_title_from_i18n` только.

### Факты из кода
1. [`issue_create.py`](../../../../../../../src/core/application/issue_create.py) L353–382 — `create_manual_issue` принимает `title: dict[str, object]`.
2. L376 — `promoted_title = _promoted_title_from_i18n(title)` схлопывает в одну строку.
3. L378–382 — `bridge.build_projection_input(promoted_title=...)` теряет per-locale title.
4. [`handlers.py`](../../../../../../../src/core/api/handlers.py) L411 — вызывает `create_manual_issue`.
5. [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) L378 — `POST /tallinn/issues`.

### AC/DoD
- [ ] (P0) Сохранённый `payload_json.title` отражает переданный i18n dict (разные et/en когда переданы разные значения).
- [ ] (P0) `promoted_title` string по-прежнему используется для bridge aggregate path где нужно.
- [ ] (P1) Валидация title dict без регрессий.

### Где менять код
- [`src/core/application/issue_create.py`](../../../../../../../src/core/application/issue_create.py) `create_manual_issue`

### Out of scope
- OpenAPI handler schema change beyond behavior (T05)
- Backfill (T03)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_req24_tallinn_issues_read_api.py -k manual 2>/dev/null || true
```
