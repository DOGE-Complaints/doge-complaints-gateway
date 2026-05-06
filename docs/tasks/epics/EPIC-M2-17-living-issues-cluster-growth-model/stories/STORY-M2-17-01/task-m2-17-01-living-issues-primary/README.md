## Task workspace — `task-m2-17-01-living-issues-primary`

- Story: [`../STORY-M2-17-01-living-issues-create-extend-orchestration.md`](../STORY-M2-17-01-living-issues-create-extend-orchestration.md)
- Requirement: [`29-living-issues-cluster-growth-model.md`](../../../../../requirements/29-living-issues-cluster-growth-model.md)
- Decision Ref: [`req29-decomposition-validation.md`](../../../../../analysis/req29-decomposition-validation.md)
- Skill declared: `python-pro`

### Scope
Оркестрация выполнения STORY-M2-17-01 и сводная верификация AC-29-1..6.

## Task: implement — primary delivery

### Цель
Закрыть соответствующий delivery-блок requirement 29 с проверяемым результатом.

### Факты из кода
1) `find_promoted_by_cluster_id` уже существует в candidate stores (req29 section 2).
2) `IssueCreateService.create_issue()` должен ветвиться create/extend path (req29 section 5).
3) Инварианты AC-29-1..6 требуют отдельной проверки по сервисным и e2e тестам (req29 section 11).

### Gap / Проблема
Без этого task остаётся неполным покрытие living-issues модели и AC requirement 29.

### AC/DoD
- [ ] (P0) Scope задачи реализован по целевым файлам.
- [ ] (P1) Добавлены/обновлены тесты и команды проверки.
- [ ] (P1) Артефакты task-папки синхронизированы.

### Где менять код
- `src/core/` (по scope конкретного task)
- `tests/` (по scope конкретного task)

### План выполнения
1. Подтвердить исходный gap по requirement и текущему коду.
2. Внести целевые изменения в runtime/test слой.
3. Прогнать таргетные проверки и обновить acceptance.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q --tb=short
```
