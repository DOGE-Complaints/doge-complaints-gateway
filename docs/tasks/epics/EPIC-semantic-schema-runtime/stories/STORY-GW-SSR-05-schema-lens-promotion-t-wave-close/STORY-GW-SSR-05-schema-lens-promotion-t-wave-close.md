# STORY-GW-SSR-05 — Pack promotion policy + T-wave close without QRY HTTP

## Meta
- **Key:** `STORY-GW-SSR-05-schema-lens-promotion-t-wave-close`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — T-wave close (sequence **5**)
- **Тип:** implement (promotion policy + negative AC-018)
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md)
- **Parent REQ:** [`51-semantic-schema-runtime.md`](../../../../../requirements/51-semantic-schema-runtime.md) §2 CL-006, §4.6–4.7, §5 AC-14/18; sibling spa 16 (SPA-003)
- **Decision:** INDEX **D-SSR-3** / **D-SSR-4** / **D-SSR-6**
- **decision_ref:** backlog SSR-05 + INDEX **D-SSR-3** / **D-SSR-4** / **D-SSR-6**
- **Siblings in package:** [SSR-01](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-01-schema-runtime-pack-load.md) Done pkg-000061; [SSR-02](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-02-structured-payload-persist.md) Done pkg-000062; [SSR-03](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-03-optional-v2-semantic-wire.md) Done pkg-000063; [SSR-04](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-04-schema-driven-cluster-lens.md) Done pkg-000064
- **Skill declared:** python-pro
- **Etalon структуры:** [STORY-GW-SSR-04](../STORY-GW-SSR-04-schema-driven-cluster-lens/STORY-GW-SSR-04-schema-driven-cluster-lens.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000065-20260828-gw-ssr-05-schema-lens-promotion-t-wave-close.yaml`](../../../../gateway-active-packages/pkg-000065-20260828-gw-ssr-05-schema-lens-promotion-t-wave-close.yaml)
- **Git:** только `semantic-schema-runtime` — [runbook Шаг 0](../../../../backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md)
- **Зависит от:** SSR-04
- **Scaffolded:** 2026-08-28T14:50:23Z

### Трассировка
| Слой | Документ | §§ |
|------|----------|-----|
| Child REQ | 51 §2 CL-006, §4.6–4.7, §5 AC-14/18 | |
| Parent | CL-006; AC-014/018; SPA-003 | |
| Decision | INDEX **D-SSR-3** identity; **D-SSR-4** `src/core/schema/` + pack data; **D-SSR-6** SSR-06/07 Draft not T-wave DoD | |

- **Разблокирует:** T-wave close (G5). **Not** SSR-06/07
- **Не reopen:** civic `require_actionable` default; civic factory policy; `structured_payload` on public Issue; QRY HTTP; second cron; ClusterLens; identity
- **Не трогаем:** identity-service / claim keys (**D-SSR-3**)

## Nested tasks (pkg-000065)

| ID | Folder |
|----|--------|
| T01 | [`task-gw-ssr-05-t01-pack-policy-mapper`](./task-gw-ssr-05-t01-pack-policy-mapper/README.md) |
| T02 | [`task-gw-ssr-05-t02-optional-gate-policy-command`](./task-gw-ssr-05-t02-optional-gate-policy-command/README.md) |
| T03 | [`task-gw-ssr-05-t03-pack-promote-clustered`](./task-gw-ssr-05-t03-pack-promote-clustered/README.md) |
| T04 | [`task-gw-ssr-05-t04-public-card-no-payload`](./task-gw-ssr-05-t04-public-card-no-payload/README.md) |
| T05 | [`task-gw-ssr-05-t05-negative-ac-018-no-qry`](./task-gw-ssr-05-t05-negative-ac-018-no-qry/README.md) |
| T06 | [`task-gw-ssr-05-t06-civic-promotion-regression`](./task-gw-ssr-05-t06-civic-promotion-regression/README.md) |
| T07 | [`task-gw-ssr-05-t07-story-acceptance-gate`](./task-gw-ssr-05-t07-story-acceptance-gate/README.md) |

## Зачем простыми словами

Membership ≠ promotion. Pack может promote без civic `complaint`/`system_bug`; civic built-in остаётся для civic tests. T-wave закрываем **без** generic filter HTTP и без processor delivery.

## Scope / Out of scope

**In:** CL-006 (membership / worthiness / projection); AC-014; civic built-in `complaint`+`system_bug` default for civic lenses (AC-008 green); `GET /tallinn/issues` remains public Issue **read**; `structured_payload` MUST NOT auto-become public Issue (SPA-003); AC-018: no QRY HTTP, no Phase F/G processor delivery to close T-wave.

**Out:** invent promotion numeric thresholds or new public Issue type enums (parent CL-006); invent Issue field names; SPA card overlay (sibling 16); processor plugins (→ SSR-07 Draft); generic filter API (→ SSR-06 Draft); identity (**D-SSR-3**). Civic numeric defaults in `PromotionGatePolicy` — **не** копировать как SSOT пака.

## Verified current state

### As-of-Done (SSR-05 pkg-000065)

| Fact | Ref |
|------|-----|
| Civic actionable types | [`gates.py:7`](../../../../../../src/core/promotion/gates.py) `ACTIONABLE_CANONICAL_TYPES = frozenset({"complaint", "system_bug"})` |
| Default require actionable type | [`gates.py:14`](../../../../../../src/core/promotion/gates.py) `require_actionable_canonical_type: bool = True` |
| Civic numeric defaults (built-in only) | [`gates.py:12–13`](../../../../../../src/core/promotion/gates.py) `min_readiness_score=70`, `min_stories=2` |
| Pack mapper | [`pack_policy.py:9–19`](../../../../../../src/core/schema/pack_policy.py) `promotion_gate_policy_from_pack` — 3 knobs from pack file |
| Optional `gate_policy` | [`issue_create.py:36`](../../../../../../src/core/application/issue_create.py); `_create_issue` `policy=command.gate_policy` [`:232`](../../../../../../src/core/application/issue_create.py) |
| Per-call submit | [`service.py:81–85`](../../../../../../src/core/promotion/service.py) `effective_policy = self.gate_policy if policy is None else policy` |
| Pack promote + CLUSTERED | [`_promote_pack_membership`](../../../../../../src/core/application/cluster_orchestrator.py) [`:138–216`](../../../../../../src/core/application/cluster_orchestrator.py); lifecycle [`:191`](../../../../../../src/core/application/cluster_orchestrator.py); `process_story` pack [`:236–237`](../../../../../../src/core/application/cluster_orchestrator.py) |
| Public Issue list | [`asgi_app.py:462`](../../../../../../src/core/api/asgi_app.py) `GET /tallinn/issues` |
| Public card shape | [`dto.py:26–36`](../../../../../../src/core/projection/dto.py) `DOGEIssue.to_public_dict` — **нет** `structured_payload` |

### Historical (pre-P3)

| Fact | Ref |
|------|-----|
| Pack readiness policy as data | **Not found** |
| Issue create always civic gates | [`issue_create.py:226–229`](../../../../../../src/core/application/issue_create.py) `submit_for_review` without `policy=` |
| `submit_for_review` | всегда `self.gate_policy` ([`service.py:84–86`](../../../../../../src/core/promotion/service.py) pre-override) |
| Pack CLUSTERED cite | [`cluster_orchestrator.py:369`](../../../../../../src/core/application/cluster_orchestrator.py) (civic `_create_issue_for_cluster` line, pre-pack-promote) |

## Стыковка с кодом

Civic default **не** менять: `PromotionGatePolicy()` и factory [`service_factory.py:108–111`](../../../../../../src/core/infrastructure/service_factory.py) остаются civic (`require_actionable_canonical_type=True`, пороги из config).

**As-of-Done:** `submit_for_review(..., policy=)` uses `effective_policy` ([`service.py:85`](../../../../../../src/core/promotion/service.py)). Pack override **на этот вызов** (`IssueCreateCommand.gate_policy`), не смена singleton. Mapper [`pack_policy.py`](../../../../../../src/core/schema/pack_policy.py). Pack CLUSTERED after successful promote [`cluster_orchestrator.py:188–193`](../../../../../../src/core/application/cluster_orchestrator.py) — статус-only, binding не трёт.

**Historical:** `submit_for_review` всегда `self.gate_policy`; pack CLUSTERED cite civic `:369`.

T-wave pack policy **мапится только на 3 существующих knobs** ([`gates.py:11–14`](../../../../../../src/core/promotion/gates.py)). CL-003 `algorithm` / `scope` / `scale` / `missing_value_policy` в promotion **не** invent новыми `reasons`. Числа — из example pack (SSR-01 T00), не civic `70`/`2` как Python SSOT пака.

`readiness_score` в `IssueCreateCommand` civic считает `readiness_score_for_cluster(..., lens: ClusterLens)` — pack **не** звать. T-wave минимум: если `len(members) >= pack.min_size`, score ≥ pack `min_readiness_score` из файла пака; иначе score ниже порога (gate fail). Это не новая наука скоринга.

**Не** вести pack через `_create_issue_for_cluster` as-is: preview civic policy + `IssueCreateCommand` без override + `readiness_for_story` civic.

Честно: optional `gate_policy` на `IssueCreateCommand` (None = civic). Civic callers не передают поле.

Карточка Issues: не добавлять payload в `DOGEIssue` (SPA-003 уже так в [`dto.py:26–36`](../../../../../../src/core/projection/dto.py)).

Проекция pack Issue = civic narrative поля (title/description required на intake). `structured_payload` не становится public card.

AC-018: grep `asgi_app.py` — нет нового filter route; `build_index` остаётся no-op из SSR-01.

## Подзадачи

| ID | Слой | Задача | Где | Не делать |
|----|------|--------|-----|-----------|
| **T01** | Pack policy | Mapper loader keys (SSR-01 T00) → `PromotionGatePolicy` на **этот** вызов: `require_actionable_canonical_type=False`, `min_stories`/`min_readiness_score` из pack file. | schema pack + mapper | Менять default/factory civic policy; invent 4-й knob |
| **T02** | Issue create | Optional `gate_policy` на `IssueCreateCommand`; `submit_for_review(..., policy=…)`. None = `self.gate_policy`. | [`issue_create.py`](../../../../../../src/core/application/issue_create.py), [`service.py`](../../../../../../src/core/promotion/service.py) | Ломать civic `_create_issue` path |
| **T03** | Pack promote | Та же orchestrator-ветка SSR-04: после membership, если pack gate pass → `create_issue` + `CLUSTERED`. Score не из civic `readiness_score_for_cluster`. | [`cluster_orchestrator.py`](../../../../../../src/core/application/cluster_orchestrator.py) | `_create_issue_for_cluster` as-is; второй cron |
| **T04** | Projection | Assert `to_public_dict` без `structured_payload`; type/title с civic narrative. | [`dto.py`](../../../../../../src/core/projection/dto.py) + test | Новые Issue field names |
| **T05** | Negative AC-018 | Нет generic filter HTTP; processor delivery не требуется. | `asgi_app.py` routes + gate | |
| **T06** | Civic regression | Existing clustering/promotion tests green (AC-008). | `tests/test_clustering_engine.py` etc. | |
| **T07** | Gate | AC-014/018; Product T-wave close. SSR-06/07 не в DoD. | | |

## Target / AC

- [x] AC-GW-REQ3-14 / AC-014: schema-pack exact-lens cluster promotes under pack readiness policy **without** civic type tokens; civic-lens tests still pass.
- [x] Civic built-in remains; not the only platform rule (CL-006).
- [x] AC-GW-REQ3-18 / AC-018: T-wave accepted without generic analytical filter HTTP (AC-005) and without processor delivery.
- [x] Public read path unchanged: `GET /tallinn/issues`; payload not automatic on Issue (SPA-003) — no invented field names.
- [x] §29 Compatibility: pack-lens promote without civic types; civic promotion tests green.

## Точки в коде

- Civic gates: [`gates.py`](../../../../../../src/core/promotion/gates.py) — default не трогать.
- Civic issue path: [`issue_create.py:210`](../../../../../../src/core/application/issue_create.py), [`cluster_orchestrator.py:269`](../../../../../../src/core/application/cluster_orchestrator.py).
- Public card: [`dto.py`](../../../../../../src/core/projection/dto.py); HTTP [`asgi_app.py:462`](../../../../../../src/core/api/asgi_app.py).

## Dependencies

- SSR-04. spa-16 overlay — sibling, не эта реализация.
- После Done T-wave: **не** считать SSR-06/07 частью close (INDEX sequence 6–7 Draft).
