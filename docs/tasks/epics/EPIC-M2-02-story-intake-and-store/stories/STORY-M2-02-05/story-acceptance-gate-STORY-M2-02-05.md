# Story acceptance gate — STORY-M2-02-05

- Story: `STORY-M2-02-05`
- Gate status: **PASS** (implementation + automated checks; операторская приёмка коммитов — по политике команды)
- Scope: GAP-07, GAP-08 (вариант A), GAP-09; `pkg-000011-20260508-m2-02-bootstrap-schema-parity.yaml`

## Evidence

- `supabase/bootstrap/000_full_init.sql` — шесть geo-колонок на `public.stories`; `ALTER COLUMN embedding DROP NOT NULL` для `story_embeddings` и `doge_issue_embeddings`.
- `supabase/migrations/20260510_1400_m2_02_bootstrap_geo_embedding_nullable.sql` — идемпотентная дельта для уже развёрнутых БД.
- `src/core/infrastructure/db_supabase.py` — `_coerce_jsonb_text_id_sequence` и использование в `SupabaseIssueCandidateStore` / `SupabaseReviewAuditLogRepository`.
- Тесты: `tests/test_supabase_bootstrap_schema.py` (geo + embedding nullable), `tests/test_db_supabase_jsonb_reads.py`.
- `python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify` → `ok 4 paths` для `pkg-000011-20260508-m2-02-bootstrap-schema-parity.yaml`.
- Отчёт волны: [`./task-m2-02-05-bootstrap-schema-primary/acceptance-verification-STORY-M2-02-05.md`](./task-m2-02-05-bootstrap-schema-primary/acceptance-verification-STORY-M2-02-05.md).
