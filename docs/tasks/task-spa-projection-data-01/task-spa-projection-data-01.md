## Task: implement — deterministic derivation for SPA projection fields

### Цель
Определить и реализовать единые правила derivation для обязательных SPA-полей: `status`, `type`, `labels`, `title/summary/description (i18n)`.

### Почему это важно (риск)
Если правила не централизованы, проекция начинает зависеть от случайного контекста вызова и быстро деградирует в костыли.

### Scope
Входит:
- policy документ/модуль derivation;
- реализация правил в projection pipeline;
- контрактные тесты на deterministic output.

Не входит:
- UI слой;
- переводческий/LLM pipeline генерации контента.

### Факты из кода (Code Facts / SSOT)
1) `src/core/projection/mapper.py`
- projection валидирует enums и делает summary fallback, но не выводит все обязательные поля из intake/story.

2) `src/core/projection/enums.py`
- есть governed vocabulary для status/type/labels.

3) `src/core/intake/contracts.py`
- входной payload не содержит SPA-ready поля.

### Gap / Проблема
`GAP-IP-004`: нет единой формализованной политики derivation SPA-полей из текущего доменного потока.

### Decision Points
- **PM decision:** минимальный набор полей, который обязателен для demo карточки.
- **CTO decision:** централизованная policy и версионирование правил вместо разрозненных fallback-веток.
- **Options:**
  - A: заполнение полей на уровне endpoint handlers.
  - B: отдельная policy в projection/application слое.
- **Recommendation:** вариант B (контрактно и масштабируемо).

### AC/DoD
- [ ] (P0) Определены deterministic rules для `status/type/labels`.
- [ ] (P0) Определены deterministic rules для i18n `title/summary/description`.
- [ ] (P0) Реализация policy централизована и покрыта тестами.
- [ ] (P1) Введен policy version marker и documented behavior.
- [ ] (P1) Нет placeholder/fake значений в обязательных полях.

### Где менять код
- `src/core/projection/` (policy/mapper/validation)
- `src/core/application/` (если часть правил должна жить в orchestration)
- `tests/test_spa_projection.py` + новые test modules
- `docs/runtime-docs/` (контрактное описание)

### План выполнения (Execution Plan)
1) Зафиксировать правила derivation по каждому обязательному полю.
2) Имплементировать policy.
3) Обновить mapper/validation.
4) Добавить тесты и документацию.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/test_spa_projection.py -q
python3 -m pytest tests/test_story_promotion_projection_bridge.py -q
python3 -m pytest tests/test_e2e_intake_create_spa_contract.py -q
```
