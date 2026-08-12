# Decision Points — STORY-M2-01-01

## DP-01: Проектный layout
- Варианты:
  - A) Плоский layout в корне.
  - B) `src/` layout с package `core`.
- Решение: **B**.
- Обоснование: лучше изоляция импортов, проще масштабировать слои и покрывать tests с `pythonpath`.

## DP-02: Минимальный runtime стек
- Варианты:
  - A) Вводить web framework сразу (FastAPI/Flask).
  - B) Сделать framework-agnostic bootstrap.
- Решение: **B**.
- Обоснование: story требует слой и bootstrap без бизнес-функциональности; framework выбирается следующими stories.

## DP-03: Проверка guardrails зависимостей
- Варианты:
  - A) Статический линтер/внешний инструмент.
  - B) Простой guardrail-тест на уровне импорта модулей.
- Решение: **B**.
- Обоснование: минимальный baseline без новых tooling-deps, но с проверяемым правилом слоев.
