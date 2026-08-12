# Implementation Plan — STORY-M2-01-03

## Phase 1 — Config model and validation
- Добавить `core.config` package.
- Реализовать schema/env parsing/errors.

## Phase 2 — Profiles and feature flags
- Добавить `DeploymentProfile`.
- Ввести profile defaults и env overrides для flags.

## Phase 3 — Tests and verification
- Написать позитивные/негативные тесты config loading.
- Прогнать `pytest` и зафиксировать acceptance.
