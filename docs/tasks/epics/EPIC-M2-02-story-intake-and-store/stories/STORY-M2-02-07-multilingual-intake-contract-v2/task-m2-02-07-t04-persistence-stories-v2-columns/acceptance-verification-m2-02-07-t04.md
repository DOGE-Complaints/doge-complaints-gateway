# Acceptance verification — T04

| AC | Код / тест | Статус |
|----|------------|--------|
| SQLite roundtrip v2 JSON | `test_sqlite_story_repository_roundtrip` | pass |
| Schema invariant | `test_stories_schema_cross_layer_invariant` | pass |
| Bootstrap columns | `000_full_init.sql` | pass |

Команда: `pytest tests/test_story_repository_lifecycle.py tests/test_stories_schema_cross_layer_invariant.py -q`
