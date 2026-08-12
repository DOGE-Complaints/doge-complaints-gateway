## Task workspace — `task-gw-l10n-01-t01-extraction-policy-dominant-i18n`

- Story: [`../STORY-GW-L10N-01-projection-content-i18n-preservation.md`](../STORY-GW-L10N-01-projection-content-i18n-preservation.md)
- Decision Ref: backlog T01; D-L10N-1; partial i18n = dominant only + fallback

---
**Priority:** P0  
**Complexity:** M  
**Estimate:** ~1 h  
**Status:** ready  
**Wave:** `pkg-000027`  
**Skill declared:** python-pro  
---

## Task: implement — dominant story i18n in `build_draft`

### Цель
В `build_draft` / `build_projection_input_from_draft` прокинуть i18n-контент доминантной истории вместо `_to_i18n(promoted_title)`; сохранить fallback на текущее поведение, если у истории нет валидного i18n.

### Факты из кода
1. [`extraction_policy.py`](../../../../../../../src/core/projection/extraction_policy.py) L124–143 — `DeterministicStoryToProjectionPolicy.build_draft` вызывает `_to_i18n` для title/summary/description.
2. L172–176 — `_to_i18n(text)` копирует одну строку в et/ru/en.
3. `dominant_story: StoryRecord` уже в сигнатуре `build_draft` (L129).
4. `StoryRecord.narrative_title` / `narrative_description` / `narrative_summary` — `dict[str, str] | None` ([`contracts.py`](../../../../../../../src/core/domain/contracts.py) L54–56).

### Product decision (fixed)
- Источник: **только** `dominant_story`; пустые слоты → `_to_i18n(promoted_title)` / aggregate fallback; **без** merge из `cluster_stories`.

### AC/DoD
- [ ] (P0) `title`/`summary`/`description` в `StoryProjectionDraft` берутся из `dominant_story` i18n dicts когда валидны.
- [ ] (P0) При отсутствии/пустом i18n — текущий `_to_i18n` fallback (без исключений).
- [ ] (P1) `build_projection_input_from_draft` без изменений контракта полей `{et,ru,en}`.

### Где менять код
- [`src/core/projection/extraction_policy.py`](../../../../../../../src/core/projection/extraction_policy.py)

### Out of scope
- `issue_create.py` manual path (T02)
- Tests (T04)
- Backfill script (T03)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -c "from core.projection.extraction_policy import DeterministicStoryToProjectionPolicy; print('import ok')"
```
