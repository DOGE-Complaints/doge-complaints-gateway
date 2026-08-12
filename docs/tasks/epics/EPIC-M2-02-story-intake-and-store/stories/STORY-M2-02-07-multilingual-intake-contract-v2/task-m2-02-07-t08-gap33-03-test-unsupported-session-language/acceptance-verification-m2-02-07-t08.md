# Acceptance verification — T08 (GAP-33-03)

| AC | Код / тест | Статус |
|----|------------|--------|
| Parser rejects `session_language=de` | `test_parse_story_intake_request_rejects_unsupported_session_language` | pass |
| HTTP 400 + taxonomy | `test_intake_stories_endpoint_returns_400_for_unsupported_session_language` | pass |

Команды:
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_story_intake_contract.py::test_parse_story_intake_request_rejects_unsupported_session_language tests/test_http_intake_endpoint.py::test_intake_stories_endpoint_returns_400_for_unsupported_session_language -q
```
