# Acceptance verification — T01

| AC | Код / тест | Статус |
|----|------------|--------|
| v2 schema only | `contracts.py`, reject v1 test | pass |
| title/description/session_language required | contract tests | pass |
| identity_issuer required | contract test | pass |

Команда: `pytest tests/test_story_intake_contract.py -q`
