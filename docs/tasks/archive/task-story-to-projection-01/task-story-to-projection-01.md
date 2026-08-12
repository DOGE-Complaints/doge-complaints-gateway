## Task: implement — bridge Story/Promotion to ProjectionInput

### Цель
Собрать единый adapter/assembler слой, который формирует `ProjectionInput` из доменных сущностей story/promotion без ad-hoc маппинга в API.

### Почему это важно (риск)
Без явного bridge-слоя любая проекция в SPA рискует собираться разрозненно, что ломает контракт и усложняет поддержку.

### Scope
Входит:
- новый bridge/assembler компонент;
- deterministic mapping из доменных объектов в `ProjectionInput`;
- тесты на mapping-правила.

Не входит:
- HTTP exposure endpoint-ов.

### Факты из кода (Code Facts / SSOT)
1) `src/core/application/services.py`
- story создается и хранится как `StoryRecord`.

2) `src/core/promotion/service.py`
- issue candidate жизненный цикл реализован отдельно.

3) `src/core/projection/input.py`
- projection требует структурированный `ProjectionInput`, которого сейчас нет в pipeline.

### Gap / Проблема
`GAP-IP-003`: отсутствует сквозной слой трансформации перед `IssueProjectionService`.

### Decision Points
- **PM decision:** нужна предсказуемая карточка SPA для demo, без ручных правок данных.
- **CTO decision:** bridge должен быть отдельным контрактным компонентом, не размазанным по handlers.
- **Options:**
  - A: маппинг внутри API handlers.
  - B: отдельный application bridge/assembler сервис.
- **Recommendation:** вариант B (чистые границы и повторное использование в API/батч-пайплайнах).

### AC/DoD
- [ ] (P0) Реализован bridge `Story/Promotion -> ProjectionInput`.
- [ ] (P0) Bridge покрыт unit tests по обязательным полям.
- [ ] (P1) Mapping ошибки возвращают понятные contract errors.
- [ ] (P1) `IssueProjectionService` получает валидный `ProjectionInput` без ручных patch-значений.

### Где менять код
- `src/core/application/` (новый bridge service)
- `src/core/projection/` (при необходимости контрактные helper-ы)
- `tests/` (unit/integration для bridge)

### План выполнения (Execution Plan)
1) Описать входы bridge и target `ProjectionInput`.
2) Реализовать mapping rules.
3) Добавить тесты.
4) Подключить bridge в orchestration слой.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/test_spa_projection.py -q
python3 -m pytest tests/test_story_promotion_projection_bridge.py -q
python3 -m pytest tests/test_e2e_intake_create_spa_contract.py -q
```
