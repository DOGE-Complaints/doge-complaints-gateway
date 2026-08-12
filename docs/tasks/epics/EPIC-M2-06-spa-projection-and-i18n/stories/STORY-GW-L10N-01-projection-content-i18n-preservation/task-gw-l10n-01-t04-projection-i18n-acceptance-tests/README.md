## Task workspace — `task-gw-l10n-01-t04-projection-i18n-acceptance-tests`

- Story: [`../STORY-GW-L10N-01-projection-content-i18n-preservation.md`](../STORY-GW-L10N-01-projection-content-i18n-preservation.md)
- Depends on: T01, T02
- Decision Ref: backlog T04

---
**Priority:** P0  
**Complexity:** M  
**Estimate:** ~1 h  
**Status:** ready  
**Wave:** `pkg-000027`  
**Skill declared:** python-pro  
---

## Task: tests — projection i18n distinguishability and fallback

### Цель
Acceptance-тесты: проекция кластера, где истории имеют разный текст по локалям → `title.et != title.en` при реально разном контенте; fallback при отсутствии i18n.

### Факты из кода
1. [`test_story_promotion_projection_bridge.py`](../../../../../../../tests/test_story_promotion_projection_bridge.py) — mock `build_draft`.
2. [`test_unit_domain_flows_supabase_wave.py`](../../../../../../../tests/test_unit_domain_flows_supabase_wave.py) L60–69 — `DeterministicStoryToProjectionPolicy().build_draft` без i18n assert.
3. [`tests/intake_v2_fixtures.py`](../../../../../../../tests/intake_v2_fixtures.py) — `make_story_record` helper.

### AC/DoD
- [ ] (P0) Тест: dominant story с разным `narrative_title` по et/en → projection `title.et != title.en`.
- [ ] (P0) Тест: отсутствие narrative_title → fallback (все три локали равны promoted string).
- [ ] (P0) Manual create path: i18n title preserved (если не покрыто в T02 acceptance).
- [ ] (P1) `python3 -m pytest tests/ -q --ignore=tests/smoke --ignore=tests/integration` green.

### Где менять код
- [`tests/test_story_promotion_projection_bridge.py`](../../../../../../../tests/test_story_promotion_projection_bridge.py)
- [`tests/test_unit_domain_flows_supabase_wave.py`](../../../../../../../tests/test_unit_domain_flows_supabase_wave.py)
- При необходимости: [`tests/test_issue_create_service.py`](../../../../../../../tests/test_issue_create_service.py)

### Out of scope
- Live Supabase integration
- Docs (T05)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_story_promotion_projection_bridge.py tests/test_unit_domain_flows_supabase_wave.py
python3 -m pytest tests/ -q --ignore=tests/smoke --ignore=tests/integration
```
