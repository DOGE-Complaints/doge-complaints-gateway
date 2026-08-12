# STORY-M2-02-05: Supabase bootstrap schema parity (data model vs `000_full_init.sql`)

## Meta
- Key: `STORY-M2-02-05`
- Parent Epic: [`../../../EPIC-M2-02-story-intake-and-store.md`](../../../EPIC-M2-02-story-intake-and-store.md)
- Type: Technical Story
- Status: Implemented (Waiting Acceptance)
- Stream: M2 Story Store / Supabase DDL parity
- Analysis reference (Decision Ref): [`../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md`](../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md)
- Post-verification follow-up: [`../../../../../analysis/implementation-report-STORY-M2-02-05-bootstrap-parity-2026-05-10.md`](../../../../../analysis/implementation-report-STORY-M2-02-05-bootstrap-parity-2026-05-10.md) §5–§8 (gap-verification follow-up tasks T04–T09; исполнение через **override** в [`../../../../../../../.cursor/plans/Gateway_builder.plan.md`](../../../../../../../.cursor/plans/Gateway_builder.plan.md), метка чата `run_mode=story02_05_verification_followup`, без смены `pkg-000011`)
- Skill declared: `python-pro`

## Story Goal
Устранить блокирующие расхождения между кодом PostgREST-слоя (`src/core/infrastructure/db_supabase.py`) и каноническим bootstrap [`supabase/bootstrap/000_full_init.sql`](../../../../../../supabase/bootstrap/000_full_init.sql), зафиксированные в анализе (GAP-07, GAP-08, GAP-09), чтобы свежий bootstrap + `DB_BACKEND=supabase` позволял intake, чтение историй и запись эмбеддингов без HTTP 400 из-за схемы.

## Cross-epic note (GAP-11)
Операционное закрытие «процесс пишет в память при пустой Supabase» остаётся в существующем таске **STORY-M2-09-05 T02** — [`../../../EPIC-M2-09-security-config-observability/stories/STORY-M2-09-05/task-m2-09-05-t02-gap-trace-00b-db-backend-supabase/README.md`](../../../EPIC-M2-09-security-config-observability/stories/STORY-M2-09-05/task-m2-09-05-t02-gap-trace-00b-db-backend-supabase/README.md). Эта story не дублирует отдельный таск по `DB_BACKEND`.

## AC / DoD
- [x] AC-BS-01 (P0): В `000_full_init.sql` (и при необходимости новой миграции под `supabase/migrations/`) присутствуют все колонки geo для `public.stories`, которые выбирает и пишет `SupabaseStoryRepository` (см. анализ §1.4, GAP-07).
- [x] AC-BS-02 (P0): Таблицы `public.story_embeddings` и `public.doge_issue_embeddings` согласованы с фактом записи кода: либо `embedding` nullable/удалён по выбранному decision, либо код заполняет колонку — без нарушения NOT NULL при INSERT (анализ §3, §5, GAP-08). **Решение:** вариант A — `ALTER COLUMN embedding DROP NOT NULL`.
- [x] AC-BS-03 (P1): Чтение JSONB `story_ids_json` / `related_story_ids_json` в Supabase-сторе кандидатов и audit не использует `json.loads(str(list))` для значений, которые PostgREST уже десериализовал в `list` (анализ §6–7, GAP-09).
- [x] AC-BS-04: `python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify` проходит для активного `pkg-000011-20260508-m2-02-bootstrap-schema-parity.yaml` после добавления путей задач.

## Acceptance artifacts

- Story gate: [`./story-acceptance-gate-STORY-M2-02-05.md`](./story-acceptance-gate-STORY-M2-02-05.md)
- Wave verification: [`./task-m2-02-05-bootstrap-schema-primary/acceptance-verification-STORY-M2-02-05.md`](./task-m2-02-05-bootstrap-schema-primary/acceptance-verification-STORY-M2-02-05.md)
- Phase log: [`./task-m2-02-05-bootstrap-schema-primary/BULLRUN-PHASE-LOG.md`](./task-m2-02-05-bootstrap-schema-primary/BULLRUN-PHASE-LOG.md)

## Nested tasks

| Order | Slug | Task folder |
|-------|------|---------------|
| 1 | primary | `task-m2-02-05-bootstrap-schema-primary` |
| 2 | T01 | `task-m2-02-05-t01-gap-bootstrap-stories-geo-columns` |
| 3 | T02 | `task-m2-02-05-t02-gap-bootstrap-embeddings-not-null` |
| 4 | T03 | `task-m2-02-05-t03-gap-jsonb-read-issue-candidates-audit` |
| 5 | T04 | `task-m2-02-05-t04-tests-bootstrap-geo-ddl-assertions` |
| 6 | T05 | `task-m2-02-05-t05-tests-jsonb-coerce-edge-cases` |
| 7 | T06 | `task-m2-02-05-t06-gap-06-live-story-context-consistency-notes` |
| 8 | T07 | `task-m2-02-05-t07-gap-10-pytest-logging-lifespan` |
| 9 | T08 | `task-m2-02-05-t08-cross-layer-stories-schema-invariant` |
| 10 | T09 | `task-m2-02-05-t09-gap-11-db-backend-default-regression` |

## Task Artifacts
- primary: [`./task-m2-02-05-bootstrap-schema-primary/README.md`](./task-m2-02-05-bootstrap-schema-primary/README.md)
- T01: [`./task-m2-02-05-t01-gap-bootstrap-stories-geo-columns/README.md`](./task-m2-02-05-t01-gap-bootstrap-stories-geo-columns/README.md)
- T02: [`./task-m2-02-05-t02-gap-bootstrap-embeddings-not-null/README.md`](./task-m2-02-05-t02-gap-bootstrap-embeddings-not-null/README.md)
- T03: [`./task-m2-02-05-t03-gap-jsonb-read-issue-candidates-audit/README.md`](./task-m2-02-05-t03-gap-jsonb-read-issue-candidates-audit/README.md)
- T04: [`./task-m2-02-05-t04-tests-bootstrap-geo-ddl-assertions/README.md`](./task-m2-02-05-t04-tests-bootstrap-geo-ddl-assertions/README.md)
- T05: [`./task-m2-02-05-t05-tests-jsonb-coerce-edge-cases/README.md`](./task-m2-02-05-t05-tests-jsonb-coerce-edge-cases/README.md)
- T06: [`./task-m2-02-05-t06-gap-06-live-story-context-consistency-notes/README.md`](./task-m2-02-05-t06-gap-06-live-story-context-consistency-notes/README.md)
- T07: [`./task-m2-02-05-t07-gap-10-pytest-logging-lifespan/README.md`](./task-m2-02-05-t07-gap-10-pytest-logging-lifespan/README.md)
- T08: [`./task-m2-02-05-t08-cross-layer-stories-schema-invariant/README.md`](./task-m2-02-05-t08-cross-layer-stories-schema-invariant/README.md)
- T09: [`./task-m2-02-05-t09-gap-11-db-backend-default-regression/README.md`](./task-m2-02-05-t09-gap-11-db-backend-default-regression/README.md)
