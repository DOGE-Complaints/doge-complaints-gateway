# Анализ — STORY-M2-01-01 (Layered Module Bootstrap)

## Проверенные факты (только из репозитория)

1. В корне репозитория отсутствует runtime-код.
   - Подтверждение: в `doge-complaints-gateway` есть только `.git`, `README.md`, `LICENSE`, `.gitignore`, `docs/`.
2. Python-файлы отсутствуют.
   - Подтверждение: поиск `**/*.py` в `doge-complaints-gateway` не возвращает файлов.
3. Build/test-конфигурация для Python отсутствует.
   - Подтверждение: поиск `pyproject.toml`, `pytest.ini` в `doge-complaints-gateway` не возвращает файлов.
4. Репозиторий сейчас docs-only baseline.
   - Подтверждение: `README.md` явно фиксирует ветку как docs-only и говорит, что runtime удален намеренно.
5. Story требует именно runtime-bootstrap 4 слоев и smoke-тесты.
   - Подтверждение: `STORY-M2-01-01-layered-module-bootstrap.md`, разделы `Scope` и `AC / DoD`.

## Gap

- Для выполнения story нужно создать новый Python bootstrap с нуля:
  - структуру пакетов по слоям;
  - минимальный стартовый orchestrator/bootstrap entrypoint;
  - guardrails зависимостей между слоями;
  - smoke-тесты bootstrapping.

## Риск

- Нужен явный выбор формата проекта (например `src/` layout + `pytest`), чтобы не создавать второй вариант структуры в следующих stories.
