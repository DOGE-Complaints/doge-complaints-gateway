# Decision Points — STORY-M2-01-03

## DP-01: Формат профилей
- Решение: строгий enum `DeploymentProfile` (`demo`, `pilot`).
- Причина: явная валидация и предсказуемые profile defaults.

## DP-02: Стратегия feature flags
- Решение: profile-based defaults + env overrides.
- Причина: demo безопасен по умолчанию, pilot готов к адаптерам.

## DP-03: Уровень строгости env validation
- Решение: `ConfigError` при отсутствии `API_BASE_URL`, невалидном профиле, timeout и bool-флагах.
- Причина: fail-fast и прозрачная диагностика на bootstrap этапе.
