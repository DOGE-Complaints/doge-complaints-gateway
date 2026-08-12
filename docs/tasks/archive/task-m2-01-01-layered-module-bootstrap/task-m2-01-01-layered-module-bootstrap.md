## Task: implement — layered module bootstrap for Module 2

### Source Story
- `docs/tasks/epics/EPIC-M2-01-core-foundation-and-governance/stories/STORY-M2-01-01-layered-module-bootstrap.md`

### Цель
Собрать минимальный runtime-каркас слоёв `API -> Application -> Domain -> Infrastructure` в репозитории `doge-complaints-gateway`, чтобы следующий функционал Module 2 добавлялся без архитектурного дрейфа.

### AC/DoD
- [ ] Создан и документирован слой `API`.
- [ ] Создан и документирован слой `Application`.
- [ ] Создан и документирован слой `Domain`.
- [ ] Создан и документирован слой `Infrastructure`.
- [ ] Зафиксированы правила зависимостей между слоями.
- [ ] Smoke-тесты bootstrapping выполняются успешно.

### Артефакты
- Фазовый лог: `BULLRUN-PHASE-LOG.md`
- Верификация AC: `acceptance-verification-STORY-M2-01-01.md`
