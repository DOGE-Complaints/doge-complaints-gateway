## Task workspace — `task-m2-17-01-t11-sqlite-extend-parity-test`

- Story: [`../STORY-M2-17-01-living-issues-create-extend-orchestration.md`](../STORY-M2-17-01-living-issues-create-extend-orchestration.md)
- Requirement: [`29-living-issues-cluster-growth-model.md`](../../../../../requirements/29-living-issues-cluster-growth-model.md)
- Decision Ref: [`req29-code-audit.md`](../../../../../analysis/req29-code-audit.md)
- Skill declared: `python-pro`

### Scope
Закрыть `GAP-29-03`: добавить SQLite-backed parity test для extend path и проверки SQL persistence.

## Task: test — T11 delivery

### Цель
Подтвердить backend parity для extend сценария не только в in-memory, но и на SQLite persistence слое.

### Факты из кода
1) В аудите зафиксирован `GAP-29-03`: отсутствует SQLite-backed extend-path тест.
2) Непокрытые участки: update/read roundtrip в `issue_candidates`, `review_audit_log`, `doge_issues`.
3) Рекомендованная зона теста: `tests/test_db_backed_pipeline_e2e.py`.

### Gap / Проблема
Без SQLite parity-теста регрессии SQL update path могут пройти незамеченными.

### AC/DoD
- [ ] (P0) Добавлен SQLite-backed тест create+extend с проверкой merged story_ids.
- [ ] (P0) Подтверждена запись `cluster_growth_extend` в `review_audit_log`.
- [ ] (P1) Проверена согласованность persisted projection после extend.
- [ ] (P1) Артефакты task-папки синхронизированы.

### Где менять код
- `tests/test_db_backed_pipeline_e2e.py` (или новый DB-backed тестовый файл)

### План выполнения
1. Добавить SQLite-backed сценарий create->extend.
2. Проверить persisted SQL state по ключевым таблицам.
3. Прогнать DB-backed тесты requirement 29 и обновить acceptance.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_db_backed_pipeline_e2e.py
```
