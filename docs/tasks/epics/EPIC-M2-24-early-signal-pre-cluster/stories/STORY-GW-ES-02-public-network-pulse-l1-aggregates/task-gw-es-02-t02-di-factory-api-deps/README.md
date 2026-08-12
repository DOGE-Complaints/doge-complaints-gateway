# task-gw-es-02-t02-di-factory-api-deps

## Meta
- **Story:** [STORY-GW-ES-02](../STORY-GW-ES-02-public-network-pulse-l1-aggregates.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000059
- **Skill declared:** python-pro
- **Depends on:** T01 (`NetworkPulseService` type exists)
- **decision_ref:** backlog ES-02 §B — без cabinet-hack

## Purpose
Провести `NetworkPulseService` через `DefaultServiceFactory` + поле `ApiDependencies.network_pulse_service` + `build_api_dependencies()`. Handler later must use deps field — **не** dig `story_intake_service.repository`.

## Code Facts
- `ApiDependencies` today — no pulse — [`dependencies.py:20-44`](../../../../../../../../src/core/api/dependencies.py)
- Labels on factory — [`service_factory.py:66`](../../../../../../../../src/core/infrastructure/service_factory.py) `story_label_repository`
- Providers — [`providers.py`](../../../../../../../../src/core/infrastructure/providers.py)
- Anti-pattern (do not copy) — cabinet dig [`handlers.py:772-776`](../../../../../../../../src/core/api/handlers.py)

## Acceptance / DoD
- [x] Traces parent AC: wired via `ApiDependencies` / factory — **not** via `story_intake_service.repository` dig
- [x] `get_network_pulse_service()` (or equiv) builds from `story_repository` + `story_label_repository`
- [x] `network_pulse_service` on `ApiDependencies`; set in `build_api_dependencies()`
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-es-02-t02.md` signed (Date post P3 verify only)

## Where to change
- [`service_factory.py`](../../../../../../../../src/core/infrastructure/service_factory.py)
- [`dependencies.py`](../../../../../../../../src/core/api/dependencies.py)
- [`providers.py`](../../../../../../../../src/core/infrastructure/providers.py) if factory exposure needs it

## Out of scope
- HTTP route (T03); service implementation details beyond factory wiring (T01)

## Verification commands
```bash
rg -n 'network_pulse_service|get_network_pulse_service' doge-complaints-gateway/src/core/api/dependencies.py doge-complaints-gateway/src/core/infrastructure/service_factory.py
rg -n 'story_intake_service.repository' doge-complaints-gateway/src/core/api/handlers.py | head
```
