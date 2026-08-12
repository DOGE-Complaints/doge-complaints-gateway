# TASK-GW-ES-04 — REQ-48 PA.2 sync + spa-15 contract seam (docs)

## Meta
- **Key:** `TASK-GW-ES-04-req48-spa15-contract-seam`
- **Пакет:** [`early-signal-pre-cluster/`](./INDEX.md)
- **Status:** ⚪ Todo
- **Приоритет:** 🟡 MED-LOW — docs/seam; разблокирует согласованный public exposure list
- **Тип:** Documentation task (не product story — cross-repo seam / PA.2; **без** API implementation)
- **Gaps:** [G-ES-DOC-01](./gap-analysis-early-signal-data-readiness-2026-08-09.md), [G-ES-DOC-02](./gap-analysis-early-signal-data-readiness-2026-08-09.md)

### Трассировка
| Слой | Документ | §§ / якорь |
|------|----------|------------|
| **Parent product** | [`DOGEstonia-Early-Signal-Dashboard-Pre-Cluster-Product-Requirements.md`](../../../../../docs/requirements%20backlog/DOGEstonia-Early-Signal-Dashboard-Pre-Cluster-Product-Requirements.md) | §§5–6 levels; §10/§12 blocks; contract seam note (siblings TBD) |
| **Project REQ** | [`48-early-signal-pre-cluster-data-readiness.md`](../../../requirements/48-early-signal-pre-cluster-data-readiness.md) | Status Draft awaiting PA.2; **AC-GW-ES-05** sibling seam; §6 open Q |
| **Sibling** | [`15-early-signal-pre-cluster-public-dashboard.md`](../../../../spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md) | Status Draft awaiting PA.2; sibling gateway 48; «no invent gateway paths» |
| **Gap SSOT** | [`gap-analysis-…`](./gap-analysis-early-signal-data-readiness-2026-08-09.md) | §1.5 seam TBD; G-ES-DOC-01/02; matrix §3 |
| **Prior** | [TASK-GW-ES-01](./TASK-GW-ES-01-early-signal-data-readiness-inventory.md) | Done — gap deliverable |

- **Зависит от:** TASK-ES-01 gap SSOT; operator **PA.2** on REQ-48 and/or spa-15
- **Разблокирует:** clearer backlog for ES-02/03 exposure scope; не API сам по себе
- **Не reopen:** TASK-ES-01 inventory facts; Issues L3

## Зачем простыми словами

Inventory (TASK-ES-01) уже зафиксировал, что внутри gateway есть / чего нет публично. REQ-48 и spa-15 всё ещё Draft: нужно после PA.2 синхронизировать статусы и явно список «какие L1/L2 факты можно отдавать наружу» — без написания endpoint.

## Что наблюдаю сейчас

| Fact | Ref |
|------|-----|
| Gap matrix + constraints Done | [`gap-analysis-…`](./gap-analysis-early-signal-data-readiness-2026-08-09.md) |
| REQ-48 Status | Draft — awaiting PA.2 |
| spa-15 Status | Draft — awaiting PA.2; invent gateway paths out of scope |
| Seam | TBD-question both sides |

## Целевое состояние

1. REQ-48 updated post-PA.2: Status + pointer to gap matrix (AC-01 table live in gap SSOT).
2. Seam section (in REQ-48 and/or this package short note): **decided** vs **still open** public exposure facts for spa-15 ↔ gateway.
3. If path still TBD — state so explicitly; **do not invent** path in this docs task.
4. Link ES-02/03 as consumers of decided exposure list.

## Acceptance Criteria

- [ ] REQ-48 points at [`gap-analysis-…`](./gap-analysis-early-signal-data-readiness-2026-08-09.md) matrix; Status reflects PA.2 outcome.
- [ ] Seam artifact lists decided vs open L1/L2 public facts (spa-15 ↔ gateway).
- [ ] No HTTP path invented solely to «close» TBD.
- [ ] ES-02/03 Meta/Depends updated if exposure decisions change blockers.

## Границы

- **In scope:** docs / PA.2 sync / cross-repo seam list.
- **Вне scope:** implement Pulse/Emerging API; spa UI mockups; Voices identity ADR; answering open Q without operator PA.2.

## Условие активации

- Operator runs PA.2 на REQ-48 and/or spa-15 **или** explicit request to sync Status/seam from current gap SSOT without full PA.2.
