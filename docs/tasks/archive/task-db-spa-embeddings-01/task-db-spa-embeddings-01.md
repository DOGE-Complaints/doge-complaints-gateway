## Task: implement — separate `spa_issue_projection_embeddings` storage

### Цель
Добавить отдельное persistent хранение embeddings для SPA проекций, пригодное для future issue clustering/search.

### Почему это важно (риск)
Без issue-level embeddings теряется возможность последующей семантической кластеризации и поиска по issue карточкам.

### Scope
Входит: таблица `spa_issue_projection_embeddings`, связь с `issue_id`, version/model metadata, индексы.
Не входит: пересчет кластеров на runtime уровне.

### Факты из кода (Code Facts / SSOT)
1. В target-анализе отдельно выделены embeddings для SPA projections.
2. В runtime сейчас projection хранится только как DTO.
3. В коде уже есть `issue_id` как связочный ключ.

### Gap / Проблема
`GAP-DB-005`: нет persistent issue-level embeddings.

### Decision Points
- **PM decision:** нужна ли обязательная генерация embeddings в demo scope.
- **CTO decision:** versioned embeddings и индексирование с учетом scale.
- **Options A/B:** one-row-per-issue vs versioned snapshots.
- **Recommendation:** versioned snapshots с active marker.

### AC/DoD
- [ ] (P0) Введена таблица `spa_issue_projection_embeddings`.
- [ ] (P0) Связь с `issue_id` и projection lifecycle валидна.
- [ ] (P1) Добавлены tests на запись/чтение и linkage.
- [ ] (P1) Зафиксирован contract для model/version/dimension.

### Где менять код
- DB migrations / schema
- projection persistence adapters
- integration tests

### План выполнения (Execution Plan)
1) Зафиксировать embedding schema. 2) Реализовать repository. 3) Интегрировать с projection pipeline. 4) Протестировать.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
# integration tests для spa projection embeddings
```
