## Task workspace — `task-gw-l10n-02-t08-reproject-backfill-original-locale-assertion`

- Story: [`../STORY-GW-L10N-02-original-locale-in-public-projection.md`](../STORY-GW-L10N-02-original-locale-in-public-projection.md)
- Depends on: T04 (reproject backfill path), T01–T02 (`original_locale` in bridge + public dict)
- Decision Ref: [`../../../../../../analysis/audit-gw-l10n-02-original-locale-2026-06-15.md`](../../../../../../analysis/audit-gw-l10n-02-original-locale-2026-06-15.md) §3 G1

---
**Priority:** P1  
**Complexity:** S  
**Estimate:** ~30 min  
**Status:** 🟢 Done  
**Wave:** audit override (`run_mode=gw_l10n_02_audit_followup`)  
**Skill declared:** python-pro  
---

## Task: tests — reproject backfill asserts `original_locale`

### Цель
Зафиксировать тестом, что `run_reproject` write path сохраняет `original_locale` в `payload_json` из linked stories (канонический порядок `et`, `ru`, `en`).

### Почему это важно (риск)
Backfill мутирует все linked issue ([`scripts/reproject_issue_i18n.py`](../../../../../../../scripts/reproject_issue_i18n.py) L170–180 через `bridge.build_projection_input`). Без assertion на `original_locale` регрессия G1 не будет поймана на reproject-пути (audit §3 G1).

### Факты из кода
1. [`scripts/reproject_issue_i18n.py`](../../../../../../../scripts/reproject_issue_i18n.py) L170–180 — `bridge.build_projection_input` → `to_public_dict()`.
2. [`issue_create.py:155-163`](../../../../../../../src/core/application/issue_create.py#L155-L163) — `original_locale_from_languages` по всем `cluster_stories`.
3. [`tests/test_reproject_issue_i18n.py`](../../../../../../../tests/test_reproject_issue_i18n.py) L146–150 — assertions только на `title`; `grep original_locale` = 0.
4. [`intake_v2_fixtures.py:101`](../../../../../../../tests/intake_v2_fixtures.py) — default `narrative_language="en"`; существующий write-тест не покрывает mixed `et`+`ru`.

### Gap / Проблема
**G1 (audit):** reproject backfill без assertion на `original_locale` в saved payload.

### AC/DoD
- [x] (P0) sqlite roundtrip: linked stories с `narrative_language` `et` + `ru` → после `run_reproject(..., dry_run=False)` в saved payload `original_locale == ["et", "ru"]`.
- [x] (P0) `grep original_locale` в `tests/test_reproject_issue_i18n.py` ≥ 1 assertion.
- [x] (P1) существующие 3 reproject-теста остаются green.
- [x] (P1) `python3 -m pytest -q tests/test_reproject_issue_i18n.py` green.

### Где менять код
- [`tests/test_reproject_issue_i18n.py`](../../../../../../../tests/test_reproject_issue_i18n.py) — новый тест или расширение write-теста

### Out of scope
- Новый pkg / смена [`gateway-active-package.current.yaml`](../../../../../../gateway-active-package.current.yaml)
- Изменение [`scripts/reproject_issue_i18n.py`](../../../../../../../scripts/reproject_issue_i18n.py) (если тест достаточен)
- Live Supabase integration test

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_reproject_issue_i18n.py
```
