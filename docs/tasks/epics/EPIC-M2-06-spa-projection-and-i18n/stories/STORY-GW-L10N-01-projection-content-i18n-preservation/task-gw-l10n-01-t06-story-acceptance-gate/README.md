## Task workspace — `task-gw-l10n-01-t06-story-acceptance-gate`

- Story: [`../STORY-GW-L10N-01-projection-content-i18n-preservation.md`](../STORY-GW-L10N-01-projection-content-i18n-preservation.md)
- Depends on: T01–T05
- Decision Ref: parent AC verbatim; [`story-acceptance-gate-STORY-GW-L10N-01.md`](../story-acceptance-gate-STORY-GW-L10N-01.md)

---
**Priority:** P0  
**Complexity:** S  
**Estimate:** ~30 min  
**Status:** ready  
**Wave:** `pkg-000027`  
**Skill declared:** python-pro  
---

## Task: tests — story parent acceptance gate (STORY-GW-L10N-01)

### Цель
Закрыть story parent AC: проверить все пункты Acceptance Criteria из backlog; заполнить `story-acceptance-gate-STORY-GW-L10N-01.md`; обновить bullrun story row.

### AC/DoD
- [ ] (P0) Все 5 parent AC из backlog — PASS с evidence (T01–T05).
- [ ] (P0) `story-acceptance-gate-STORY-GW-L10N-01.md` → Result PASS + date.
- [ ] (P0) `builder_resolve_queue.py --project gateway --verify` → `ok 6 paths`.
- [ ] (P1) Unit suite green: `pytest tests/ -q --ignore=tests/smoke --ignore=tests/integration`.

### Где менять
- [`story-acceptance-gate-STORY-GW-L10N-01.md`](../story-acceptance-gate-STORY-GW-L10N-01.md)
- [`bullrun-launch-index.md`](../../../../bullrun-launch-index.md) — story row STORY-GW-L10N-01

### Out of scope
- Epic AC gate (отдельный шаг после story)

### Команды проверки
```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest tests/ -q --ignore=tests/smoke --ignore=tests/integration
```
