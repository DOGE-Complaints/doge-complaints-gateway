## Task workspace — `task-m2-04-05-t01-remove-legacy-cluster-lenses`

- Story: [`../STORY-M2-04-05-civic-canonical-signal-pipeline.md`](../STORY-M2-04-05-civic-canonical-signal-pipeline.md)
- Decision Ref: [`../../../../../../requirements/34-civic-clustering-canonical-signal-pipeline.md`](../../../../../../requirements/34-civic-clustering-canonical-signal-pipeline.md) §2.1; gap-interview G-04.1

## Task: refactor — remove legacy cluster lenses from enum and engine

### Цель
Удалить шесть legacy линз (`topic_micro`, `need_local`, …) из `ClusterLens`, `LEGACY_LENSES` и допустимых значений конфига, чтобы keyword-оси не использовались в runtime.

### Факты из кода
1. [`src/core/cluster/types.py`](../../../../../../../src/core/cluster/types.py) L11–16 — legacy six + civic six в одном enum.
2. [`src/core/cluster/engine.py`](../../../../../../../src/core/cluster/engine.py) L19–28 — `LEGACY_LENSES` и `CANONICAL_LENSES = LEGACY_LENSES` (deprecated alias).
3. [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py) `_all_cluster_lens_ids()` — включает все 12 id.

### Gap / Проблема
Legacy lenses используют keyword signals (`"road" in text`) — 0% на ET/RU (REQ-34 §1, G-04).

### AC/DoD
- [x] (P0) `ClusterLens` содержит только civic six: `civic_domain_micro`, `failure_pattern_micro`, `civic_weight_systemic`, `desired_outcome_local`, `affected_group_local`, `geographic_district_micro`.
- [x] (P0) Удалены `LEGACY_LENSES`, `CANONICAL_LENSES` alias; `_SYSTEMIC_LENSES` / `_LOCAL_LENSES` / `_MICRO_LENSES` не ссылаются на удалённые enum members.
- [x] (P0) `_all_cluster_lens_ids()` и тесты config не принимают legacy lens strings.
- [x] (P1) `cluster/__init__.py` exports обновлены.

### Где менять код
- [`src/core/cluster/types.py`](../../../../../../../src/core/cluster/types.py)
- [`src/core/cluster/engine.py`](../../../../../../../src/core/cluster/engine.py)
- [`src/core/cluster/__init__.py`](../../../../../../../src/core/cluster/__init__.py)
- [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py)
- Тесты, импортирующие legacy `ClusterLens.*` или env с legacy lenses

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_config_loading.py tests/test_cluster_active_lenses_runtime_effect.py -q --tb=short
```
