# 01. Scope и ограничения (Demo)

## In Scope
- Story intake как первичный слой (без forced collapse в issue).
- Story intelligence (профиль сигналов).
- Dynamic cluster views (минимальные линзы MVP).
- Distinct issue promotion (issue-candidate -> issue).
- SPA-compatible projection (zero-change).
- Evidence pack и полная traceability.
- Geo enrichment как отдельный модуль.

## Out of Scope (Demo)
- Реальный on-chain submit/signing.
- Реальный wallet push transport.
- Финальные гос-интеграции.

## Pilot-ready, но выключено в Demo
- интерфейсы для wallet-sign flow;
- state machine upload/sign/callback;
- tx broadcaster adapter.

## Нефункциональные ограничения
- PII-min by default.
- Backward compatibility с текущим SPA-контрактом.
- Обязательная explainability кластеризации и issue-промоции.
- Миграционная совместимость с legacy данными.
