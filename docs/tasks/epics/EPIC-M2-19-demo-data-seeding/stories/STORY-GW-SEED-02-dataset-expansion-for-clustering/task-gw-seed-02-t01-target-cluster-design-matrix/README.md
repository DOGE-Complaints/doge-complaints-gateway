# task-gw-seed-02-t01

## Meta
- **Story:** [STORY-GW-SEED-02](../STORY-GW-SEED-02-dataset-expansion-for-clustering.md)
- **Type:** analyze
- **Status:** 🟢 Done
- **Package:** pkg-000037
- **Skill declared:** python-pro

## Purpose
Определить целевые кластеры: какие темы × сколько issue хотим на доске; в каких `scenario_group`; согласовать **N** для parent AC «≥N тем с ≥8 историй»; закрыть открытые вопросы backlog (число карточек, ручная vs скриптовая генерация).

## Code Facts
- Cluster key (primary lens) — [`engine.py:70-89`](../../../../../../../src/core/cluster/engine.py#L70-L89) `cluster_key_for_lens`
- Signal inference from labels — [`enrichment.py:37-78`](../../../../../../../src/core/profile/enrichment.py#L37-L78) `infer_signals_from_canonical`
- Civic domain vocab — [`vocabulary.py:5-20`](../../../../../../../src/core/cluster/vocabulary.py#L5-L20)
- Batch min ready — [`cluster_orchestrator.py:159-168`](../../../../../../../src/core/application/cluster_orchestrator.py#L159-L168)
- Promotion `min_stories` = `CLUSTER_MIN_SIZE` — [`service_factory.py:97-100`](../../../../../../../src/core/infrastructure/service_factory.py#L97-L100)
- Canvas baseline — [`dogestonia_simulation_canvas_v0_1.json`](../../../../../../../tests/sandbox/dogestonia_simulation_canvas_v0_1.json)
- Clustering audit — [`analysis-clustering-seed-data-investigation-2026-06-22.md`](../../../../../../analysis/analysis-clustering-seed-data-investigation-2026-06-22.md)

## Acceptance / DoD
- Traces parent AC: N согласовано для «≥N тем с ≥8 историй с общими метками»
- Artifact [`cluster-target-matrix.md`](./cluster-target-matrix.md): темы × `scenario_group` × `(civic_domain, geographic_district, failure_pattern)` × target story count ≥8 × expected issue count
- Открытые вопросы backlog закрыты в matrix (demo issue count; manual vs script approach)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- Task artifact: `cluster-target-matrix.md` in this folder
- Optional offline script/notebook under `tests/` (read-only analysis of v0_1 label distribution) — no `src/core/`

## Out of scope
- Creating `dogestonia_simulation_canvas_v0_2.json` (T02)
- Runtime clustering verify (T03)
- Application code changes

## Verification commands
```bash
# Offline: inspect v0_1 label distribution (no DB)
cd doge-complaints-gateway && python3 -c "
import json
from pathlib import Path
from collections import Counter
p = Path('tests/sandbox/dogestonia_simulation_canvas_v0_1.json')
data = json.loads(p.read_text())
groups = Counter(s.get('scenario_group') for s in data)
print('scenario_groups', dict(groups), 'total', len(data))
"
```
