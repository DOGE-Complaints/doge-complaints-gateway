## Task workspace — `task-m2-02-05-t07-gap-10-pytest-logging-lifespan`

- Story: [`../STORY-M2-02-05-supabase-bootstrap-schema-parity.md`](../STORY-M2-02-05-supabase-bootstrap-schema-parity.md)
- Decision Ref: [`../../../../../../analysis/implementation-report-STORY-M2-02-05-bootstrap-parity-2026-05-10.md`](../../../../../../analysis/implementation-report-STORY-M2-02-05-bootstrap-parity-2026-05-10.md) (§5.4)

## Task: tests — GAP-10 остаток: pytest без lifespan и уровень логов

### Цель
Зафиксировать (тестом или краткой runtime-документацией в согласованном месте) поведение §5.4: в **pytest** сессии ASGI lifespan может не выполняться → `configure_logging()` из приложения не вызывается → корневой logger остаётся WARNING и DEBUG/INFO «теряются» — это **P2**, не P0 runtime.

### Факты из кода
1) Вызов настройки логирования в lifespan: [`src/core/api/asgi_app.py`](../../../../../../src/core/api/asgi_app.py) — поиск по символу `configure_logging` (в районе строк, указанных в §5.4 отчёта).
2) Реализация: [`src/core/logging_setup.py`](../../../../../../src/core/logging_setup.py) — `configure_logging` (см. файл, функция с `root.setLevel`).

### Gap / Проблема
Нет теста/дока, явно описывающего различие «uvicorn production» vs «pytest без lifespan».

### AC/DoD
- [ ] (P1) Либо unit/integration тест, либо согласованный markdown в `docs/runtime-docs/` / комментарий в `logging_setup.py` с **проверяемой** отсылкой на сценарий pytest (без изменения прод-поведения без отдельного ADR).
- [ ] (P2) Не дублировать полный объём STORY-M2-09 trace wave — только узкий факт из §5.4.

### Где менять код
- [`src/core/api/asgi_app.py`](../../../../../../src/core/api/asgi_app.py), [`src/core/logging_setup.py`](../../../../../../src/core/logging_setup.py), тесты под [`tests/`](../../../../../../tests/) — по результату выбора «тест vs док».

### План выполнения
1. Подтвердить факт вызова/не-вызова в pytest (grep тестов на `lifespan`, `TestClient`).
2. Выбрать минимальный артефакт (тест предпочтительнее по task-standard).

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_supabase_observability.py tests/core/test_logging_setup.py 2>/dev/null || pytest -q tests/ -k logging --tb=short -q
```
