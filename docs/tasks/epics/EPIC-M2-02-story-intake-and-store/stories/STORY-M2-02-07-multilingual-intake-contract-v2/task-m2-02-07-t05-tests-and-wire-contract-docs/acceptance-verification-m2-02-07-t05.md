# Acceptance verification — T05 (REQ-33 §5)

| AC | Тест / поведение | Статус |
|----|------------------|--------|
| POST v2 → HTTP 202 | `test_http_intake_endpoint.py` | pass |
| Без identity_issuer → 400 | `test_story_intake_contract.py` | pass |
| Без title/description → 400 | contract tests | pass |
| Idempotent POST без header (SHA-256 body) | `test_http_intake_sha256_idempotency_without_header` | pass |
| `StoryRecord.narrative_title` dict | lifecycle / simulation e2e | pass |
| v1 → 400 | `test_parse_story_intake_request_rejects_v1_schema` | pass |

Команда: `pytest -q` (gateway) — 251 passed.
