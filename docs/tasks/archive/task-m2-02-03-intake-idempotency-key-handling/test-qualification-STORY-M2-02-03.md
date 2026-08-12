# Test Qualification — STORY-M2-02-03

- Command: `python3 -m pytest -q`
- Result: `31 passed`
- Coverage focus:
  - повторы с одинаковым idempotency key;
  - разные ключи -> разные story;
  - совместимость с existing DI/service tests.
