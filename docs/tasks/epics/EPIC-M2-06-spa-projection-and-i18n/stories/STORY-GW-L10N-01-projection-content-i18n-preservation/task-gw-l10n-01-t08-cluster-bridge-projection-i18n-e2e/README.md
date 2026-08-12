## Task workspace — `task-gw-l10n-01-t08-cluster-bridge-projection-i18n-e2e`

- Story: [`../STORY-GW-L10N-01-projection-content-i18n-preservation.md`](../STORY-GW-L10N-01-projection-content-i18n-preservation.md)
- Depends on: T01, T04
- Decision Ref: [`../../../../../../analysis/audit-gw-l10n-01-projection-content-i18n-2026-06-15.md`](../../../../../../analysis/audit-gw-l10n-01-projection-content-i18n-2026-06-15.md) §3 G2

---
**Priority:** P1  
**Complexity:** S  
**Estimate:** ~45 min  
**Status:** ready  
**Wave:** audit override (`run_mode=gw_l10n_01_audit_followup`)  
**Skill declared:** python-pro  
---

## Task: tests — cluster bridge projection i18n E2E

### Цель
E2E-тест основного кластерного пути: `StoryPromotionProjectionBridge.build_projection_input` с несколькими stories → `IssueProjectionService.project` → `to_public_dict()` с различимыми per-locale title.

### Почему это важно (риск)
T04 покрывает `build_draft` (unit) и manual-create, но не сквозной bridge path для multi-story cluster (audit G2). Риск низкий (тот же `build_draft`), но не verified тестом.

### Факты из кода
1. [`issue_create.py:126-159`](../../../../../../../src/core/application/issue_create.py#L126-L159) — `StoryPromotionProjectionBridge.build_projection_input`.
2. [`extraction_policy.py:141-152`](../../../../../../../src/core/projection/extraction_policy.py#L141-L152) — i18n из `dominant_story`.
3. [`test_gw_l10n_01_projection_i18n.py`](../../../../../../../tests/test_gw_l10n_01_projection_i18n.py) — unit `build_draft` + manual path; **нет** multi-story bridge assert.
4. [`test_story_promotion_projection_bridge.py`](../../../../../../../tests/test_story_promotion_projection_bridge.py) — bridge tests без per-locale distinguishability assert.
5. [`tests/intake_v2_fixtures.py`](../../../../../../../tests/intake_v2_fixtures.py) — `make_story_record`, `narrative_dict`.

### Gap / Проблема
**G2 (audit):** cluster promotion path не утверждает `title.et != title.en` на публичной проекции.

### AC/DoD
- [ ] (P0) 2+ stories в repo; dominant с разным `narrative_title` et/en → `bridge.build_projection_input` → `title.et != title.en`.
- [ ] (P0) `IssueProjectionService.project` → `to_public_dict()` сохраняет различимость в `title`.
- [ ] (P1) `python3 -m pytest -q tests/test_gw_l10n_01_projection_i18n.py` (или bridge test file) green.
- [ ] (P1) Full unit suite без регрессий.

### Где менять код
- [`tests/test_gw_l10n_01_projection_i18n.py`](../../../../../../../tests/test_gw_l10n_01_projection_i18n.py) (preferred)
- Альтернатива: [`tests/test_story_promotion_projection_bridge.py`](../../../../../../../tests/test_story_promotion_projection_bridge.py)

### Out of scope
- Live cron/cluster orchestrator HTTP E2E
- `original_locale` (GW-L10N-02)
- Новый pkg

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_l10n_01_projection_i18n.py -k bridge
python3 -m pytest tests/ -q --ignore=tests/smoke --ignore=tests/integration
```
