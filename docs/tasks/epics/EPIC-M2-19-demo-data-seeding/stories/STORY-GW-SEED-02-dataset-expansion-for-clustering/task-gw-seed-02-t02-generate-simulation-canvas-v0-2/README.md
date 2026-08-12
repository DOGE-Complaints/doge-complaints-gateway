# task-gw-seed-02-t02

## Meta
- **Story:** [STORY-GW-SEED-02](../STORY-GW-SEED-02-dataset-expansion-for-clustering.md)
- **Type:** data
- **Status:** 🟢 Done
- **Package:** pkg-000037
- **Skill declared:** python-pro
- **Depends on:** T01 (`cluster-target-matrix.md`)

## Purpose
Сгенерировать расширенный canvas `dogestonia_simulation_canvas_v0_2.json` с ≥8 историй на целевой кластер; сохранить совместимость со схемой загрузчика (`normalized_issue_payload.canonical_payload`).

## Code Facts
- Loader reads `canonical_payload` — [`simulation_runner.py:55`](../../../../../../../tests/simulation_runner.py#L55)
- Canvas path env — [`simulation_runner.py:163`](../../../../../../../tests/simulation_runner.py#L163) `SIMULATION_CANVAS_PATH`
- v0_1 schema reference — [`dogestonia_simulation_canvas_v0_1.json`](../../../../../../../tests/sandbox/dogestonia_simulation_canvas_v0_1.json) (first element structure)
- Target matrix — [`../task-gw-seed-02-t01-target-cluster-design-matrix/cluster-target-matrix.md`](../task-gw-seed-02-t01-target-cluster-design-matrix/cluster-target-matrix.md)

## Acceptance / DoD
- Traces parent AC: расширенный canvas создан отдельным файлом; v0_1 не изменён
- Traces parent AC: по ≥N темам (из T01) набирается ≥8 историй с общими метками на кластер
- File exists: [`tests/sandbox/dogestonia_simulation_canvas_v0_2.json`](../../../../../../../tests/sandbox/dogestonia_simulation_canvas_v0_2.json)
- `git diff tests/sandbox/dogestonia_simulation_canvas_v0_1.json` empty
- Each scenario has `normalized_issue_payload.canonical_payload` compatible with loader
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- **Create:** `tests/sandbox/dogestonia_simulation_canvas_v0_2.json`
- Optional: generator script under `tests/` or `scripts/` (data-only)
- **Do not modify:** `tests/sandbox/dogestonia_simulation_canvas_v0_1.json`

## Out of scope
- `src/core/` application code
- Lowering `CLUSTER_MIN_SIZE`
- Full hosted load (T03)

## Verification commands
```bash
cd doge-complaints-gateway
test -f tests/sandbox/dogestonia_simulation_canvas_v0_2.json
git diff --exit-code tests/sandbox/dogestonia_simulation_canvas_v0_1.json
python3 -c "
import json
from pathlib import Path
p = Path('tests/sandbox/dogestonia_simulation_canvas_v0_2.json')
data = json.loads(p.read_text())
assert isinstance(data, list) and len(data) > 0
cp = data[0]['normalized_issue_payload']['canonical_payload']
assert 'type' in cp and 'labels' in cp
print('entries', len(data))
"
```
