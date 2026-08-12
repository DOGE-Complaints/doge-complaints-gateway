## Task: tests — unit coverage for domain flows and invariants

### Цель
Добавить unit тесты на доменные edge-cases и инварианты intake/promotion/projection контуров, чтобы стабилизировать бизнес-логику независимо от инфраструктуры.

### Почему это важно (риск)
Без domain-level тестов возможны скрытые регрессии в правилах деривации и lifecycle переходах.

### Факты из кода (Code Facts / SSOT)
1. В домене есть модули `intake`, `promotion`, `projection`.
2. Есть часть contract тестов, но покрытие edge-case инвариантов не полное.
3. Projection rules опираются на deterministic derivation policy.

### Gap / Проблема
Недостаточно тестов на граничные значения и инварианты доменных переходов.

### AC/DoD
- [ ] (P0) Покрыты edge-cases intake validation.
- [ ] (P0) Покрыты lifecycle transition guards в promotion.
- [ ] (P0) Покрыты projection invariants (status/type/labels/policy_version).
- [ ] (P1) Добавлены негативные сценарии для malformed/partial inputs.

### Где менять код
- `tests/`
- `src/core/intake/`
- `src/core/promotion/`
- `src/core/projection/`

### План выполнения (Execution Plan)
1) Составить инвариантную карту. 2) Добавить unit тесты по каждому модулю. 3) Укрепить regression bucket.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests -k "intake or promotion or projection" -q
```
