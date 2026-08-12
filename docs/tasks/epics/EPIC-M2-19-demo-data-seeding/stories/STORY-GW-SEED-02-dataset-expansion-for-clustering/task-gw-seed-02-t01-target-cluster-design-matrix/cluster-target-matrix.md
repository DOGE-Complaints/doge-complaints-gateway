# Cluster target matrix — STORY-GW-SEED-02 T01

- **Date:** 2026-06-22
- **N (parent AC):** **2** темы с ≥8 историй на кластер
- **Approach:** script-generated variations (`tests/sandbox/generate_dogestonia_canvas_v0_2.py`)

## Открытые вопросы (закрыто)

| Вопрос | Решение |
|--------|---------|
| Сколько issue-карточек для «наполненного» демо? | **2** issue (по одному на целевой кластер) минимум; v0_2 даёт запас 9+9 stories |
| Ручная vs скриптовая генерация? | **Скрипт** с шаблоном v0_1 + вариации текста/локали |

## Code facts (cluster key)

Primary lens `civic_domain_micro` + `CLUSTER_GEO_FILTER=district` ([`engine.py`](../../../../../../../src/core/cluster/engine.py), [`enrichment.py`](../../../../../../../src/core/profile/enrichment.py)):

- `civic_domain` = **первый** label из `canonical_labels`, входящий в `CIVIC_DOMAIN_VOCABULARY`
- Geo bucket = `admin_district` после intake ([`scope.py:94-101`](../../../../../../../src/core/geo/scope.py))
- Promotion `min_stories` = `CLUSTER_MIN_SIZE` (=8) ([`service_factory.py`](../../../../../../../src/core/infrastructure/service_factory.py))

`cluster_metadata.primary_cluster_key` из canvas **игнорируется**.

## Target clusters

| ID | scenario_group | civic_domain | failure_pattern | geographic_district | stories | expected issues |
|----|----------------|--------------|-----------------|---------------------|---------|-----------------|
| C1-waste-kalamaja | environment | `waste` (first in labels) | `maintenance_gap` | Kalamaja | **9** | 1 |
| C2-roads-lasnamae | infrastructure | `roads` (first in labels) | `broken_infrastructure` | Lasnamäe | **9** | 1 |

**Shared label block (C1):** `waste`, `environment`, `safety`, `maintenance_gap`, `recurring_issue`, `residents`

**Shared label block (C2):** `roads`, `safety`, `broken_infrastructure`, `unsafe_condition`, `recurring_issue`, `pedestrians`

**location_query pattern:**

- C1: `yard waste bins, Tallinn, Estonia (kalamaja_waste_cluster_v02)`
- C2: `pothole street, Tallinn, Estonia (lasnamae_roads_cluster_v02)`

## v0_1 baseline (reference only)

| scenario_group | count in v0_1 |
|----------------|---------------|
| infrastructure | 50 |
| environment | 40 |
| digital | 25 |
| conflict | 15 |

Max observed cluster size on hosted v0_1 load: **6** ([`analysis-clustering-seed-data-investigation-2026-06-22.md`](../../../../../../analysis/analysis-clustering-seed-data-investigation-2026-06-22.md)) — insufficient for `CLUSTER_MIN_SIZE=8`.

## T02 deliverable

- File: `tests/sandbox/dogestonia_simulation_canvas_v0_2.json`
- **18** scenarios (9+9), `simulation_id` prefix `DOGE-EST-V02-`
- v0_1 **не изменяется**
