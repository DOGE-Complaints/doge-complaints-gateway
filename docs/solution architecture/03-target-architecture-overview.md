# 03. Целевая архитектура (Demo baseline)

## High-level схема

```mermaid
graph TD
    GPT["GPT Intake Output"] --> API["API & Contract Layer"]
    API --> ORCH["Story Registry Orchestrator"]
    ORCH --> STORE["Story Store"]
    ORCH --> INTEL["Story Intelligence Engine"]
    INTEL --> CLUSTER["Cluster View Engine"]
    CLUSTER --> PROMO["Issue Promotion Engine"]
    PROMO --> PROJ["SPA Projection Engine"]
    PROMO --> EVID["Evidence Pack Engine"]
    ORCH --> GEO["Geo Intelligence Module"]

    STORE --> DB[("PostgreSQL/Supabase")]
    INTEL --> DB
    CLUSTER --> DB
    PROJ --> DB
    EVID --> DB
    GEO --> DB

    PROJ --> SPA["Existing SPA Issue Contract"]
    EVID --> PILOT["Pilot Adapters (Wallet/Blockchain)"]
```

## Layering model
- **Presentation/API:** request validation, auth, DTO mapping.
- **Application/Orchestration:** lifecycle-команды и координаторы.
- **Domain:** story/profile/cluster/issue/evidence правила.
- **Infrastructure:** db, external APIs, adapters.

## Design principles
- Story-first, issue-later.
- Dynamic clustering, not static taxonomy.
- Projection as dedicated module (не side-effect кластера).
- Evidence-first traceability by default.
- Adapter-first tokenization readiness.
