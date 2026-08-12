## Task workspace — `task-m2-04-05-t07-tests-civic-lenses-et-ru`

- Story: [`../STORY-M2-04-05-civic-canonical-signal-pipeline.md`](../STORY-M2-04-05-civic-canonical-signal-pipeline.md)
- Decision Ref: REQ-34 §4 (ET/RU + civic-only)

## Task: tests — civic lenses and multilingual canonical signal coverage

### Цель
Закрепить REQ-34 acceptance: clustering и signal extraction работают на ET/RU текстах через `canonical_labels`, без EN keywords в narrative.

### Факты из кода
1. [`tests/test_signal_extraction_canonical.py`](../../../../../../../tests/test_signal_extraction_canonical.py) L66 — still tests `hybrid` mode (must be removed/rewritten after T02).
2. [`tests/test_cluster_active_lenses_runtime_effect.py`](../../../../../../../tests/test_cluster_active_lenses_runtime_effect.py) — parametrizes `CLUSTER_ACTIVE_LENSES`.
3. [`tests/intake_v2_fixtures.py`](../../../../../../../tests/intake_v2_fixtures.py) — v2 payloads with `canonical_labels` for extension.

### Gap / Проблема
No dedicated proof that ET/RU narratives cluster correctly when body language is not English (REQ-34 §4 last AC).

### AC/DoD
- [x] (P0) Test: Estonian narrative text + `canonical_labels` including `roads`, `broken_infrastructure` → civic signals not `unknown` for domain/pattern.
- [x] (P0) Test: Russian narrative (no EN tokens) + canonical labels → same.
- [x] (P0) `test_signal_extraction_canonical` no longer references `signal_source=hybrid|keyword`.
- [x] (P0) `test_cluster_active_lenses_runtime_effect` uses civic lens string from REQ-34 §2.2.
- [x] (P1) Story-level pytest slice documented in STORY gate: `pytest tests/test_signal_extraction_canonical.py tests/test_cluster_active_lenses_runtime_effect.py tests/test_story_cluster_orchestrator.py -q`.

### Где менять код
- [`tests/test_signal_extraction_canonical.py`](../../../../../../../tests/test_signal_extraction_canonical.py)
- [`tests/test_cluster_active_lenses_runtime_effect.py`](../../../../../../../tests/test_cluster_active_lenses_runtime_effect.py)
- [`tests/test_story_cluster_orchestrator.py`](../../../../../../../tests/test_story_cluster_orchestrator.py)
- Optional: `tests/fixtures/canonical_et_ru_stories.py`

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_signal_extraction_canonical.py tests/test_cluster_active_lenses_runtime_effect.py tests/test_story_cluster_orchestrator.py -q --tb=short
```
