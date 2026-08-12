## Task: implement — separate `story_embeddings` storage

### Цель
Добавить отдельный persistent слой для embeddings входящих stories с versioned metadata.

### Почему это важно (риск)
Без отдельного storage embeddings невозможны качественный semantic search и кластеризация на уровне историй.

### Scope
Входит: схема `story_embeddings`, связи с `story_id`, версия модели/временные метки, индексы.
Не входит: embeddings для SPA projections.

### Факты из кода (Code Facts / SSOT)
1. В target-анализе выделены отдельные таблицы embeddings.
2. В `src/core/**` сейчас нет DB embeddings storage.
3. Story ID уже существует как доменный ключ.

### Gap / Проблема
`GAP-DB-005`: отсутствует persistence embeddings для stories.

### Decision Points
- **PM decision:** минимальный набор embedding метаданных для демо-аналитики.
- **CTO decision:** версии embeddings и модель должны быть first-class полями.
- **Options A/B:** один embedding на story vs versioned multi-row.
- **Recommendation:** versioned multi-row с флагом активной версии.

### AC/DoD
- [ ] (P0) Создана таблица/репозиторий `story_embeddings`.
- [ ] (P0) Поддержана связь с `stories.story_id`.
- [ ] (P1) Добавлены поля версии модели и timestamps.
- [ ] (P1) Добавлены tests на запись/чтение embeddings.

### Где менять код
- DB migrations / schema
- `src/core/infrastructure/` (repo/adapters)
- `tests/` (integration)

### План выполнения (Execution Plan)
1) Зафиксировать схему. 2) Реализовать repository. 3) Добавить tests и валидацию linkage.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
# integration tests для story embeddings
```
