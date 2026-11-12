# task-gw-ssr-22-t01-handlers-no-silent-skip

## Task: implement — убрать silent skip; fail явно (T01)

## Meta
- **Story:** [STORY-GW-SSR-22](../STORY-GW-SSR-22-civic-geo-gate-hardening.md)
- **Type:** implement
- **Status:** 🔵 Done · P4 PASS 2026-08-30T20:13:31Z
- **Package:** pkg-000079
- **Skill declared:** python-pro
- **Depends on:** T00 lock
- **Scaffolded:** 2026-08-30T20:01:08Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-22-civic-geo-gate-hardening.md` T01

## Purpose
При активном pack `geo_scope` не silent-accept, если `geo_service is None`. Fail по T00 (intake 4xx и/или согласованный query-required для scope check). Не новый HTTP path. Не полный `geo_detail`.

## Code Facts
- `geo_scope` from pack civic — [`handlers.py:254–257`](../../../../../../../src/core/api/handlers.py)
- **As-of-Done:** scope + `geo_service is None` → `IntakeValidationError("geo unavailable")` — [`handlers.py:258–260`](../../../../../../../src/core/api/handlers.py)
- **Historical (pre-SSR-22):** Silent skip when service None — [`handlers.py:260–268`](../../../../../../../src/core/api/handlers.py) pre-P3
- 422 `GeoScopeMismatchError` already — [`handlers.py:324–337`](../../../../../../../src/core/api/handlers.py)

## Acceptance / DoD
- [x] `geo_scope` active + `geo_service is None` → не 202 / не silent accept
- [x] Нет `geo_scope` → geo-agnostic как сейчас (REQ-35)
- [x] Нет нового HTTP path; нет `GET /schema-active`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/api/handlers.py` `:254–268`

## Out of scope
- Новый HTTP path. Полный `geo_detail` parse (→23). Удалить GeoService.
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
