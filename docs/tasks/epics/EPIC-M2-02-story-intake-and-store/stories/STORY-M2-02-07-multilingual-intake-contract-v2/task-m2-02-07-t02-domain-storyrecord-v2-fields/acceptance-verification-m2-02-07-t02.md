# Acceptance verification — T02

| AC | Код / тест | Статус |
|----|------------|--------|
| StoryRecord v2 fields | `domain/contracts.py`, lifecycle tests | pass |
| Service mapping | `services.py`, repository roundtrip | pass |

Команда: `pytest tests/test_story_repository_lifecycle.py tests/test_story_intake_live_context_not_on_record.py -q`
