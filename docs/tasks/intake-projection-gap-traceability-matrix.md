# Intake/Projection Gap Traceability Matrix

## Назначение

Единая матрица трассировки:

- `gap_id -> owner task -> run summary -> closure state`.

SSOT-источник gap-ов: `docs/runtime-docs/issue-intake-and-spa-projection-audit.md`.

## Матрица

| gap_id | Gap summary | Owner task | Task status | Run summary evidence | Closure state | Notes |
|---|---|---|---|---|---|---|
| GAP-IP-001 | Нет `POST /intake/stories` в runtime | `TASK-INTAKE-HTTP-01` | Todo | — | Planned | Demo-critical intake boundary |
| GAP-IP-002 | Нет HTTP create issue endpoint | `TASK-ISSUE-CREATE-HTTP-01` | Todo | — | Planned | Core product use-case |
| GAP-IP-003 | Нет bridge `Story/Promotion -> ProjectionInput` | `TASK-STORY-TO-PROJECTION-01` | Todo | — | Planned | Contract adapter before projection |
| GAP-IP-004 | Нет единой policy derivation `status/type/labels/i18n` | `TASK-SPA-PROJECTION-DATA-01` | Todo | — | Planned | Deterministic SPA contract |
| GAP-IP-005 | Нет e2e pipeline contract tests | `TASK-E2E-CONTRACT-01` | Todo | — | Planned | Cross-stage regression safety |

## Статусы closure state

- `Planned` — есть owner task, реализация не начата.
- `In Progress` — owner task в работе.
- `Closed` — owner task `Done (Committed)` + run-summary evidence.
- `Deferred` — есть явное обоснование и новая целевая дата/задача.

## Правило обновления

Матрица обновляется в той же итерации, когда меняется:

1. статус owner task в `bullrun-launch-index.md`;
2. факт появления нового `run-summary-*`;
3. состояние gap (planned/in progress/closed/deferred).
