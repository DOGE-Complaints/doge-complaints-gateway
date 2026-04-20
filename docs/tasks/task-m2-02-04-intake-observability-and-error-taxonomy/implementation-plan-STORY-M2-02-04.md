# Implementation Plan — STORY-M2-02-04

1. Добавить `core.intake.observability` модуль.
2. Экспортировать observability API из `core.intake`.
3. Добавить unit tests:
   - taxonomy classification;
   - payload shape (`trace_id`);
   - structured logging fields;
   - telemetry counters.
4. Прогнать полный `pytest`.
