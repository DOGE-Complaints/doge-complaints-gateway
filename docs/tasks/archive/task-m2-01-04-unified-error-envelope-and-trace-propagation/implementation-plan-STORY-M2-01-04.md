# Implementation Plan — STORY-M2-01-04

## Phase 1 — Envelope and mapper
- Добавить dataclass контракт success/error envelope.
- Реализовать `ensure_trace_id()` и error mapping.

## Phase 2 — Boundary handler and logging
- Добавить boundary handler `handle_health()` с unified envelope.
- Добавить logging helper с `trace_id`.

## Phase 3 — Contract tests and verification
- Добавить tests для error shape/mapping.
- Добавить tests для trace propagation (payload + logs).
