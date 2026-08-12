## Task workspace — `task-m2-02-07-t03-api-raw-body-idempotency-sha256`

- Story: [`../STORY-M2-02-07-multilingual-intake-contract-v2.md`](../STORY-M2-02-07-multilingual-intake-contract-v2.md)
- Decision Ref: REQ-33 §2.4; [`../../../../../../analysis/gap-interview-decisions-2026-05-13.md`](../../../../../../analysis/gap-interview-decisions-2026-05-13.md) G-08

## Task: implement — raw body + SHA-256 idempotency fallback

### Цель
При отсутствии заголовка `Idempotency-Key` вычислять ключ как `sha256(raw_body_bytes)` до `json.loads`, чтобы GPT-retry с тем же телом не создавал дубль story.

### Факты из кода
1. [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) L279–290 — `payload = await request.json()`; `idempotency_key=request.headers.get("idempotency-key")` только из заголовка.
2. [`src/core/api/handlers.py`](../../../../../../../src/core/api/handlers.py) — `handle_story_intake(..., idempotency_key: str | None = None)` передаёт ключ в сервис без fallback.

### Gap / Проблема
G-08: повторный идентичный запрос без заголовка создаёт вторую story.

### AC/DoD
- [ ] (P0) `resolve_idempotency_key(header, body: bytes) -> str`: header если непустой, иначе `hashlib.sha256(body).hexdigest()`.
- [ ] (P0) `intake_stories`: `raw_body = await request.body()` до парсинга JSON; парсинг из `raw_body`.
- [ ] (P1) Тест: два POST с одинаковым body без заголовка → один `story_id`.

### Где менять код
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py)
- [`src/core/api/handlers.py`](../../../../../../../src/core/api/handlers.py)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_story_intake_idempotency.py tests/test_http_intake_endpoint.py -q --tb=short
```
