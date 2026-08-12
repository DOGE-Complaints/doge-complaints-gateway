## Task workspace — `task-m2-02-05-t03-gap-jsonb-read-issue-candidates-audit`

- Story: [`../STORY-M2-02-05-supabase-bootstrap-schema-parity.md`](../STORY-M2-02-05-supabase-bootstrap-schema-parity.md)
- Decision Ref: [`../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md`](../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md) (§6–7, GAP-09)

## Task: fix — JSONB list deserialization for candidates and audit log

### Цель
Исправить чтение полей `story_ids_json` и `related_story_ids_json` в [`src/core/infrastructure/db_supabase.py`](../../../../../../src/core/infrastructure/db_supabase.py) так, чтобы корректно обрабатывался ответ PostgREST, когда JSONB уже приходит как Python `list`, без `json.loads(str(list))`.

### Факты из кода
1) `SupabaseIssueCandidateStore.get` / `find_promoted_by_cluster_id` используют `json.loads(str(row["story_ids_json"]))` (пример строки 581 в текущей версии файла).
2) `SupabaseReviewAuditLogRepository.list_for_candidate` использует `json.loads(str(row["related_story_ids_json"]))` (около строки 658).
3) Анализ §6 «JSONB-BUG» описывает цепочку: PostgREST → `list` → `str(list)` → невалидный JSON для `json.loads`.

### Gap / Проблема
GAP-09: первое реальное чтение кандидата/audit после записи JSONB может выбросить `JSONDecodeError`.

### AC/DoD
- [x] (P0) Единый helper (или inline ветвление `isinstance(raw, list)`) применён в обоих местах чтения + любых других read-путях того же класса для этих колонок.
- [x] (P0) Юнит- или integration-тест воспроизводит `list`-ответ и проходит без исключения.
- [x] (P1) Поведение для `str` (legacy) сохранено.

### Где менять код
- [`doge-complaints-gateway/src/core/infrastructure/db_supabase.py`](../../../../../../src/core/infrastructure/db_supabase.py)
- Тесты: [`doge-complaints-gateway/tests/`](../../../../../../tests/) (конкретный файл добавить рядом с существующими supabase store tests при наличии).

### План выполнения
1. Добавить нормализацию JSONB→sequence в одном месте.
2. Заменить вызовы в `SupabaseIssueCandidateStore` и `SupabaseReviewAuditLogRepository`.
3. Добавить регрессионный тест с mocked row dict.

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_supabase_observability.py tests/integration/supabase/ -q --tb=no 2>/dev/null | head -50
```
