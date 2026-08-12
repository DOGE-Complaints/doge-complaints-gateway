# STORY-M2-02-07: Multilingual story intake contract v2 (REQ-33)

## Meta
- Key: `STORY-M2-02-07`
- Parent Epic: [`../../../EPIC-M2-02-story-intake-and-store.md`](../../../EPIC-M2-02-story-intake-and-store.md)
- Type: Technical Story
- Status: Done (Awaiting Commits) — T01–T09; gate [`story-acceptance-gate-STORY-M2-02-07.md`](./story-acceptance-gate-STORY-M2-02-07.md)
- Stream: M2 Intake / contracts
- Decision Ref: [`../../../../../requirements/33-multilingual-story-intake-contract-v2.md`](../../../../../requirements/33-multilingual-story-intake-contract-v2.md); [`../../../../../analysis/gap-interview-decisions-2026-05-13.md`](../../../../../analysis/gap-interview-decisions-2026-05-13.md) — G-01, G-07, G-08; audit [`../../../../../analysis/audit-req33-multilingual-intake-v2-2026-05-15.md`](../../../../../analysis/audit-req33-multilingual-intake-v2-2026-05-15.md)
- Operative queue: [`../../../../gateway-active-packages/pkg-000012-20260513-req33-multilingual-intake-v2.yaml`](../../../../gateway-active-packages/pkg-000012-20260513-req33-multilingual-intake-v2.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) (T01–T05 only; **не менять** immutable paths)
- Audit follow-up override: `run_mode=story02_07_audit_req33_followup` in [`.cursor/plans/Gateway_builder.plan.md`](../../../../../../.cursor/plans/Gateway_builder.plan.md) (T06–T09)
- Skill declared: `python-pro` (runtime)

## Story Goal
Внедрить breaking change `m2.story_intake_envelope.v2`: dict `{et, ru, en}` для `title` и `description`, обязательный `session_language`, eID gate (`identity_issuer` required), SHA-256 idempotency fallback при отсутствии заголовка — по REQ-33 и gap-interview 2026-05-13. Follow-up по аудиту 2026-05-15 — observability, schema NOT NULL, тестовые хвосты.

## Scope
- Реализация и тесты по вложенным таскам T01–T05 (intake → domain → API → persistence → tests).
- Follow-up T06–T09 по [`audit-req33-multilingual-intake-v2-2026-05-15.md`](../../../../../analysis/audit-req33-multilingual-intake-v2-2026-05-15.md).
- **Суперседит** переходный контракт STORY-M2-02-06 T01–T03 (`title_hint` / `title_hint_et|ru|en`), не дублировать их отдельной story.

## Out of scope
- Multilingual отображение в SPA (REQ-33 §6; EPIC-M2-06).
- Миграция существующих v1 историй в store (отдельная story).
- `GPT UI/instructions/api-orchestrator.md` — отдельный PR вне `doge-complaints-gateway` (T05: checklist / ссылка, не блокер gateway AC).

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-m2-02-07-t01-intake-contract-v2-parse-and-validation`](./task-m2-02-07-t01-intake-contract-v2-parse-and-validation/README.md) | pkg-000012 |
| 2 | [`task-m2-02-07-t02-domain-storyrecord-v2-fields`](./task-m2-02-07-t02-domain-storyrecord-v2-fields/README.md) | pkg-000012 |
| 3 | [`task-m2-02-07-t03-api-raw-body-idempotency-sha256`](./task-m2-02-07-t03-api-raw-body-idempotency-sha256/README.md) | pkg-000012 |
| 4 | [`task-m2-02-07-t04-persistence-stories-v2-columns`](./task-m2-02-07-t04-persistence-stories-v2-columns/README.md) | pkg-000012 |
| 5 | [`task-m2-02-07-t05-tests-and-wire-contract-docs`](./task-m2-02-07-t05-tests-and-wire-contract-docs/README.md) | pkg-000012 |
| 6 | [`task-m2-02-07-t06-gap33-01-ready-v2-columns-healthcheck`](./task-m2-02-07-t06-gap33-01-ready-v2-columns-healthcheck/README.md) | audit follow-up |
| 7 | [`task-m2-02-07-t07-gap33-02-submitter-identity-issuer-not-null`](./task-m2-02-07-t07-gap33-02-submitter-identity-issuer-not-null/README.md) | audit follow-up |
| 8 | [`task-m2-02-07-t08-gap33-03-test-unsupported-session-language`](./task-m2-02-07-t08-gap33-03-test-unsupported-session-language/README.md) | audit follow-up |
| 9 | [`task-m2-02-07-t09-gap33-04-sqlite-i18n-roundtrip-e2e`](./task-m2-02-07-t09-gap33-04-sqlite-i18n-roundtrip-e2e/README.md) | audit follow-up |

## AC / DoD (story level)
- [x] REQ-33 §5: v2 payload → HTTP 202; отсутствие `identity_issuer` / `narrative.title` / `narrative.description` / `session_language` → HTTP 400; v1 `schema_version` → HTTP 400 с понятным сообщением.
- [x] Повторный POST с тем же body без `Idempotency-Key` → тот же `story_id` (G-08).
- [x] `StoryRecord` содержит dict-поля title/description/session_language; `submitter_identity_issuer` обязателен на intake.
- [x] `bullrun-launch-index.md`, `gateway-active-package.current.yaml` → `pkg-000012`, `gateway_resolve_queue.py --verify` → `ok 5 paths`.
- [x] Audit follow-up T06–T09 закрыты (см. таблицу ниже).

---

## Таблица: gap / REQ → task → файлы → статус (wave T01–T05)

| Gap / REQ | Task | Целевые файлы / артефакты | Статус |
|-----------|------|---------------------------|--------|
| G-01 v2 narrative + eID | T01 | `intake/contracts.py`, handlers 400 | Done (Awaiting Commits) |
| G-01 StoryRecord | T02 | `domain/contracts.py`, `application/services.py` | Done (Awaiting Commits) |
| G-08 idempotency | T03 | `asgi_app.py`, `handlers.py` | Done (Awaiting Commits) |
| REQ §3 persistence | T04 | `db_sqlite.py`, `db_supabase.py`, migrations | Done (Awaiting Commits) |
| REQ §5 AC / tests | T05 | `tests/test_story_intake_*`, `simulation_runner.py` | Done (Awaiting Commits) |

## Audit follow-up (2026-05-15)

| Gap | Task | Файлы | Статус |
|-----|------|-------|--------|
| GAP-33-01 | T06 | `dependencies.py`, `db_supabase.py`, readiness tests | Done (Awaiting Commits) |
| GAP-33-02 | T07 | `000_full_init.sql`, migration `20260515_*`, `db_sqlite.py` | Done (Awaiting Commits) |
| GAP-33-03 | T08 | `test_story_intake_contract.py`, `test_http_intake_endpoint.py` | Done (Awaiting Commits) |
| GAP-33-04 | T09 | `test_db_backed_pipeline_e2e.py` | Done (Awaiting Commits) |
