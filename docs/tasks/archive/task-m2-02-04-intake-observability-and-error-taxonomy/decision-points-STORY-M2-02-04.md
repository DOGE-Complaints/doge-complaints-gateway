# Decision Points — STORY-M2-02-04

## DP-01: Taxonomy categories
- Решение: `validation_error`, `domain_error`, `infrastructure_error`, `internal_error`.
- Причина: совместимость с операционной аналитикой и triage.

## DP-02: Logging model
- Решение: structured logging c `trace_id`, `error_type`, `error_code`, `event`.
- Причина: трассируемость intake инцидентов по цепочке.

## DP-03: Telemetry baseline
- Решение: lightweight counters (`accepted`, `rejected`, `failed`) как стартовый слой.
- Причина: demo-ready мониторинг без привязки к конкретному metrics backend.
