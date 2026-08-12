## Task workspace — `task-m2-02-06-t08-gap-02-03-04-testclient-simulation-canvas-intake`

- Story: [`../STORY-M2-02-06-data-model-registry-section-16-followup.md`](../STORY-M2-02-06-data-model-registry-section-16-followup.md)
- Decision Ref: [`../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md`](../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md) — **«Незакрытые хвосты — финальный прогон»**, рецепт TestClient; GAP-02/03/04 (верификация gateway без `GATEWAY_URL`)

## Task: tests — E2E intake по фрагменту simulation canvas через FastAPI TestClient

### Цель
Зафиксировать регрессионным тестом, что POST `/intake/stories` с payload в форме canvas (мультиязычный title, summary, origin) персистится в in-memory `StoryRepository` так же, как ожидает контракт — **без** внешнего HTTP-сервера и без `urllib` (паттерн как в [`tests/test_e2e_create_story_fullpath.py`](../../../../../../../tests/test_e2e_create_story_fullpath.py)).

### Факты из кода
1. `get_api_dependencies().story_intake_service` имеет публичное поле **`repository`**, метод `get_story(story_id)` — см. [`src/core/application/services.py`](../../../../../../../src/core/application/services.py) (`StoryIntakeService`), [`handlers.py`](../../../../../../../src/core/api/handlers.py) (логирует `repository.__class__`).
2. `INTAKE_SCHEMA_VERSION` — [`core/intake/__init__.py`](../../../../../../../src/core/intake/__init__.py) или re-export из contracts.

### Gap / Проблема
Отсутствует автоматическая проверка цепочки «canvas-shaped JSON → HTTP handler → StoryRecord»; реальный GPT-прогон не обязателен для закрытия gateway-слоя (см. Decision Ref).

### AC/DoD
- [x] (P0) Новый файл `tests/test_e2e_simulation_canvas_intake.py`: fixture `client` с `monkeypatch` env + `_clear_api_dependencies_cache` + `TestClient(app)` (как fullpath e2e).
- [x] (P0) Загрузка [`tests/sandbox/dogestonia_simulation_canvas_v0_1.json`](../../../../../../../tests/sandbox/dogestonia_simulation_canvas_v0_1.json); выборка ≥1 сценария с известным `simulation_id` (проверить наличие id в JSON).
- [x] (P0) POST `/intake/stories` с `narrative.title_hint_et|ru|en`, `narrative.summary`, `origin` → `200`; чтение `get_api_dependencies().story_intake_service.repository.get_story(story_id)`.
- [x] (P1) Assert полей `narrative_title_hint_et|ru|en`, `narrative_summary_json` (после `json.loads`), `origin_source`, `origin_conversation_id` согласованы с payload.

### Где менять код
- [`tests/test_e2e_simulation_canvas_intake.py`](../../../../../../../tests/test_e2e_simulation_canvas_intake.py) (создать).

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_e2e_simulation_canvas_intake.py
```
