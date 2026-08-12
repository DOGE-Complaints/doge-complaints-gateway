# STORY-GW-ES-02 — Public Network Pulse L1 aggregates (`GET /tallinn/network-pulse`)

## Meta
- **Key:** `STORY-GW-ES-02-public-network-pulse-l1-aggregates`
- **Пакет:** [`early-signal-pre-cluster/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) — pipeline gate PASS 2026-08-10T10:55:48Z pkg-000059 · [`STORY-GW-ES-02`](../../epics/EPIC-M2-24-early-signal-pre-cluster/stories/STORY-GW-ES-02-public-network-pulse-l1-aggregates/STORY-GW-ES-02-public-network-pulse-l1-aggregates.md) · epic [`EPIC-M2-24`](../../epics/EPIC-M2-24-early-signal-pre-cluster.md) · REQ-49 path `GET /tallinn/network-pulse`
- **Приоритет:** 🟠 MED — разблокирует spa-15 Network Pulse (honest data)
- **Тип:** implement (application read-model + public GET; HTTP path **не** invent в этой постановке)
- **Gaps:** [G-ES-PUB-01](./gap-analysis-early-signal-data-readiness-2026-08-09.md), [G-ES-PUB-02](./gap-analysis-early-signal-data-readiness-2026-08-09.md); note [G-ES-INV-01](./gap-analysis-early-signal-data-readiness-2026-08-09.md) (`/metrics` unfit)
- **Etalon структуры:** [STORY-GW-DRAFT-01](../story-draft-handoff/STORY-GW-DRAFT-01-story-draft-stash.md) (слои + DI + T0N)

### Трассировка
| Слой | Документ | §§ / якорь |
|------|----------|------------|
| **Parent product** | [`DOGEstonia-Early-Signal-Dashboard-Pre-Cluster-Product-Requirements.md`](../../../../../docs/requirements%20backlog/DOGEstonia-Early-Signal-Dashboard-Pre-Cluster-Product-Requirements.md) | §5.1 L1 Raw Activity; **§10** Network Pulse; §22–23 honest / anti-gaming; §29 privacy |
| **Project REQ** | [`48-early-signal-pre-cluster-data-readiness.md`](../../../requirements/48-early-signal-pre-cluster-data-readiness.md) | §4.4–5 Level 1; AC-GW-ES-02..04 constraints; §6 open Q 1/3/4/5 |
| **Sibling** | [`15-early-signal-pre-cluster-public-dashboard.md`](../../../../spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md) | Network Pulse block; contract TBD with gateway |
| **Gap SSOT** | [`gap-analysis-…§3–4`](./gap-analysis-early-signal-data-readiness-2026-08-09.md) | L1 Public=N; G-ES-PUB-01/02 |
| **Prior** | [TASK-GW-ES-01](./TASK-GW-ES-01-early-signal-data-readiness-inventory.md) | Done — inventory |

- **Зависит от:** TASK-ES-01 Done; **follow-on gateway REQ (new NN)** that names public path+payload — **или** явный operator go-ahead to open path design (**T00**)
- **Разблокирует:** spa-15 Pulse wiring (после контракта); не spa layout
- **Не reopen:** Issues L3 / PUBLIC-01; Voices (identity); clustering math; `/metrics` semantics

## Зачем простыми словами

Пользователь на board должен видеть, что Stories уже есть (Network Pulse), без выдачи Topics за Issues и без PII. До ES-02 данные (`list_stories` + labels) были внутри gateway без публичного aggregate; story закрыла gap через application-сервис + public GET (path SSOT: REQ-49).

## Текущее состояние (post-Done, pkg-000059)

| Fact | Ref |
|------|-----|
| Public Pulse route | `GET /tallinn/network-pulse` in [`PUBLIC_ROUTES`](../../../../src/core/api/asgi_app.py) (`:65`) + `@app.get` (`:434–439`) |
| Handler | [`handle_network_pulse`](../../../../src/core/api/handlers.py) (`:40`) → `dependencies.network_pulse_service.build_pulse()` |
| Application service | [`NetworkPulseService`](../../../../src/core/application/network_pulse.py) (`:30`) / `build_pulse` (`:36`) |
| DI | [`ApiDependencies.network_pulse_service`](../../../../src/core/api/dependencies.py) (`:28`) wired in `build_api_dependencies` (`:92`) |
| Factory | [`get_network_pulse_service`](../../../../src/core/infrastructure/service_factory.py) (`:157`) |
| Topics filter | `is_public_label_disposition` in [`network_pulse.py:69`](../../../../src/core/application/network_pulse.py) |
| `/metrics` ≠ Pulse | [`api/metrics.py`](../../../../src/core/api/metrics.py) — no Story Pulse aggregates; service-auth |
| Gate | PASS 2026-08-10T10:55:48Z · pkg-000059 |

## Что наблюдаю — pre-Done (historical)

> **Historical.** Снимок **до** ES-02 implementation. Не текущее runtime-состояние.

| Fact | Ref (as of pre-Done) |
|------|-----|
| No public pulse / story-count route | `PUBLIC_ROUTES` without `/tallinn/network-pulse` |
| DI без pulse | `ApiDependencies` без `network_pulse_service` |
| Cabinet activity anti-pattern | activity dig via `story_intake_service.repository` in cabinet handler — **не копировать** для Pulse |
| L3 public etalon | `GET /tallinn/issues` без service-auth |

## Требование / целевое состояние

### MVP product defaults (закрывают open Q для DoD)

- **Обязательно:** `stories_collected` = `len(StoryRepository.list_stories())`.
- **В том же сервисе (dims):**  
  - `languages` — distinct counts by `narrative_language` (skip null/empty);  
  - `areas` — distinct counts by `geo.admin_district` (fallback: `admin_settlement` / `admin_region` если district пуст); honesty: small sample ≠ city coverage;  
  - `topics` — frequency of taxonomy labels via `StoryLabelRepository` (**keys/docs must say topic/label, never Issue**);  
  - `recent_stories_7d` — count where `created_at` within last 7 days (UTC).
- **Out:** Voices / unique submitters; PII; reuse `/metrics`.

### A. Application — `NetworkPulseService`

- Новый модуль `src/core/application/network_pulse.py` (рядом со `story_activity.py`).
- `@dataclass(frozen=True) class NetworkPulseService` с явными зависимостями:
  - `story_repository: StoryRepository`
  - `story_label_repository: StoryLabelRepository | None` (topics dim; если None → topics `[]` / omit per payload contract)
- Метод `build_pulse(*, now: datetime | None = None) -> dict[str, Any]` — **public** scope (без submitter filter).
- Payload: только non-PII aggregates; **не** включать `submitter_*`, narrative text, contacts.
- Агрегация MVP: list + in-memory fold (как Issues fetch-all path). SQL/`count` RPC — **out of first DoD** (gap open Q5 follow-up).

### B. DI / Factory — без cabinet-hack

- `DefaultServiceFactory.get_network_pulse_service()` (или эквивалент) собирает сервис из `story_repository` + `story_label_repository`.
- Поле `network_pulse_service: NetworkPulseService` на [`ApiDependencies`](../../../../src/core/api/dependencies.py); проводка в `build_api_dependencies()`.
- Handler вызывает **`dependencies.network_pulse_service`**, **не** `story_intake_service.repository`.

### C. API — public GET (path from REQ)

- Handler `handle_network_pulse(deps, …)` → `build_success_envelope(data=pulse)`.
- `@app.get(<PATH_FROM_REQ_NN>)` **без** `require_*_service_auth` (паттерн Issues list).
- Добавить тот же path в `PUBLIC_ROUTES` tuple ([`asgi_app.py:57–64`](../../../../src/core/api/asgi_app.py)).
- **T00:** literal path+payload schema берутся **только** из follow-on REQ/ADR; в этой стори path не invent.

### D. Normative / privacy

- Topic ≠ Issue в ключах ответа и runtime-docs.
- Нет поля/копи «N Stories until Issue».
- Issues L3 (`GET /tallinn/issues`) unchanged.

### E. Tests

- Unit: `NetworkPulseService` на in-memory repos (stories_collected, dims, 7d window, no PII keys).
- HTTP: public GET без auth → 200 envelope; Issues regression smoke green.

## Подзадачи

| ID | Слой | Задача |
|----|------|--------|
| **T00** | Gate | Follow-on gateway REQ (new NN) или ADR cites **path + payload** contract; иначе stop before T03 |
| **T01** | Application | `NetworkPulseService.build_pulse()` — stories_collected + languages/areas/topics/recent_7d; non-PII |
| **T02** | DI | `DefaultServiceFactory` + `ApiDependencies.network_pulse_service` + `build_api_dependencies` |
| **T03** | API | Handler + `@app.get` (path from REQ) + `PUBLIC_ROUTES` entry; envelope success |
| **T04** | Normative | Payload keys/docs: Topic≠Issue; no threshold-gaming counter |
| **T05** | Tests | Unit service + HTTP public smoke; Issues L3 regression unchanged |
| **T06** | Runtime-docs | OpenAPI + API_REFERENCE после path named |

## Acceptance Criteria

- [x] T00: follow-on REQ/ADR names path + payload (не invent path только в этой стори).
- [x] `NetworkPulseService` exists; `stories_collected` grounded on `list_stories`.
- [x] MVP dims (languages / areas / topics / recent_7d) implemented or explicitly omitted only if REQ payload narrower — then update this AC.
- [x] Wired via `ApiDependencies` / factory — **not** via `story_intake_service.repository` dig.
- [x] Public GET (no service-auth) returns envelope; path in `PUBLIC_ROUTES`.
- [x] Topic ≠ Issue; no «N Stories until Issue»; no PII / Voices.
- [x] `/metrics` not used for Pulse.
- [x] `GET /tallinn/issues` behavior unchanged (regression).

## Runtime-docs дельта

- [`api-reference/openapi.yaml`](../../../runtime-docs/api-reference/openapi.yaml) — path from REQ.
- [`api-reference/API_REFERENCE.md`](../../../runtime-docs/api-reference/API_REFERENCE.md) — Network Pulse L1; Topic≠Issue note.
- При необходимости pointer из REQ-48 / spa-15 seam ([TASK-GW-ES-04](./TASK-GW-ES-04-req48-spa15-contract-seam.md)).

## Открытые под-вопросы (реализация)

- Точный JSON shape keys — только в follow-on REQ (T00).
- k-anonymity / min cell size (gap Q3): MVP = raw distinct counts; если PA.2 потребует floor — follow-up AC, не silent invent.
- Perf: если demo load страдает от full `list_stories` — отдельный SQL count story (не в T01–T05 DoD).

## Швы

| Слой | Файлы |
|------|--------|
| Application | новый `network_pulse.py`; etalon [`story_activity.py`](../../../../src/core/application/story_activity.py) |
| Domain ports | [`contracts.py`](../../../../src/core/domain/contracts.py) `StoryRepository`, `StoryLabelRepository` — **без** нового entity |
| Factory / infra | [`service_factory.py`](../../../../src/core/infrastructure/service_factory.py), [`providers.py`](../../../../src/core/infrastructure/providers.py) |
| DI | [`dependencies.py`](../../../../src/core/api/dependencies.py) |
| API | [`handlers.py`](../../../../src/core/api/handlers.py), [`asgi_app.py`](../../../../src/core/api/asgi_app.py), [`envelope.py`](../../../../src/core/api/envelope.py) |
| Tests | `tests/test_gw_es_02_*` (паттерн `test_gw_public_01_*`) |

## Границы

- **In scope:** Pulse L1 application + DI + public GET after path named.
- **Вне scope:** invent path here; Voices; Emerging L2 (→ ES-03); spa layout; clustering math; EmergingSignal table; changing Issues.

## Зависимости / связь

- Inventory: [TASK-GW-ES-01](./TASK-GW-ES-01-early-signal-data-readiness-inventory.md).
- Seam preferred: [TASK-GW-ES-04](./TASK-GW-ES-04-req48-spa15-contract-seam.md) (exposure list) — soft; MVP dims выше достаточны для старта после T00.
- Sibling L2: [GW-ES-03](./STORY-GW-ES-03-public-emerging-l2-read.md).
- L3 regression lineage: [GW-PUBLIC-01](../issues-read-contract/STORY-GW-PUBLIC-01-public-issues-regression.md).
