# STORY-GW-ES-03 — Public Emerging L2 read (derived, ≠ Issues)

## Meta
- **Key:** `STORY-GW-ES-03-public-emerging-l2-read`
- **Пакет:** [`early-signal-pre-cluster/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) — P3 PASS 2026-08-10T12:17:38Z pkg-000060; REQ-50 `GET /tallinn/emerging-signals` · [`gate`](../../epics/EPIC-M2-24-early-signal-pre-cluster/stories/STORY-GW-ES-03-public-emerging-l2-read/task-gw-es-03-t07-story-acceptance-gate/story-acceptance-gate-STORY-GW-ES-03.md) · epic [`EPIC-M2-24`](../../epics/EPIC-M2-24-early-signal-pre-cluster.md)
- **Приоритет:** 🟠 MED — Level 2 discovery без путаницы с Issues
- **Тип:** implement (derived application read-model + public GET; path **не** invent здесь)
- **Gaps:** [G-ES-PUB-03](./gap-analysis-early-signal-data-readiness-2026-08-09.md)
- **Etalon структуры:** [STORY-GW-DRAFT-01](../story-draft-handoff/STORY-GW-DRAFT-01-story-draft-stash.md); wire — Issues list; aggregate — [ES-02](./STORY-GW-ES-02-public-network-pulse-l1-aggregates.md) / [`StoryActivityService`](../../../../src/core/application/story_activity.py)

### Трассировка
| Слой | Документ | §§ / якорь |
|------|----------|------------|
| **Parent product** | [`DOGEstonia-Early-Signal-Dashboard-Pre-Cluster-Product-Requirements.md`](../../../../../docs/requirements%20backlog/DOGEstonia-Early-Signal-Dashboard-Pre-Cluster-Product-Requirements.md) | §5.2 L2 Emerging Structure; **§6.2** Emerging Signal (ephemeral, not Issue); **§12** Emerging Signals block; §22–23; §33 no invent clustering gates |
| **Project REQ** | [`48-early-signal-pre-cluster-data-readiness.md`](../../../requirements/48-early-signal-pre-cluster-data-readiness.md) | §4.6 Level 2; §6 open Q 2 |
| **Sibling** | [`15-early-signal-pre-cluster-public-dashboard.md`](../../../../spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md) | Emerging Signals block; L2 ≠ L3 UX |
| **Gap SSOT** | [`gap-analysis-…§3`](./gap-analysis-early-signal-data-readiness-2026-08-09.md) | L2 Public=**Y** (`GET /tallinn/emerging-signals`); G-ES-PUB-03 Closed by ES-03 |
| **Prior** | [TASK-GW-ES-01](./TASK-GW-ES-01-early-signal-data-readiness-inventory.md) Done; typically after/parallel [GW-ES-02](./STORY-GW-ES-02-public-network-pulse-l1-aggregates.md) DI family |

- **Зависит от:** TASK-ES-01 Done; MVP L2 rule ниже (closes open Q2 for this story); path SSOT **REQ-50** (T00 Done)
- **Разблокирует:** spa-15 Emerging Signals data (после контракта / TASK-ES-04)
- **Не reopen:** Issues projection semantics; cluster promotion thresholds (parent §33); EmergingSignal persistent entity

## Зачем простыми словами

Доска должна показывать «паттерны начинают формироваться» без выдачи их за confirmed Issues. Story закрыла gap: **derived** read-model (`EmergingSignalsService`) + public GET (path SSOT: REQ-50) — не таблица `EmergingSignal` и не копия `GET /tallinn/issues`.

## Текущее состояние (post-Done, pkg-000060)

| Fact | Ref |
|------|-----|
| Public Emerging route | `GET /tallinn/emerging-signals` in [`PUBLIC_ROUTES`](../../../../src/core/api/asgi_app.py) (`:67`) + `@app.get` (`:450–459`) |
| Handler | [`handle_emerging_signals`](../../../../src/core/api/handlers.py) (`:51`) → `dependencies.emerging_signals_service.build_emerging(...)` |
| Application service | [`EmergingSignalsService`](../../../../src/core/application/emerging_signals.py) (`:36`) / `build_emerging` (`:57`) |
| DI | [`ApiDependencies.emerging_signals_service`](../../../../src/core/api/dependencies.py) (`:30`) wired in `build_api_dependencies` (`:95`) |
| Factory | [`get_emerging_signals_service`](../../../../src/core/infrastructure/service_factory.py) |
| Path+payload SSOT | [`50-early-signal-emerging-l2-api.md`](../../../requirements/50-early-signal-emerging-l2-api.md) |
| L3 Issues (≠ Emerging) | `GET /tallinn/issues` [`asgi_app.py:462`](../../../../src/core/api/asgi_app.py) |
| Gate | PASS 2026-08-10T12:17:38Z · pkg-000060 |

## Что наблюдаю — pre-Done (historical)

> **Historical.** Снимок **до** ES-03 implementation. Не текущее runtime-состояние.

| Fact | Ref (as of pre-Done) |
|------|-----|
| Possible L2 inputs | `story_labels` / `story_signals` / `cluster_memberships`; readiness `list_stories_ready_for_clustering` |
| Labels / link / published map | `StoryLabelRepository`; `IssueStoryLinkStore`; `map_issue_status_to_cabinet` |
| No public emerging route | `PUBLIC_ROUTES` without `/tallinn/emerging-signals` |
| No EmergingSignal entity required | parent §6.2; REQ-48 §2 |
| Cabinet DI anti-pattern | activity dig via `issue_create_service.issue_story_link_store` — **не копировать** для Emerging |

## MVP derivation rule (closes open Q2 for this story)

**Emerging L2 = top-N taxonomy label frequencies** across stories, **excluding** any story that links to an Issue projection whose status maps to **published** (reuse cabinet mapping / `canonicalize_status_on_read`).

- Source of labels: `StoryLabelRepository.list_by_story` (per story) or equivalent axis fold — **not** `IssueProjectionReadStore.list_projections` as the emerging source.
- Output: ephemeral list `{ label, axis?, story_count, … }` — **Topic/label language**, never Issue ids as the primary emerging identity.
- **Not equal** to Issues list shape/source.
- **No** persistent `EmergingSignal` table in this story.
- Clustering / promotion gates **unchanged**.

## Требование / целевое состояние

### A. Application — `EmergingSignalsService`

- Новый модуль `src/core/application/emerging_signals.py`.
- `@dataclass(frozen=True)` deps:
  - `story_repository: StoryRepository`
  - `story_label_repository: StoryLabelRepository`
  - `issue_story_link_store: IssueStoryLinkStore | None`
  - `issue_projection_read_store: IssueProjectionReadStore`
- `build_emerging(*, top_n: int = …) -> dict[str, Any]`:
  1. `list_stories()`;
  2. for each story: if linked issue is published → skip labels from that story;
  3. aggregate label frequencies; take top-N;
  4. return non-PII structure (no submitter keys, no narrative text).

### B. DI / Factory

- `DefaultServiceFactory.get_emerging_signals_service()` from existing repos/stores (labels already on factory; link store from issue_create wiring — **expose explicitly**, not dig via intake).
- `ApiDependencies.emerging_signals_service`; `build_api_dependencies()` wires it.
- Handler uses **`dependencies.emerging_signals_service` only**.

### C. API — public GET (path from REQ-50)

- Handler → `build_success_envelope`.
- `@app.get("/tallinn/emerging-signals")` without service-auth; path ∈ `PUBLIC_ROUTES` ([`asgi_app.py:67,450`](../../../../src/core/api/asgi_app.py)).
- **T00 Done:** path+payload SSOT = [`50-early-signal-emerging-l2-api.md`](../../../requirements/50-early-signal-emerging-l2-api.md).

### D. Normative

- Topic ≠ Issue; anti «N until Issue».
- Contract/tests prove Emerging response **≠** Issues projection list (different handler/service/source).
- Parent §33: do not change `CLUSTER_MIN_SIZE` / promotion gates.

### E. Tests

- Unit: published-linked stories excluded; top-N ordering; no PII keys.
- Contract: Emerging payload must not be the same as `list_projections` Issues envelope shape used by board L3.
- HTTP public smoke; Issues regression green.

## Подзадачи (pipeline pkg-000060 + audit T08–T10)

| ID | Слой | Задача |
|----|------|--------|
| **T00** | Gate | Path named in follow-on REQ/ADR; document MVP L2 rule (this story §) as Q2 close for MVP |
| **T01** | Application | `EmergingSignalsService` — label-freq top-N + exclude published-issue stories |
| **T02** | DI | Factory + `ApiDependencies.emerging_signals_service` (no repository dig) |
| **T03** | API | Public GET + `PUBLIC_ROUTES` (path from REQ-50) |
| **T04** | Normative | Topic≠Issue; Emerging ≠ Issues contract notes |
| **T05** | Tests | Unit/HTTP + Emerging≠Issues + Issues regression |
| **T06** | Docs | OpenAPI/API_REFERENCE after path named |
| **T07** | Gate | Story acceptance gate |
| **T08** | Docs (audit) | R1 post-Done observation — `run_mode=gw_es_03_audit_followup` |
| **T09** | Docs (audit) | R2+G3 gap-analysis Public=Y |
| **T10** | Docs (audit) | R3+R4 shell cites sync |

## Acceptance Criteria

- [x] T00: path+payload named outside this file alone.
- [x] MVP rule implemented: label frequency; exclude published-linked stories; documented in runtime-docs.
- [x] No `EmergingSignal` table/migration in this story.
- [x] Service on `ApiDependencies` / factory — not cabinet dig pattern.
- [x] Public GET; path in `PUBLIC_ROUTES`.
- [x] Response distinct from `GET /tallinn/issues` (test).
- [x] Topic ≠ Issue; no threshold-gaming counter; clustering gates unchanged.
- [x] No PII in payload.

## Runtime-docs дельта

- OpenAPI + API_REFERENCE — Emerging L2; explicit «not Issues» note.
- Cross-link gap / TASK-ES-04 exposure if seam updated.

## Открытые под-вопросы (реализация)

- Exact `top_n` default and multi-axis — **closed by REQ-50** (default 10, clamp [1,50]; all public axes).
- Whether `story_signals` / memberships later replace labels — **out**; successor story + ADR / ES-08.
- k-anonymity floor — same as ES-02 (PA.2 / follow-up).

## Швы

| Слой | Файлы |
|------|--------|
| Application | новый `emerging_signals.py`; status helper reuse from [`story_activity.py`](../../../../src/core/application/story_activity.py) |
| Domain | existing `StoryLabelRepository` / `StoryRepository` — **no** new entity |
| Issue links / read | [`issue_create.py`](../../../../src/core/application/issue_create.py) protocols |
| Factory / DI | [`service_factory.py`](../../../../src/core/infrastructure/service_factory.py), [`dependencies.py`](../../../../src/core/api/dependencies.py) |
| API | [`handlers.py`](../../../../src/core/api/handlers.py), [`asgi_app.py`](../../../../src/core/api/asgi_app.py) |
| Tests | `tests/test_gw_es_03_*` + Issues regression |

## Границы

- **In scope:** derived L2 read-model + DI + public GET after path named.
- **Вне scope:** invent path; Pulse L1 (→ ES-02); Voices; spa layout; EmergingSignal DDL; changing promotion/cluster math; Offers.

## Зависимости / связь

- [TASK-GW-ES-01](./TASK-GW-ES-01-early-signal-data-readiness-inventory.md); soft [TASK-GW-ES-04](./TASK-GW-ES-04-req48-spa15-contract-seam.md).
- Parallel/after [GW-ES-02](./STORY-GW-ES-02-public-network-pulse-l1-aggregates.md) (shared DI discipline).
- L3 must stay: [GW-PUBLIC-01](../issues-read-contract/STORY-GW-PUBLIC-01-public-issues-regression.md).
