# task-gw-ssr-22-t00-fail-mode-decision

## Task: decision — Boot ConfigError vs intake 4xx (T00)

## Meta
- **Story:** [STORY-GW-SSR-22](../STORY-GW-SSR-22-civic-geo-gate-hardening.md)
- **Type:** analyze
- **Status:** 🔵 Done · P4 PASS 2026-08-30T20:13:31Z
- **Package:** pkg-000079
- **Skill declared:** python-pro
- **Depends on:** SSR-20 Done (G20); G21 PASS
- **Scaffolded:** 2026-08-30T20:01:08Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-22-civic-geo-gate-hardening.md` T00

## Purpose
**Locked (P3):** intake 4xx — `IntakeValidationError("geo unavailable")`. Не boot ConfigError. Не invent dual-source. Не полный `geo_intake` (→23).

## Code Facts
- **As-of-Done:** scope + `geo_service is None` → `IntakeValidationError("geo unavailable")` — [`handlers.py:258–260`](../../../../../../../src/core/api/handlers.py)
- Intake `geo_service: GeoService | None = None` — [`services.py:100`](../../../../../../../src/core/application/services.py)
- Factory always `geo_service: GeoService` — [`service_factory.py:64`](../../../../../../../src/core/infrastructure/service_factory.py)
- D-SSR-10 — [`INDEX.md:53`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Historical (pre-SSR-22):** scope + query then `if geo_service is not None` (skip) — [`handlers.py:254–268`](../../../../../../../src/core/api/handlers.py) pre-P3

## Acceptance / DoD
- [x] Один fail-mode выбран и записан в pipeline §Target / AC + T01/T02 README
- [x] Не dual-source env+pack; не invent `geo_intake` modes (→23)
- [x] T02 = implement only if boot; else N/A with reason
- [x] BULLRUN phases complete

## Where to change
- This README + pipeline story AC (P3 lock). No product code in P1.

## Out of scope
- Product runtime this task except documenting the lock. Full `geo_detail` (→23).
- Overlay bans (every task):
  - Remove silent skip when `geo_scope` active + `geo_service is None`.
  - **No full `geo_detail` / `geo_intake` parse** (→23). No invent HTTP filter.
  - **No ClusterLens add/remove.** Enum stays 10 (`types.py:10–22`).
  - **Нет `GET /schema-active`.** Нет IDX. Нет GPT UI.
  - **No global require-geo.** Optional / no-`geo_scope` stays geo-agnostic (REQ-35).
  - **Нет SSR-06/07/12.** Не reopen 01–21. Не стартовать 23…25 в этом pkg.
  - Stay `semantic-schema-runtime`. Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.

## Verification commands
```bash
rg -n "geo_service is None|geo_service is not None" doge-complaints-gateway/src/core/api/handlers.py
```
