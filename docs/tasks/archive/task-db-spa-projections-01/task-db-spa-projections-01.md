## Task: implement — separate `spa_issue_projections` read-model storage

### Цель
Сделать отдельное persistent хранилище SPA проекций, связанное с issue/story lineage, вместо чисто runtime DTO.

### Почему это важно (риск)
Без materialized projection storage dashboard данные неустойчивы и не пригодны для стабильной выдачи/кеширования.

### Scope
Входит: схема `spa_issue_projections`, linkage по `issue_id`, repository слой чтения/обновления.
Не входит: embeddings SPA проекций.

### Факты из кода (Code Facts / SSOT)
1. Projection строится в runtime через `IssueProjectionService`, но не хранится.
2. `issue_id` уже используется в evidence/projection контуре.
3. В target-анализе projection отделена как read-model слой.

### Gap / Проблема
`GAP-DB-004` и часть `GAP-DB-006`: отсутствует DB persistence SPA projections и integrity linkage.

### Decision Points
- **PM decision:** какие projection поля обязательны для demo dashboard.
- **CTO decision:** четкое разделение source-of-truth и read-model.
- **Options A/B:** upsert single row vs versioned projection snapshots.
- **Recommendation:** upsert + audit/version поле (без избыточного дублирования).

### AC/DoD
- [ ] (P0) Реализована таблица `spa_issue_projections`.
- [ ] (P0) Гарантирована связь с `issue_id` и lineage.
- [ ] (P1) Repository интегрирован в projection pipeline.
- [ ] (P1) Добавлены integration tests на persistence/readback.

### Где менять код
- DB migrations / schema
- `src/core/projection/` и/или `src/core/infrastructure/`
- `tests/` (integration)

### План выполнения (Execution Plan)
1) Определить schema read-model. 2) Реализовать repository. 3) Подключить pipeline. 4) Добавить tests.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/test_spa_projection.py -q
# + integration tests на persistence
```
