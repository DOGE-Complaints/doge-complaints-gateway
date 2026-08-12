## Task workspace — `task-gw-l10n-01-t07-reproject-script-autotests`

- Story: [`../STORY-GW-L10N-01-projection-content-i18n-preservation.md`](../STORY-GW-L10N-01-projection-content-i18n-preservation.md)
- Depends on: T03 (script exists)
- Decision Ref: [`../../../../../../analysis/audit-gw-l10n-01-projection-content-i18n-2026-06-15.md`](../../../../../../analysis/audit-gw-l10n-01-projection-content-i18n-2026-06-15.md) §3 G1

---
**Priority:** P1  
**Complexity:** M  
**Estimate:** ~1 h  
**Status:** ready  
**Wave:** audit override (`run_mode=gw_l10n_01_audit_followup`)  
**Skill declared:** python-pro  
---

## Task: tests — `reproject_issue_i18n.py` dry-run and sqlite roundtrip

### Цель
Автотесты для one-off backfill-скрипта: dry-run не пишет в store; write обновляет `payload_json` per-locale из dominant story; повторный прогон идемпотентен.

### Почему это важно (риск)
Скрипт мутирует `doge_issues.payload_json` на всех linked issue ([`scripts/reproject_issue_i18n.py`](../../../../../../../scripts/reproject_issue_i18n.py)); без тестов регрессия маппинга/`type`/`status` не будет поймана (audit G1).

### Факты из кода
1. [`scripts/reproject_issue_i18n.py`](../../../../../../../scripts/reproject_issue_i18n.py) L39–55 — `--dry-run`, `--issue-id`.
2. L59–80 — `_load_issue_story_map` из sqlite/supabase `issue_story_links`.
3. L134–152 — `bridge.build_projection_input` → `save_projection` (skip при dry-run L158–165).
4. L154–155 — сохраняет `type` из existing payload.
5. `grep reproject tests/` → **0** matches (audit §3 G1).

### Gap / Проблема
**G1 (audit):** ops-скрипт без unit/integration автотеста.

### AC/DoD
- [ ] (P0) sqlite (или in-memory store): issue + story links + dominant story с разным `narrative_title` et/en → после write `payload_json.title.et != title.en`.
- [ ] (P0) `--dry-run` не вызывает `save_projection` (payload unchanged).
- [ ] (P0) повторный write → идемпотентный payload (stable hash or deep equality).
- [ ] (P1) `type` из existing payload сохранён после reproject.
- [ ] (P1) `python3 -m pytest -q tests/test_reproject_issue_i18n.py` green.

### Где менять код
- Новый: [`tests/test_reproject_issue_i18n.py`](../../../../../../../tests/test_reproject_issue_i18n.py)
- Опционально (testability): [`scripts/reproject_issue_i18n.py`](../../../../../../../scripts/reproject_issue_i18n.py) — вынести core loop из `main()` без смены CLI

### Out of scope
- Live Supabase integration test
- Изменение extraction_policy (T01 Done)
- Новый pkg / смена `gateway-active-package.current.yaml`

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_reproject_issue_i18n.py
python3 scripts/reproject_issue_i18n.py --help
```
