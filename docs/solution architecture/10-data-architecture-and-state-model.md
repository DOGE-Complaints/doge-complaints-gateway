# 10. Data Architecture & State Model

## Logical bounded contexts
- Story Context
- Intelligence Context
- Cluster Context
- Issue Projection Context
- Evidence Context
- Geo Context

## Core state machines

### Story lifecycle
`accepted -> profiled -> cluster_eligible -> issue_linked -> archived`

### Cluster lifecycle
`analytics -> candidate -> promoted | reframed | split | merged`

### Issue lifecycle (internal)
`projected_new -> reviewed -> published_ready`

## Persistence principles
- migration-first schema governance;
- immutable core + mutable derived layers;
- explicit version columns for profile/lens/projection policies;
- idempotency keys for command handlers.

## Read models
- board read model (SPA fields only);
- issue details read model (enriched but contract-safe);
- evidence drill-down read model (internal).
