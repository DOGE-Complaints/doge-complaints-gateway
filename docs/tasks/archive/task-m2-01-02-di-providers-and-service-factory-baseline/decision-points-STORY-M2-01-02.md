# Decision Points — STORY-M2-01-02

## DP-01: Где размещать контракт ServiceFactory
- Варианты:
  - A) В `domain`.
  - B) В `application`.
- Решение: **B**.
- Обоснование: factory создает application services; domain остается независимым от orchestration/wiring.

## DP-02: Где размещать реализацию factory
- Варианты:
  - A) В `api`.
  - B) В `infrastructure`.
- Решение: **B**.
- Обоснование: wiring инфраструктурных реализаций в сервисы — инфраструктурная ответственность.

## DP-03: Как проверить отсутствие ad-hoc в API dependencies
- Решение: добавить guardrail-тест, который проверяет `api/dependencies.py` на отсутствие прямых `InMemoryHealthRepository(` и `HealthService(`.
