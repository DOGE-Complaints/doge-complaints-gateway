## Task workspace — `task-m2-17-01-t10-e2e-clustered-status-ac29-6`

- Story: [`../STORY-M2-17-01-living-issues-create-extend-orchestration.md`](../STORY-M2-17-01-living-issues-create-extend-orchestration.md)
- Requirement: [`29-living-issues-cluster-growth-model.md`](../../../../../requirements/29-living-issues-cluster-growth-model.md)
- Decision Ref: [`req29-code-audit.md`](../../../../../analysis/req29-code-audit.md)
- Skill declared: `python-pro`

### Scope
Закрыть `GAP-29-02`: добавить в e2e-покрытие явные assertions по `CLUSTERED` для историй обеих волн (AC-29-6).

## Task: test — T10 delivery

### Цель
Формально закрыть AC-29-6 в тестах и поймать будущие регрессии lifecycle update в extend path.

### Факты из кода
1) В аудите зафиксирован `GAP-29-02`: в e2e нет assert на `CLUSTERED` для batch1/batch2.
2) Lifecycle update выполняется в orchestrator и должен покрываться тестом.
3) Точка изменения: `tests/test_e2e_story_cluster_issue_pipeline.py`.

### Gap / Проблема
AC-29-6 выполняется в коде, но не верифицируется тестовыми assertions.

### AC/DoD
- [ ] (P0) В e2e тест добавлены assertions на `StoryLifecycleStatus.CLUSTERED` для обеих волн.
- [ ] (P1) Тесты e2e по living issues проходят.
- [ ] (P1) Артефакты task-папки синхронизированы.

### Где менять код
- `tests/test_e2e_story_cluster_issue_pipeline.py`

### План выполнения
1. Дополнить существующий e2e тест assertions по lifecycle status.
2. Прогнать e2e-набор requirement 29.
3. Зафиксировать результаты в acceptance.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_e2e_story_cluster_issue_pipeline.py
```
