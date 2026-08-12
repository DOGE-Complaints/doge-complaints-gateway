## Task: implement — SQL-backed stories persistence (incoming stories)

### Цель
Перевести хранение входящих stories/idempotency/profile linkage с in-memory на SQL/Supabase-backed контур.

### Почему это важно (риск)
Пока stories живут в памяти, нет durability и гарантированной целостности после рестарта.

### Scope
Входит: `stories`, `idempotency_keys`, базовый story-related repository слой.
Не входит: embeddings и SPA projections.

### Факты из кода (Code Facts / SSOT)
1. `StoryRecord` и `IdempotencyRecord` определены в `src/core/domain/contracts.py`.
2. Сейчас используются `InMemoryStoryRepository` и `InMemoryIdempotencyRepository`.
3. Story intake сервис зависит от этих контрактов: `src/core/application/services.py`.

### Gap / Проблема
`GAP-DB-001` и часть `GAP-DB-006`: нет SQL-persistence и DB-level integrity для входящих stories.

### Decision Points
- **PM decision:** какие поля stories обязательны для demo proof.
- **CTO decision:** сохранить protocol compatibility без layer coupling.
- **Options A/B:** прямой switch репозиториев vs dual-mode адаптер.
- **Recommendation:** dual-mode через ServiceFactory profile wiring.

### AC/DoD
- [ ] (P0) SQL-backed `StoryRepository` и `IdempotencyRepository` реализованы.
- [ ] (P0) Уникальность idempotency ключа обеспечена DB constraint.
- [ ] (P0) Story lifecycle поля сохраняются без semantic drift.
- [ ] (P1) Добавлены integration tests для save/get/idempotency.

### Где менять код
- `src/core/infrastructure/` (новые SQL repositories + provider wiring)
- `src/core/application/services.py` (при необходимости минимальные адаптации)
- `tests/` (integration tests)

### План выполнения (Execution Plan)
1) Реализовать SQL repos. 2) Подключить через providers. 3) Добавить integration tests. 4) Сверить lifecycle semantics.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/test_story_repository_lifecycle.py tests/test_story_intake_idempotency.py -q
```
