## Task workspace — `task-m2-17-01-t09-embedding-upsert-atomicity`

- Story: [`../STORY-M2-17-01-living-issues-create-extend-orchestration.md`](../STORY-M2-17-01-living-issues-create-extend-orchestration.md)
- Requirement: [`29-living-issues-cluster-growth-model.md`](../../../../../requirements/29-living-issues-cluster-growth-model.md)
- Decision Ref: [`req29-code-audit.md`](../../../../../analysis/req29-code-audit.md)
- Skill declared: `python-pro`

### Scope
Закрыть `GAP-29-01`: перевести `save_projection_embedding()` с DELETE+INSERT на атомарный upsert в SQLite/Supabase.

## Task: implement — T09 delivery

### Цель
Устранить spec deviation по embedding persistence, чтобы в extend path не было окна гонки и временного исчезновения записи по `issue_id`.

### Факты из кода
1) В аудите зафиксирован `GAP-29-01` с текущей схемой DELETE+INSERT.
2) Требование 29 (section 7.2) требует idempotent upsert для issue projection embeddings.
3) Текущая реализация затрагивает `src/core/infrastructure/db_sqlite.py` и `src/core/infrastructure/db_supabase.py`.

### Gap / Проблема
DELETE+INSERT в embedding store неатомарен и может дать кратковременное отсутствие строки при concurrent access.

### AC/DoD
- [ ] (P0) `save_projection_embedding` в SQLite реализован как upsert по `issue_id`.
- [ ] (P0) `save_projection_embedding` в Supabase реализован одним upsert-запросом по `issue_id`.
- [ ] (P1) Regression-тесты living issues остаются зелеными.
- [ ] (P1) Артефакты task-папки синхронизированы.

### Где менять код
- `src/core/infrastructure/db_sqlite.py`
- `src/core/infrastructure/db_supabase.py`
- `tests/` (при необходимости точечного покрытия)

### План выполнения
1. Подтвердить текущее поведение DELETE+INSERT по аудиту.
2. Перевести SQLite/Supabase реализацию на upsert-паттерн.
3. Прогнать таргетные тесты и обновить acceptance.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q --tb=short
```
