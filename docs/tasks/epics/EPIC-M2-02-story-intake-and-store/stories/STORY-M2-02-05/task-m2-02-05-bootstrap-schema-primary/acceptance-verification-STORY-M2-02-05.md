# Acceptance verification — STORY-M2-02-05 (bootstrap schema parity wave)

- Story: [`../STORY-M2-02-05-supabase-bootstrap-schema-parity.md`](../STORY-M2-02-05-supabase-bootstrap-schema-parity.md)
- Input package: `doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000011-20260508-m2-02-bootstrap-schema-parity.yaml`
- Build window: [`../../../../../run-reports/gateway-build-windows/gateway-cursor-build-window--STORY-M2-02-05.md`](../../../../../run-reports/gateway-build-windows/gateway-cursor-build-window--STORY-M2-02-05.md)
- Analysis: [`../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md`](../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md)

## AC mapping

| AC | Evidence | Result |
|----|-----------|--------|
| AC-BS-01 (GAP-07) | `000_full_init.sql` + миграция `20260510_1400_m2_02_bootstrap_geo_embedding_nullable.sql`; тест `test_supabase_bootstrap_contains_stories_geo_columns_gap07` | Pass |
| AC-BS-02 (GAP-08, вариант **A**) | `ALTER COLUMN embedding DROP NOT NULL` на обеих embedding-таблицах; README bootstrap § GAP-08 A | Pass |
| AC-BS-03 (GAP-09) | `_coerce_jsonb_text_id_sequence`; тесты `test_db_supabase_jsonb_reads.py` | Pass |
| AC-BS-04 | `gateway_resolve_queue.py --verify` | Pass (`ok 4 paths`) |

## Commands run (record)

```bash
cd /Users/eslinko/Development/DOGEstonia && python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && pytest -q tests/test_supabase_bootstrap_schema.py tests/test_db_supabase_jsonb_reads.py
```

## Nested tasks

| Task | Role | Status |
|------|------|--------|
| T01 | Geo DDL bootstrap + migration | Done |
| T02 | Embedding NOT NULL → nullable (A) | Done |
| T03 | JSONB read normalization | Done |

## Operator follow-up (optional)

- Применить миграцию на stage/prod Supabase при отдельном релизном окне.
- Закрыть GAP-11 отдельно через STORY-M2-09-05 T02 (`DB_BACKEND=supabase`), без дублирования в этой story.
