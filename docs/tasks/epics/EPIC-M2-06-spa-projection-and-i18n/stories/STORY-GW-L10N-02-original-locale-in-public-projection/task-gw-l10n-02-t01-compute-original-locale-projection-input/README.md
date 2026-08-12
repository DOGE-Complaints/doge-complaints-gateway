# task-gw-l10n-02-t01

## Meta
- **Story:** [STORY-GW-L10N-02](../STORY-GW-L10N-02-original-locale-in-public-projection.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000028
- **Skill declared:** python-pro

## Purpose
Вычислять `original_locale` = уникальные `narrative_language` по всем `cluster_stories` в каноническом порядке `et`, `ru`, `en`; прокинуть в `ProjectionInput` и draft builder.

## Code Facts
- `src/core/projection/input.py:8-30` — `ProjectionInput` без `original_locale`
- `src/core/application/issue_create.py:127-160` — `StoryPromotionProjectionBridge`, `cluster_stories`
- `src/core/projection/extraction_policy.py:157+` — `build_projection_input_from_draft`
- `src/core/domain/contracts.py:53` — `StoryRecord.narrative_language`

## Acceptance / DoD
- Traces: AC2 (dedup+order); AC3 (omit when none)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- Новый helper (напр. в `extraction_policy.py` или `i18n.py`) — collect unique locales
- `ProjectionInput` — поле `original_locale: tuple[str, ...]` или `list[str]`
- `issue_create.py` bridge — передать вычисленное значение
- `build_projection_input_from_draft` — propagate

## Verification commands
```bash
Unit test helper + bridge wiring (T06); manual smoke после T02
```
