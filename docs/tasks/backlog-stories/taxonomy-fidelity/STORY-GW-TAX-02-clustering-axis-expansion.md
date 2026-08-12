# STORY-GW-TAX-02 — Clustering axis expansion (композит + новые оси)

## Meta
- **Key:** `STORY-GW-TAX-02-clustering-axis-expansion`
- **Пакет:** [`taxonomy-fidelity/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) — gate PASS 2026-07-15 pkg-000055
- **Приоритет:** 🟠 MED — issue-карточки сейчас грубые (одна ось = сфера); богатый civic-смысл не влияет на группировку
- **Тип:** feature (cluster engine + lenses + per-lens threshold)
- **Цель:** **Цель 2** — таксономия используется в кластеризации осмысленно
- **Основание (решения):** [`interview-clustering-axes-2026-07-13`](../../../analysis/interview-clustering-axes-2026-07-13.md) — **D-CLUST-1..4** (уточняют [D-TAX-4](../../../analysis/interview-taxonomy-persistence-clustering-2026-07-13.md))
- **Зависит от:** [GW-TAX-01](./STORY-GW-TAX-01-taxonomy-persistence-fidelity.md) (per-axis данные в `story_labels`)
- **Эпик-связь:** [`EPIC-M2-17 Living Issues Cluster Growth`](../../epics/EPIC-M2-17-living-issues-cluster-growth-model.md)

## Зачем простыми словами
Сейчас issue-карточка на доске = «все истории одной **сферы**» (напр. «Мусор» — всё скопом). Грубо и не actionable. Богатый смысл (конкретный **объект**, глубинная **нужда**, упадок **среды**) в группировке не участвует. Нужно сделать карточки **точнее и осмысленнее**: основной ключ — связка «сфера + тип сбоя» («Не вывозят баки»), плюс новые оси как дополнительные линзы — но аккуратно с порогом, чтобы доска не опустела.

## Что наблюдаю сейчас (verified по коду — ИСПРАВЛЕНО)
> Прошлая формулировка «текущих 2 оси civic_domain+failure_pattern» **неточна** (см. [interview §1](../../../analysis/interview-clustering-axes-2026-07-13.md)). Реальность:

| Элемент | Реальность |
|---------|-----------|
| Кто создаёт карточку | **только primary-линза** ([cluster_orchestrator.py:239,144](../../../../src/core/application/cluster_orchestrator.py#L239)) |
| Primary сейчас | **`civic_domain`** (одна ось) — `CLUSTER_PRIMARY_LENS=civic_domain_micro` ([.env:34](../../../../.env)) |
| Ключ линзы | `lens:dimension:value:scope\|geo` — **одно** значение одной оси ([cluster/engine.py:70](../../../../src/core/cluster/engine.py#L70)) |
| `domain+pattern` | **только debug-лейбл** ([cluster_orchestrator.py:139](../../../../src/core/application/cluster_orchestrator.py#L139)), не группировка |
| Активные линзы | 6 ([CIVIC_LENSES](../../../../src/core/cluster/engine.py#L20)); 5 из них считаются, но карточки не создают |
| `SignalDimension` | 13 значений; есть `CIVIC_DOMAIN`/`FAILURE_PATTERN`/`NEED`; **нет** `service_object`, `ecosystem_signal` ([contracts.py:20](../../../../src/core/domain/contracts.py#L20)) |
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
5. Пересчёт [`expected-board-fill-matrix`](../../epics/EPIC-M2-19-demo-data-seeding/stories/STORY-GW-SEED-02-dataset-expansion-for-clustering/task-gw-seed-02-t04-expected-board-fill-matrix/expected-board-fill-matrix.md) (SEED-02) под composite + новые оси.

## Подзадачи (firm — активация-ready)
| ID | Задача | Швы |
|----|--------|-----|
| T01 | Composite-primary: движок строит ключ из **связки** осей (`civic_domain`+`failure_pattern`); расширить `cluster_key_for_lens` (сейчас `lens:dimension:value:scope`) на composite-key + primary-линза | [`cluster/engine.py:70,182`](../../../../src/core/cluster/engine.py#L70) |
| T02 | Новые `SignalDimension` `service_object`/`ecosystem_signal` + `ClusterLens` + `lens_dimension`-маппинг; `deep_need`→ существующий `NEED` | [`domain/contracts.py:137`](../../../../src/core/domain/contracts.py#L137), [`cluster/types.py`](../../../../src/core/cluster/types.py) |
| T03 | Источник сигналов из `story_labels` per-axis (GW-TAX-01) вместо/поверх `infer_signals_from_canonical` | [`profile/enrichment.py`](../../../../src/core/profile/enrichment.py), [`cluster_orchestrator.py`](../../../../src/core/application/cluster_orchestrator.py) |
| T04 | Per-lens `min_size`: конфиг `CLUSTER_MIN_SIZE_BY_LENS` (composite-primary=8, богатые оси ниже) + honor в `_resolve_min_size_guard`/promotion-gate; глобальный `CLUSTER_MIN_SIZE` не понижать | [`config/schema.py`](../../../../src/core/config/schema.py), [`cluster_orchestrator.py`](../../../../src/core/application/cluster_orchestrator.py) |
| T05 | Пересчёт `expected-board-fill-matrix` (SEED-02) под composite+новые оси; тесты плотности кластеров (v0_2) | SEED-02 T04 matrix |
| T06 | Acceptance gate: cluster-тесты + full offline suite green; демо-доска (v0_2) **не пустеет** после composite-primary | `tests/test_gw_tax_02_*` |

## Acceptance Criteria
- [ ] Primary issue-ключ = composite `civic_domain + failure_pattern` (не одна ось); карточки предметнее («сфера: сбой»)
- [ ] Добавлены оси `service_object`, `deep_need`, `ecosystem_signal` (из `story_labels` per-axis) как линзы/фасеты
- [ ] Per-lens `min_size`: composite-primary=8, богатые оси ниже; глобально не понижен
- [ ] Демо-доска (v0_2) не опустела; existing cluster-тесты + full offline suite green

## Границы
- **In scope:** composite-primary, новые оси/линзы, per-lens порог, источник из `story_labels`.
- **Вне scope:** приём/хранение таксономии → [GW-TAX-01](./STORY-GW-TAX-01-taxonomy-persistence-fidelity.md); GPT-контракт → GPT-TAX-01; «параллельные доски-линзы» (D-CLUST-1 отклонено — возможное будущее расширение).
- **Не понижать** `CLUSTER_MIN_SIZE` глобально ради наполнения (D-CLUST-4).

## Швы
- Движок: [`cluster/engine.py`](../../../../src/core/cluster/engine.py) (`cluster_key_for_lens`, `CIVIC_LENSES`, `lens_dimension`), [`cluster/types.py`](../../../../src/core/cluster/types.py) (`ClusterLens`); оркестратор: [`application/cluster_orchestrator.py`](../../../../src/core/application/cluster_orchestrator.py) (primary + `_resolve_min_size_guard`); сигналы: [`profile/enrichment.py`](../../../../src/core/profile/enrichment.py); enum: [`domain/contracts.py` SignalDimension](../../../../src/core/domain/contracts.py#L20); конфиг: [`config/schema.py`](../../../../src/core/config/schema.py) (`CLUSTER_*`); сборка: [`infrastructure/service_factory.py:83`](../../../../src/core/infrastructure/service_factory.py#L83).
