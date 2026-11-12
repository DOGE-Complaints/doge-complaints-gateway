# STORY-GW-SSR-04 — Schema-pack exact lens membership (civic ClusterLens preserved)

## Meta
- **Key:** `STORY-GW-SSR-04-schema-driven-cluster-lens`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — T-wave clustering (sequence **4**)
- **Тип:** implement (common engine + data lens)
- **Parent REQ:** 51 §2 CL, §4.5–4.6, §5 AC-07; parent CL-001…005, AC-007/008
- **Skill declared:** python-pro
- **Git:** только `semantic-schema-runtime` — [runbook Шаг 0](./orchestrator-t-wave-runbook.md)
- **Зависит от:** SSR-02

## Зачем простыми словами

Хотя бы одна exact-линза из pack data, без нового члена `ClusterLens`. Civic линзы и тесты остаются зелёными. Membership ≠ Issue.

## Scope / Out of scope

**In:** schema-driven exact membership (AC-007, CL-001/003); coexist with civic engine (CL-002); multiple memberships (CL-004); T-wave MAY cluster on pack-declared payload fields (51 §4.5); civic tests AC-008; SEC-004: sensitive fields not automatic in cluster narratives.

**Out:** new `ClusterLens` enum member for the example pack lens; invent promotion thresholds (→ SSR-05); `story_dimensions` / filter HTTP (→ SSR-06 Draft); identity (**D-SSR-3**); invent pack YAML keys beyond parent example **shape**.

## Verified current state

### As-of-Done (SSR-04 pkg-000064)

| Fact | Ref |
|------|-----|
| `ClusterLens` StrEnum (10 members; no pack lens) | [`types.py:10–22`](../../../../src/core/cluster/types.py) |
| `CIVIC_LENSES` tuple | [`engine.py:20–31`](../../../../src/core/cluster/engine.py) |
| Pack exact engine | [`pack_engine.py`](../../../../src/core/schema/pack_engine.py) `SchemaPackClusterEngine` / `pack_cluster_id` [`:44–46`](../../../../src/core/schema/pack_engine.py); `is_schema_bound` [`:16–18`](../../../../src/core/schema/pack_engine.py) |
| `lens_dimension` exhaustive on enum | [`engine.py:66–79`](../../../../src/core/cluster/engine.py) — KeyError на неизвестном enum |
| Signals source | [`get_signals_for_story`](../../../../src/core/profile/enrichment.py) `:87` — labels/canonical **не** payload |
| Orchestrator split | pack → `_process_pack_bound_story` then return None [`cluster_orchestrator.py:143–145`](../../../../src/core/application/cluster_orchestrator.py); civic pool `_civic_ready` [`:86–87`](../../../../src/core/application/cluster_orchestrator.py); `process_all_pending` pack then civic [`:215–221`](../../../../src/core/application/cluster_orchestrator.py) |
| Pack persist | `save_membership` in `_process_pack_bound_story` [`:109–114`](../../../../src/core/application/cluster_orchestrator.py); no Issue / no `CLUSTERED` |
| Civic persist after Issue | `CLUSTERED` then `_persist_memberships` [`:422–436`](../../../../src/core/application/cluster_orchestrator.py); `_persist_memberships` [`:452–468`](../../../../src/core/application/cluster_orchestrator.py) |
| Cron | [`cluster_cron.py:64`](../../../../src/core/scheduler/cluster_cron.py) still `process_all_pending` only |
| Factory | [`service_factory.py:158`](../../../../src/core/infrastructure/service_factory.py) `schema_pack_engine=SchemaPackClusterEngine()` |
| Membership store | `lens: str` [`contracts.py:206–208`](../../../../src/core/domain/contracts.py); table [`db_sqlite.py:351–356`](../../../../src/core/infrastructure/db_sqlite.py) |

### Historical (pre-P3)

| Fact | Ref |
|------|-----|
| Orchestrator pool | `list_stories_ready_for_clustering()` **все** READY_FOR_PROFILE (no `_civic_ready`) |
| Pack engine | **Not found** — planned as «новый `SchemaPackClusterEngine`» |
| Civic `_persist_memberships` cite | [`cluster_orchestrator.py:365–381`](../../../../src/core/application/cluster_orchestrator.py) (pre-pack-branch line numbers) |

## Стыковка с кодом

**Запрещённый «удобный» таск (invariant):** `ClusterLens.POLICE_STATION = "police_station"` + строка в `lens_dimension`. Это ломает AC-001/007 и civic enum.

**As-of-Done путь:** `SchemaPackClusterEngine` в [`pack_engine.py`](../../../../src/core/schema/pack_engine.py) — dotted paths на `structured_payload`; `cluster_id` = `schema:<schema_id>:<lens_id>:…`; `save_membership(story_id, lens=pack_lens_id, cluster_id=…)`. Civic `ClusteringEngine` / `test_clustering_engine.py` / `test_gw_tax_02_*` **не** расширять enum.

**Фильтр + точка вызова (As-of-Done):** [`cluster_cron.py:64`](../../../../src/core/scheduler/cluster_cron.py) зовёт только `process_all_pending`. **Не** второй cron. Schema-bound → `_process_pack_bound_story` [`cluster_orchestrator.py:89–145`](../../../../src/core/application/cluster_orchestrator.py); civic без этих stories (`_civic_ready`). Pack без persist binding (SSR-02 None) остаётся civic.

**Membership ≠ Issue (As-of-Done):** civic `_persist_memberships` + `CLUSTERED` только после успешного `create_issue` ([`cluster_orchestrator.py:422–436`](../../../../src/core/application/cluster_orchestrator.py), [`:452–468`](../../../../src/core/application/cluster_orchestrator.py)). Pack пишет `save_membership` **без** Issue. Lifecycle до promote **не** `CLUSTERED` — стори остаётся `READY_FOR_PROFILE`; engine идемпотентен на повтор cron.

CL-004: pack lens ids + civic lens ids на одном `story_id` (PK `story_id, lens`) **только если** civic не прогонялся. Для pack-bound civic memberships не писать.

`cluster_id` pack: namespace `schema:<schema_id>:<lens_id>:…`, не `stable_cluster_id(lens: ClusterLens, …)` — иначе коллизия с [`find_promoted_by_cluster_id`](../../../../src/core/application/issue_create.py) `:198`.

SEC-004: pack **не** копировать raw payload в narrative string. Civic `build_cluster_narrative` принимает `ClusterLens` — не вызывать для pack.

Зависит от persist fields (SSR-02). Wire (SSR-03) нужен для e2e intake; unit engine может фикстурить `StoryRecord` с payload.

## Подзадачи

| ID | Слой | Задача | Где | Не делать |
|----|------|--------|-----|-----------|
| **T01** | Pack engine | Exact membership from payload paths; unknown path → skip/error typed; `cluster_id` namespaced; no `ClusterLens` member; не звать `readiness_score_for_cluster` / `build_cluster_narrative`. | new module | Править `lens_dimension` dict |
| **T02** | Isolation + invoke | Ветка в `process_story` / `process_all_pending`: schema-bound → pack engine, civic pool без этих stories. Cron **не** менять. Civic tests на unlabeled fixtures зелёные. | [`cluster_orchestrator.py`](../../../../src/core/application/cluster_orchestrator.py) | Второй `ClusterCronJob`; мешать pack в civic buckets; менять `list_stories_ready_for_clustering` SQL так, что civic fixtures пропадут |
| **T03** | Persist membership | `ClusterMembershipStore.save_membership` **до** Issue; идемпотентный upsert. | sqlite/supabase stores as-is | Новая таблица; civic `_persist_memberships` |
| **T04** | Lifecycle | Не ставить `CLUSTERED` в этой стори (это SSR-05 после promote). Повтор cron не плодит дубли membership. | | Копировать civic «membership only after issue» |
| **T05** | Tests | Two stories same `institution.office_id` (example path) → same cluster_id; civic `test_clustering_engine.py` unchanged green; no new enum value in `types.py`; schema-bound не попадает в civic buckets. | `tests/test_gw_ssr_04_*` | |
| **T06** | Gate | AC-007/008. | | |

## Target / AC

- [x] AC-GW-REQ3-07 / AC-007: exact lens over structured fields → memberships without new hard-coded `ClusterLens` member.
- [x] AC-008: existing Tallinn civic clustering + issue projection tests still pass.
- [x] CL-004: Story MAY have multiple memberships; no exclusive collapse.
- [x] SEC-004: no automatic sensitive payload in cluster narratives.

## Точки в коде

- Civic (не расширять): [`types.py`](../../../../src/core/cluster/types.py), [`engine.py`](../../../../src/core/cluster/engine.py), [`enrichment.py`](../../../../src/core/profile/enrichment.py).
- Стык: [`cluster_orchestrator.py`](../../../../src/core/application/cluster_orchestrator.py), [`ClusterMembershipStore`](../../../../src/core/domain/contracts.py).
- Pack lens block: parent CL-001 YAML = example shape (T00 pack из SSR-01).

## Dependencies

- SSR-02. Civic TAX-02 — compatibility, not replace.
- Может идти параллельно с SSR-03 после SSR-02.
