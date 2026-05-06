## Task workspace — `task-m2-17-01-t12-projection-content-invariant`

- Story: [`../STORY-M2-17-01-living-issues-create-extend-orchestration.md`](../STORY-M2-17-01-living-issues-create-extend-orchestration.md)
- Requirement: [`29-living-issues-cluster-growth-model.md`](../../../../../requirements/29-living-issues-cluster-growth-model.md)
- Decision Ref: [`req29-code-audit.md`](../../../../../analysis/req29-code-audit.md)
- Skill declared: `python-pro`

### Scope
Закрыть `GAP-29-04`: добавить content assertion для INV-LI-04, подтверждающий обновление projection payload после extend.

## Task: test — T12 delivery

### Цель
Явно покрыть инвариант согласованности проекции с актуальным merged набором story_ids.

### Факты из кода
1) В аудите зафиксирован `GAP-29-04`: нет проверки содержимого проекции после extend.
2) Extend path строит проекцию на `updated.story_ids`, но это не подтверждено content-assertion.
3) Основная точка теста: `tests/test_issue_create_service.py` (допустимо усиление e2e).

### Gap / Проблема
Регрессия в построении проекции после extend может не быть замечена текущими тестами.

### AC/DoD
- [ ] (P0) Добавлен assert, что projection content после extend отражает расширенный story set.
- [ ] (P1) Проверка выполнена на сервисном уровне (и при необходимости на e2e уровне).
- [ ] (P1) Артефакты task-папки синхронизированы.

### Где менять код
- `tests/test_issue_create_service.py`
- `tests/test_e2e_story_cluster_issue_pipeline.py` (опционально)

### План выполнения
1. Усилить существующий create->extend тест content-assertion для projection.
2. При необходимости добавить дополнительный assert в e2e.
3. Прогнать таргетные тесты и обновить acceptance.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_issue_create_service.py tests/test_e2e_story_cluster_issue_pipeline.py
```
