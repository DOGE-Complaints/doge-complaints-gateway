# Карта доказательств (claim-to-source)

## Назначение

Этот документ фиксирует источники фактов для runtime-документации.  
Каждое существенное утверждение в `docs/runtime-docs/*` должно ссылаться на строки поведения в коде или тестах.

## Архитектура и DI

- **Composition root проходит через bootstrap -> api dependencies -> providers -> service factory**
  - `src/core/bootstrap.py`
  - `src/core/api/dependencies.py`
  - `src/core/infrastructure/providers.py`
  - `src/core/infrastructure/service_factory.py`
- **Layer guardrails существуют как тестовые ограничения**
  - `tests/test_layer_guardrails.py`
  - `tests/test_bootstrap_smoke.py`
  - `tests/test_di_service_factory.py`

## API boundary и envelopes

- **Текущий API реализован handler-функциями, а не web-router файлом**
  - `src/core/api/handlers.py`
  - `src/core/api/__init__.py`
- **Единый envelope-контракт success/error + trace**
  - `src/core/api/envelope.py`
  - `tests/test_error_envelope_contract.py`
  - `tests/test_trace_propagation.py`
- **Набор ops-handler операций (health, readiness, protected, metrics)**
  - `src/core/api/handlers.py`
  - `tests/test_api_security_and_ops.py`

## Security и env

- **Service-to-service auth: Bearer и X-Service-Token**
  - `src/core/api/security.py`
  - `src/core/api/handlers.py`
  - `tests/test_api_security_and_ops.py`
- **Auth disabled при отсутствии SERVICE_API_TOKEN**
  - `src/core/api/security.py::build_service_auth_from_env`
  - `tests/test_api_security_and_ops.py::test_build_service_auth_from_env`
- **Конфигурационный контракт runtime**
  - `src/core/config/schema.py`
  - `tests/test_config_loading.py`

## Intake / profile / lifecycle

- **Intake request schema и парсинг**
  - `src/core/intake/contracts.py`
  - `tests/test_story_intake_contract.py`
- **Story lifecycle переходы**
  - `src/core/application/services.py::StoryIntakeService.advance_story_readiness`
  - `tests/test_story_repository_lifecycle.py`
- **Idempotency на intake**
  - `src/core/application/services.py::StoryIntakeService.create_story`
  - `tests/test_story_intake_idempotency.py`
- **Signal profile quality/enrichment**
  - `src/core/profile/schema.py`
  - `src/core/profile/enrichment.py`
  - `src/core/profile/validation.py`
  - `tests/test_signal_profile_schema.py`
  - `tests/test_signal_profile_quality_validation.py`
  - `tests/test_signal_profile_enrichment_and_versioning.py`

## Cluster / promotion / projection

- **Clustering engine (canonical lenses, readiness scoring, memberships)**
  - `src/core/cluster/engine.py`
  - `tests/test_clustering_engine.py`
- **Promotion gates и lifecycle candidate**
  - `src/core/promotion/gates.py`
  - `src/core/promotion/service.py`
  - `src/core/promotion/types.py`
  - `tests/test_issue_promotion_service.py`
- **Projection contract и валидация tx placeholders**
  - `src/core/projection/input.py`
  - `src/core/projection/mapper.py`
  - `src/core/projection/validation.py`
  - `src/core/projection/dto.py`
  - `tests/test_spa_projection.py`

## Evidence, geo, adapters

- **Evidence pack lineage, redaction, export metadata**
  - `src/core/evidence/service.py`
  - `src/core/evidence/redaction.py`
  - `src/core/evidence/repositories.py`
  - `tests/test_evidence_pack.py`
- **Geo cache-first resolve + fallback/retry**
  - `src/core/geo/service.py`
  - `src/core/geo/chain.py`
  - `src/core/geo/providers.py`
  - `src/core/geo/metrics.py`
  - `tests/test_geo_intelligence.py`
- **Adapters пока stub/demo-only для demo и pilot**
  - `src/core/adapters/protocols.py`
  - `src/core/adapters/demo.py`
  - `src/core/adapters/registry.py`
  - `tests/test_adapters_demo_pilot.py`

## DB and operations boundaries

- **В runtime нет real DB integration**
  - `src/core/infrastructure/repositories.py`
  - `src/core/evidence/repositories.py`
  - `src/core/promotion/repositories.py`
  - `src/core/config/schema.py`
- **`example.env` содержит Supabase/DB переменные как шаблон, но runtime ядро их не читает напрямую**
  - `example.env`
  - `src/core/config/schema.py`

## Правило использования карты

Если в `runtime-docs` появляется новое нетривиальное утверждение, перед merge нужно:

1. Добавить соответствующую ссылку на код/тест в эту карту.
2. Проверить, что ссылка действительно доказывает утверждение (а не просто упоминает термин).
3. Обновить `cross-check-and-quality-gates.md`.
