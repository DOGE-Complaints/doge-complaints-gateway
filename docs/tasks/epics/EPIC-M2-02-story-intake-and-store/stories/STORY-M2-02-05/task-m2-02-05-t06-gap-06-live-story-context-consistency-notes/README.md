## Task workspace — `task-m2-02-05-t06-gap-06-live-story-context-consistency-notes`

- Story: [`../STORY-M2-02-05-supabase-bootstrap-schema-parity.md`](../STORY-M2-02-05-supabase-bootstrap-schema-parity.md)
- Decision Ref: [`../../../../../../analysis/implementation-report-STORY-M2-02-05-bootstrap-parity-2026-05-10.md`](../../../../../../analysis/implementation-report-STORY-M2-02-05-bootstrap-parity-2026-05-10.md) (§5.3); см. также [`../../../../../../requirements/req-cross-layer-contract-testing.md`](../../../../../../requirements/req-cross-layer-contract-testing.md) (C-01)

## Task: tests — GAP-06: `live_story_context` не попадает в `StoryRecord`

### Цель
Зафиксировать регрессионным тестом факт: `StoryIntakeRequest.live_story_context` парсится из payload, но при построении `StoryRecord` в сервисе intake поле **не переносится** (молчаливое отбрасывание).

### Факты из кода
1) Парсинг `live_story_context` / `consistency_notes`: [`src/core/intake/contracts.py`](../../../../../../src/core/intake/contracts.py) примерно строки 198–225 (`parse_story_intake_request` / `LiveStoryContext`).
2) Построение `StoryRecord` при intake: [`src/core/application/services.py`](../../../../../../src/core/application/services.py) примерно строки 122–151 — в конструктор **не** передаются поля из `request.live_story_context`.
3) Существующий контрактный тест запроса: [`tests/test_story_intake_contract.py`](../../../../../../tests/test_story_intake_contract.py) строки 36–50 — проверяет `request.live_story_context`, не персистентность в record.

### Gap / Проблема
§5.3 отчёта: потеря данных без ошибки; нет теста «accepted but not persisted» на уровне record/DTO полей.

### AC/DoD
- [ ] (P0) Добавлен тест (новый или расширение существующего), который после вызова intake-пути (или минимального вызова сервиса с мок-репозиторием) assert-ит: у результирующего `StoryRecord` / сохранённой записи **нет** поля `consistency_notes` / `live_story_context` (или эквивалентная проверка через `dataclasses.fields` / отсутствие атрибутов, согласованная с фактической моделью `StoryRecord` в [`core/domain/contracts.py`](../../../../../../src/core/domain/contracts.py)).
- [ ] (P1) В комментарии к тесту — ссылка на `decision_ref` и пометка P2/product, если продукт позже потребует персистенцию (вне scope этого таска без отдельного решения).

### Где менять код
- [`doge-complaints-gateway/tests/`](../../../../../../tests/) (конкретный файл выбрать после чтения `StoryRecord` и DI-пути intake)
- При необходимости только чтение: [`src/core/application/services.py`](../../../../../../src/core/application/services.py), [`src/core/domain/contracts.py`](../../../../../../src/core/domain/contracts.py)

### План выполнения
1. Уточнить минимальный вызов (фикстуры как в соседних intake-тестах).
2. Написать assert против фактических полей `StoryRecord`.
3. `pytest` на добавленный файл/класс.

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_story_intake_contract.py tests/test_story_intake_field_persistence.py 2>/dev/null || pytest -q tests/test_story_intake_contract.py
```
