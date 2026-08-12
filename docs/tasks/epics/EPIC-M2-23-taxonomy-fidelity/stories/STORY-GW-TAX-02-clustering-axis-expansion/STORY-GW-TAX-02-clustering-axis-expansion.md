# STORY-GW-TAX-02 — Clustering axis expansion (композит + новые оси)

## Meta
- **Key:** `STORY-GW-TAX-02-clustering-axis-expansion`
- **Parent Epic:** [`../../../EPIC-M2-23-taxonomy-fidelity.md`](../../../EPIC-M2-23-taxonomy-fidelity.md)
- **Type:** feature (cluster engine + lenses + per-lens threshold)
- **Status:** 🔵 Done (Awaiting Commits) — gate PASS 2026-07-15 pkg-000055
- **Приоритет:** 🟠 MED — issue-карточки сейчас грубые (одна ось = сфера); богатый civic-смысл не влияет на группировку
- **Цель:** **Цель 2** — таксономия используется в кластеризации осмысленно
- **source:** [`../../../../backlog-stories/taxonomy-fidelity/STORY-GW-TAX-02-clustering-axis-expansion.md`](../../../../backlog-stories/taxonomy-fidelity/STORY-GW-TAX-02-clustering-axis-expansion.md)
- **Основание (решения):** [`interview-clustering-axes-2026-07-13`](../../../../analysis/interview-clustering-axes-2026-07-13.md) — **D-CLUST-1..4** (уточняют [D-TAX-4](../../../../analysis/interview-taxonomy-persistence-clustering-2026-07-13.md))
- **Зависит от:** [GW-TAX-01](../STORY-GW-TAX-01-taxonomy-persistence-fidelity/STORY-GW-TAX-01-taxonomy-persistence-fidelity.md) (per-axis данные в `story_labels`; Done pkg-000054)
- **Эпик-связь:** [`EPIC-M2-17 Living Issues Cluster Growth`](../../../EPIC-M2-17-living-issues-cluster-growth-model.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000055-20260715-gw-tax-02-clustering-axis-expansion.yaml`](../../../../gateway-active-packages/pkg-000055-20260715-gw-tax-02-clustering-axis-expansion.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **6** тасков T01–T06
- **decision_ref:** backlog + interview D-CLUST-1..4

## Зачем простыми словами
Сейчас issue-карточка на доске = «все истории одной **сферы**» (напр. «Мусор» — всё скопом). Грубо и не actionable. Богатый смысл (конкретный **объект**, глубинная **нужда**, упадок **среды**) в группировке не участвует. Нужно сделать карточки **точнее и осмысленнее**: основной ключ — связка «сфера + тип сбоя» («Не вывозят баки»), плюс новые оси как дополнительные линзы — но аккуратно с порогом, чтобы доска не опустела.

## Что наблюдаю сейчас (verified по коду — ИСПРАВЛЕНО)
> Прошлая формулировка «текущих 2 оси civic_domain+failure_pattern» **неточна** (см. [interview §1](../../../../analysis/interview-clustering-axes-2026-07-13.md)). Реальность:

| Элемент | Реальность |
|---------|-----------|
| Кто создаёт карточку | **только primary-линза** ([cluster_orchestrator.py:239,144](../../../../../../src/core/application/cluster_orchestrator.py#L239)) |
| Primary сейчас | **`civic_domain`** (одна ось) — `CLUSTER_PRIMARY_LENS=civic_domain_micro` ([.env:34](../../../../../../.env)) |
| Ключ линзы | `lens:dimension:value:scope\|geo` — **одно** значение одной оси ([cluster/engine.py:70](../../../../../../src/core/cluster/engine.py#L70)) |
| `domain+pattern` | **только debug-лейбл** ([cluster_orchestrator.py:139](../../../../../../src/core/application/cluster_orchestrator.py#L139)), не группировка |
| Активные линзы | 6 ([CIVIC_LENSES](../../../../../../src/core/cluster/engine.py#L20)); 5 из них считаются, но карточки не создают |
| `SignalDimension` | 13 значений; есть `CIVIC_DOMAIN`/`FAILURE_PATTERN`/`NEED`; **нет** `service_object`, `ecosystem_signal` ([contracts.py:20](../../../../../../src/core/domain/contracts.py#L20)) |
| Порог | `CLUSTER_MIN_SIZE` (prod-цель 8; demo `.env`=2), единый |
| Источник сигналов | `infer_signals_from_canonical` (пере-угадывание) → после GW-TAX-01 брать из `story_labels` per-axis |

## Требование / целевое состояние (D-CLUST-1..4)
1. **Composite-primary ключ (D-CLUST-1/2):** primary-группировка = **`civic_domain + failure_pattern`** (связка, не одна ось). Пример: `waste + maintenance_gap` → «Не вывозят баки». Требует новой возможности движка (сейчас ключ = одно значение одной оси).
2. **Новые оси (D-CLUST-3):** добавить **`service_object`**, **`deep_need`**, **`ecosystem_signal`** как линзы/фасеты:
   - `service_object`, `ecosystem_signal` — **новые** `SignalDimension` + `ClusterLens`;
   - `deep_need` — маппинг на существующий `NEED` (или новый dimension);
   - `failure_pattern` — уже линзa (входит в composite-primary).
3. **Источник — `story_labels` (D-TAX-1):** сигналы осей берутся из per-axis данных (GW-TAX-01), не пере-угадываются словарями.
4. **Порог по-линзово (D-CLUST-4):** per-lens `min_size` — composite-primary (сфера+сбой) выше (8); `service_object`/`deep_need`/`ecosystem_signal` ниже. Не понижать порог глобально.
5. Пересчёт [`expected-board-fill-matrix`](../../../EPIC-M2-19-demo-data-seeding/stories/STORY-GW-SEED-02-dataset-expansion-for-clustering/task-gw-seed-02-t04-expected-board-fill-matrix/expected-board-fill-matrix.md) (SEED-02) под composite + новые оси.

## Подзадачи (pipeline queue)
| ID | Task | Type | Status |
|----|------|------|--------|
| T01 | [Composite primary cluster key](./task-gw-tax-02-t01-composite-primary-cluster-key/README.md) | implement | ✅ Done |
| T02 | [New signal dimensions and lenses](./task-gw-tax-02-t02-new-signal-dimensions-and-lenses/README.md) | implement | ✅ Done |
| T03 | [Story labels signal source](./task-gw-tax-02-t03-story-labels-signal-source/README.md) | implement | ✅ Done |
| T04 | [Per-lens min size config](./task-gw-tax-02-t04-per-lens-min-size-config/README.md) | implement | ✅ Done |
| T05 | [Expected board fill matrix recalc](./task-gw-tax-02-t05-expected-board-fill-matrix-recalc/README.md) | tests | ✅ Done |
| T06 | [Story acceptance gate](./task-gw-tax-02-t06-story-acceptance-gate/README.md) | gate | ✅ Done |

## Acceptance Criteria
- [x] Primary issue-ключ = composite `civic_domain + failure_pattern` (не одна ось); карточки предметнее («сфера: сбой»)
- [x] Добавлены оси `service_object`, `deep_need`, `ecosystem_signal` (из `story_labels` per-axis) как линзы/фасеты
- [x] Per-lens `min_size`: composite-primary=8, богатые оси ниже; глобально не понижен
- [x] Демо-доска (v0_2) не опустела; existing cluster-тесты + full offline suite green

## Границы
- **In scope:** composite-primary, новые оси/линзы, per-lens порог, источник из `story_labels`.
- **Вне scope:** приём/хранение таксономии → [GW-TAX-01](../STORY-GW-TAX-01-taxonomy-persistence-fidelity/STORY-GW-TAX-01-taxonomy-persistence-fidelity.md); GPT-контракт → GPT-TAX-01; «параллельные доски-линзы» (D-CLUST-1 отклонено — возможное будущее расширение).
- **Не понижать** `CLUSTER_MIN_SIZE` глобально ради наполнения (D-CLUST-4).

## Швы
- Движок: [`cluster/engine.py`](../../../../../../src/core/cluster/engine.py) (`cluster_key_for_lens`, `CIVIC_LENSES`, `lens_dimension`), [`cluster/types.py`](../../../../../../src/core/cluster/types.py) (`ClusterLens`); оркестратор: [`application/cluster_orchestrator.py`](../../../../../../src/core/application/cluster_orchestrator.py) (primary + `_resolve_min_size_guard`); сигналы: [`profile/enrichment.py`](../../../../../../src/core/profile/enrichment.py); enum: [`domain/contracts.py` SignalDimension](../../../../../../src/core/domain/contracts.py#L20); конфиг: [`config/schema.py`](../../../../../../src/core/config/schema.py) (`CLUSTER_*`); сборка: [`infrastructure/service_factory.py:83`](../../../../../../src/core/infrastructure/service_factory.py#L83).
