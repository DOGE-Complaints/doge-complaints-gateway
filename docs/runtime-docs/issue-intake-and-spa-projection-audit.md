# Issue Intake и SPA Projection: фактический аудит runtime

## Цель документа

Зафиксировать по коду:

1. какой входной payload реально обрабатывается для создания сущности на intake-слое;
2. есть ли в этом входе SPA-совместимый projection-объект;
3. если нет, где и как он строится в коде;
4. где есть разрыв между существующим runtime API и моделями `intake`/`projection`.

Источники: `src/core/**`, `tests/**`, `docs/runtime-docs/api-reference/openapi.yaml`.

## 1) Фактический HTTP runtime на текущий момент

В `src/core/api/asgi_app.py` для бизнес-потока активен только `POST /intake/stories`.  
`POST /issues` отсутствует в runtime surface (проверяется `tests/test_http_issue_create_endpoint.py`).

## 2) Входная модель данных `StoryIntakeRequest` (as-is)

Контракт задается `parse_story_intake_request()` в `src/core/intake/contracts.py`.

### 2.1 Required поля

- `schema_version = "m2.story_intake_envelope.v1"`
- `submitter.external_user_id`
- `narrative.original_text`
- `narrative.language` (`et | ru | en`)
- `narrative.title_hint`

### 2.2 Optional поля

- `submitter.identity_issuer`
- `narrative.location_query`
- `narrative.canonical_type`
- `narrative.canonical_labels`
- `origin.*`
- `privacy.contains_pii`, `privacy.redaction_requested` (strict bool when present)
- `live_story_context.consistency_notes`

## 3) Runtime flow: intake -> cluster -> issue -> projection -> storage

1. API handler: `handle_story_intake()` парсит payload и создает story через `StoryIntakeService`.
2. `StoryIntakeService.create_story()`:
   - idempotency check/store,
   - story persistence (`StoryRepository`),
   - story embedding persistence (`StoryEmbeddingStore`) c `embedding_policy_version`.
3. После успешного intake вызывается `StoryClusterOrchestrator.process_story(story_id)`.
4. Оркестратор вычисляет cluster memberships и при готовности запускает `IssueCreateService.create_issue(...)`.
5. `IssueCreateService`:
   - проводит promotion checks,
   - строит projection draft через `StoryPromotionProjectionBridge` + `StoryToProjectionPolicy`,
   - materialize SPA projection через `IssueProjectionService`,
   - сохраняет projection (`IssueProjectionStore`),
   - сохраняет linkage (`IssueStoryLinkStore`),
   - сохраняет issue embedding (`IssueProjectionEmbeddingStore`) с policy version.

## 4) Где формируется SPA projection

Во входном intake payload **нет** готового SPA projection объекта.

Он формируется только внутри projection stack:

- `src/core/projection/extraction_policy.py`
- `src/core/projection/input.py`
- `src/core/projection/service.py`
- `src/core/projection/dto.py`

Итоговый shape для dashboard: `id/status/type/labels/title/summary/description` + optional fields.

## 5) Contracts and storage

- Stories: `stories` + `idempotency_keys` + `story_embeddings`
- Issues: `spa_issue_projections` + `spa_issue_projection_embeddings`
- Process linkage: `issue_candidates`, `review_audit_log`, `issue_story_links`
- Supabase read-model для SPA: `issues_dashboard` view

## 6) Достаточность данных для projection

Текущий intake контракт уже содержит минимально нужные поля для deterministic story->issue extraction без дополнительной AI модели на этом этапе:

- narrative text/title/language
- optional canonical hints (`canonical_type`, `canonical_labels`)
- submitter/origin/privacy metadata для governance/audit

Ограничение: качество кластеризации и типизации issue сейчас rule-based и зависит от policy heuristic; это ожидаемое ограничение текущей demo-wave.

## 7) Verification evidence

- HTTP boundary: `tests/test_http_intake_endpoint.py`, `tests/test_http_issue_create_endpoint.py`
- Story-first e2e: `tests/test_e2e_intake_create_spa_contract.py`, `tests/test_e2e_story_cluster_issue_pipeline.py`
- Projection contract: `tests/test_spa_projection.py`, `tests/test_story_promotion_projection_bridge.py`
- Embedding/versioning/linkage: `tests/test_embedding_policy_versioning.py`, `tests/test_process_linkage_sqlite.py`

## 8) Gap Register (SSOT)

| gap_id | Симптом (факт кода) | Статус | Закрыто в |
|---|---|---|---|
| GAP-IP-001 | ~~Нет HTTP intake endpoint (`POST /intake/stories`) в runtime~~ | **Closed** | `asgi_app.py:140-152`, `handlers.py:114-154` |
| GAP-IP-002 | Удален manual HTTP issue-create endpoint в пользу story-first boundary | **Closed** | `asgi_app.py` (без `/issues`), `handlers.py` (без `handle_issue_create`) |
| GAP-IP-003 | ~~Нет bridge `Story/Promotion -> ProjectionInput`~~ | **Closed** | `application/issue_create.py:38-75` — `StoryPromotionProjectionBridge` |
| GAP-IP-004 | Нет внешнего (requirements-level) контракта policy заполнения SPA полей (type/labels derivation) | **Planned** | Policy есть в runtime (`EXTRACTION_POLICY_VERSION`), но не вынесен как отдельный продуктовый контракт |
| GAP-IP-005 | ~~Нет e2e pipeline-контрактов от HTTP intake/create до SPA payload~~ | **Closed** | `tests/test_e2e_intake_create_spa_contract.py` + `tests/test_story_promotion_projection_bridge.py` |

## 10) Rule: gap ownership and closure

Каждый `gap_id` должен существовать в одном из состояний:

- `Planned` — есть `owner task key` в backlog;
- `In Progress` — owner task выполняется;
- `Closed` — owner task в `Done (Committed)` и есть run-report ссылка;
- `Deferred` — есть явное обоснование в матрице трассировки.
