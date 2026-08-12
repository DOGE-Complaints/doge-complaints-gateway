# Acceptance verification — T03

| AC | Код / тест | Статус |
|----|------------|--------|
| SHA-256 fallback без header | `test_http_intake_sha256_idempotency_without_header` | pass |
| Raw body before parse | `asgi_app.py` | pass |
| HTTP 202 on success | `test_http_intake_endpoint.py` | pass |

Команда: `pytest tests/test_story_intake_idempotency.py tests/test_http_intake_endpoint.py -q`
