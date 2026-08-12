# TASK-GW-ES-01 — Early Signal / Pre-Cluster data readiness inventory

## Meta
- **Key:** `TASK-GW-ES-01-early-signal-data-readiness-inventory`
- **Пакет:** [`early-signal-pre-cluster/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) — deliverable [`gap-analysis-early-signal-data-readiness-2026-08-09.md`](./gap-analysis-early-signal-data-readiness-2026-08-09.md) 2026-08-09
- **Приоритет:** 🟠 MED — разблокирует честный public Pulse / spa-15 без invented API
- **Тип:** Documentation task (не product story — правки только в доках / inventory; код не трогаем)
- **Skill:** `.cursor/skills/sources/jeffallan-claude-skills/skills/architecture-designer/SKILL.md`
- **Parent REQ:** [`docs/requirements/48-early-signal-pre-cluster-data-readiness.md`](../../../requirements/48-early-signal-pre-cluster-data-readiness.md)
- **Parent product:** Early Signal Dashboard Pre-Cluster (§5–6, §10, §12, §22–23, §29, §33)
- **Sibling:** [`spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md`](../../../../spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md) — contract seam TBD-question
- **Зависит от:** —
- **Разблокирует:** follow-on gateway REQ (new NN) *если* public aggregates approved; [GW-ES-02](./STORY-GW-ES-02-public-network-pulse-l1-aggregates.md) / [GW-ES-03](./STORY-GW-ES-03-public-emerging-l2-read.md); [TASK-GW-ES-04](./TASK-GW-ES-04-req48-spa15-contract-seam.md)
- **Не reopen:** Issues public read stack / clustering math / identity Voices

## Зачем простыми словами

Нужно зафиксировать, какие **уже существующие** gateway stores/read paths могут честно поддержать Early Signal (Stories activity, taxonomy/geo aggregates, cluster maturity hints) и какие пробелы требуют отдельного API/ADR — **без** назначения HTTP path/body в этом task.

## Scope

- Inventory: Stories store, story signals / labels, cluster memberships, Issues projection read.
- Mapping parent Level 1 candidate metrics → existing data vs Unknown.
- Constraints: privacy (no PII); Topic ≠ Issue; honest data; anti-threshold gaming; no EmergingSignal entity unless later REQ.
- Open questions list for PA.2 / future API REQ (не решать здесь).

## Out of scope

- Inventing `/…` paths, response schemas, or DB tables.
- Changing clustering math / promotion gates.
- Voices / unique verified persons (identity).
- SPA layout/copy (sibling 15).
- Offers.

## Что наблюдаю сейчас (verified)

См. полный inventory + matrix в SSOT:

[`gap-analysis-early-signal-data-readiness-2026-08-09.md`](./gap-analysis-early-signal-data-readiness-2026-08-09.md)

| Fact | Path |
|------|------|
| Public Issues list | [`asgi_app.py:427`](../../../../src/core/api/asgi_app.py) `GET /tallinn/issues`; [`handlers.py:362`](../../../../src/core/api/handlers.py) |
| `/metrics` service-auth, no Story counts | [`asgi_app.py:65,393`](../../../../src/core/api/asgi_app.py); [`api/metrics.py:31–38`](../../../../src/core/api/metrics.py) |
| StoryRecord opaque author keys | [`contracts.py:48–49`](../../../../src/core/domain/contracts.py) |
| Story list Protocol | [`contracts.py:79–87`](../../../../src/core/domain/contracts.py) |
| Public HTTP Story count / pulse / emerging | **Not found** on public content reads |

## Target

1. Deliverable = filled Parent metric → Existing source → Public today? → Gap table — **done** in [`gap-analysis-…§3`](./gap-analysis-early-signal-data-readiness-2026-08-09.md).
2. Explicit: **no** new public route mandated by this task / Draft-48 alone.
3. Privacy: cite opaque submitter keys; forbid PII in any *future* aggregate payload.
4. Normative: Topic≠Issue; no «Stories until Issue» counter for follow-on API REQ.
5. Sibling spa-15 referenced; contract seam TBD until follow-on gateway REQ defines a path — if ever.
6. Regression: do not break `GET /tallinn/issues` (docs/decision only).

## Acceptance Criteria

- [x] AC-GW-ES-01: Parent metric → Existing source (file/store) → Public today? (Y/N) → Gap table exists and is code-cited where known.
- [x] AC-GW-ES-02: Document states **no** new public route mandated by Draft-48 / this task alone.
- [x] AC-GW-ES-03: Privacy section cites `contracts.py:48–49` and forbids PII fields in future aggregate payloads.
- [x] AC-GW-ES-04: Topic≠Issue and no «Stories until Issue» listed as normative for follow-on API REQ.
- [x] AC-GW-ES-05: Sibling spa-15 referenced; seam TBD-question.
- [x] AC-GW-ES-06: No change to `GET /tallinn/issues` behavior under this task (docs-only unless explicit operator scope expand).

## Точки в коде (known)

- Issues public: `asgi_app.py:427`, `handlers.py:362`
- Stories Protocol: `contracts.py:79–87`
- Opaque author: `contracts.py:48–49`
- Signals: `profile/schema.py:6–13`, `contracts.py:172+`
- Cluster: `cluster/types.py:10–22`; cron `scheduler/cluster_cron.py:15+`; gate `asgi_app.py:156–178`
- Full cites: [gap-analysis §2](./gap-analysis-early-signal-data-readiness-2026-08-09.md)

## Dependencies

- Parent Early Signal §§ as in REQ-48.
- Sibling spa REQ-15 (ref).
- Issues lineage / [GW-PUBLIC-01](../issues-read-contract/STORY-GW-PUBLIC-01-public-issues-regression.md) for Level 3 public Issues (existing).
- Primer privacy (parent cites): `docs/modules/dashboard/search-matching-interviews/00-architecture-primer.md` §5.
- Not dependent on identity/gpt for this inventory.

## Open questions (from REQ-48 §6 — block API design)

См. [gap-analysis §5](./gap-analysis-early-signal-data-readiness-2026-08-09.md). Follow-up: [gap-analysis §4](./gap-analysis-early-signal-data-readiness-2026-08-09.md) — STORY-ES-02/03 + TASK-ES-04.
