# task-gw-es-03-t02-di-factory-api-deps

## Meta
- **Story:** [STORY-GW-ES-03](../STORY-GW-ES-03-public-emerging-l2-read.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000060
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-10T12:06:12Z

## Purpose
Провести `EmergingSignalsService` через factory + `ApiDependencies` без cabinet/intake repository dig.

## Code Facts
- Etalon — [`get_network_pulse_service`](../../../../../../../../src/core/infrastructure/service_factory.py) (`:157`)
- Factory already has `story_label_repository` (`:67`), `issue_story_link_store` (`:65`)
- `ApiDependencies` / `build_api_dependencies` — [`dependencies.py`](../../../../../../../../src/core/api/dependencies.py)
- Anti-pattern — cabinet dig via intake in handlers — **do not copy**

## Acceptance / DoD
- [ ] Traces AC: Service on `ApiDependencies` / factory — not cabinet dig
- [ ] `DefaultServiceFactory.get_emerging_signals_service()` builds from explicit deps
- [ ] `ApiDependencies.emerging_signals_service` wired in `build_api_dependencies()`
- [ ] Existing tests constructing `ApiDependencies` updated if needed
- [ ] BULLRUN phases complete
- [ ] `acceptance-verification-gw-es-03-t02.md` signed (Date post P3 verify only)

## Where to change
- [`service_factory.py`](../../../../../../../../src/core/infrastructure/service_factory.py)
- [`dependencies.py`](../../../../../../../../src/core/api/dependencies.py)
- Fixture kwargs in tests that build `ApiDependencies` manually

## Out of scope
- Handler/route (T03); service algorithm (T01)

## Verification commands
```bash
rg -n 'emerging_signals_service|get_emerging_signals_service' doge-complaints-gateway/src/core/
```
