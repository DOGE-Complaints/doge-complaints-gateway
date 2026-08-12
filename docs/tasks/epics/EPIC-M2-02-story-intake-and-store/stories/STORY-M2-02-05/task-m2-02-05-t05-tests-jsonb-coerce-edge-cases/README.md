## Task workspace — `task-m2-02-05-t05-tests-jsonb-coerce-edge-cases`

- Story: [`../STORY-M2-02-05-supabase-bootstrap-schema-parity.md`](../STORY-M2-02-05-supabase-bootstrap-schema-parity.md)
- Decision Ref: [`../../../../../../analysis/implementation-report-STORY-M2-02-05-bootstrap-parity-2026-05-10.md`](../../../../../../analysis/implementation-report-STORY-M2-02-05-bootstrap-parity-2026-05-10.md) (§5.2)

## Task: tests — edge-cases для `_coerce_jsonb_text_id_sequence`

### Цель
Расширить покрытие GAP-09-хелпера: пустые списки, JSON-строка массива, нестроковые элементы списка.

### Факты из кода
1) [`src/core/infrastructure/db_supabase.py`](../../../../../../src/core/infrastructure/db_supabase.py) строки 28–36 — `_coerce_jsonb_text_id_sequence`.
2) [`tests/test_db_supabase_jsonb_reads.py`](../../../../../../tests/test_db_supabase_jsonb_reads.py) — существующие кейсы list/str/None/tuple.

### Gap / Проблема
§5.2 отчёта: сценарии `[]`, `"[]"`, `[1,2,3]` не покрыты; регресс может пройти незамеченным.

### AC/DoD
- [ ] (P0) Тест: `_coerce_jsonb_text_id_sequence([]) == ()`.
- [ ] (P0) Тест: `_coerce_jsonb_text_id_sequence("[]") == ()`.
- [ ] (P0) Тест: `_coerce_jsonb_text_id_sequence([1, 2, 3]) == ("1", "2", "3")`.
- [ ] (P1) `pytest -q tests/test_db_supabase_jsonb_reads.py` проходит.

### Где менять код
- [`doge-complaints-gateway/tests/test_db_supabase_jsonb_reads.py`](../../../../../../tests/test_db_supabase_jsonb_reads.py)

### План выполнения
1. Добавить три функции-теста по §5.2.
2. Убедиться, что поведение хелпера уже соответствует (если нет — минимальная правка хелпера + тесты).

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_db_supabase_jsonb_reads.py
```
