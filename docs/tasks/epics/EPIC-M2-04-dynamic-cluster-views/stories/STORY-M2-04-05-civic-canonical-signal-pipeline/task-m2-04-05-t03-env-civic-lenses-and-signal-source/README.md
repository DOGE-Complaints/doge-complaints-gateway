## Task workspace — `task-m2-04-05-t03-env-civic-lenses-and-signal-source`

- Story: [`../STORY-M2-04-05-civic-canonical-signal-pipeline.md`](../STORY-M2-04-05-civic-canonical-signal-pipeline.md)
- Decision Ref: REQ-34 §2.2, §2.3; gap-interview G-04.2, D-01

## Task: implement — civic CLUSTER_ACTIVE_LENSES and canonical-only signal source config

### Цель
Задать в `example.env` и schema defaults шесть civic линз; ограничить `CLUSTER_SIGNAL_SOURCE` только значением `canonical`; выровнять `CLUSTER_PRIMARY_LENS` с активным набором.

### Факты из кода
1. [`example.env`](../../../../../../../example.env) L53 — legacy six lenses active.
2. [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py) L173–176 — `CLUSTER_SIGNAL_SOURCE` description lists `canonical | narrative | hybrid`.
3. L329–336 — `_parse_cluster_signal_source` allows `narrative`, `hybrid`.

### Gap / Проблема
Civic lenses существуют в enum, но не активированы в operator env (G-04.2).

### AC/DoD
- [x] (P0) `example.env`: `CLUSTER_ACTIVE_LENSES=civic_domain_micro,failure_pattern_micro,civic_weight_systemic,desired_outcome_local,affected_group_local,geographic_district_micro`.
- [x] (P0) `CLUSTER_PRIMARY_LENS` ∈ active set (default `civic_domain_micro`).
- [x] (P0) `CLUSTER_SIGNAL_SOURCE=canonical` only; invalid `keyword`/`hybrid`/`narrative` → `ConfigError`.
- [x] (P1) Default in `ENV_SCHEMA` for `CLUSTER_ACTIVE_LENSES` matches civic six (if schema defaults still list legacy — update).
- [x] (P1) `tests/test_config_loading.py` updated for new allowed values.

### Где менять код
- [`example.env`](../../../../../../../example.env)
- [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py)
- [`tests/test_config_loading.py`](../../../../../../../tests/test_config_loading.py)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_config_loading.py -q --tb=short
```
