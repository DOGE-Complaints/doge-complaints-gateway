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
- idempotency keys for command handlers;
- **авторство:** при приёме intake сохранять связь story с внешним субъектом (`submitter.external_user_id`, `identity_issuer`) из OAuth-потока GPT/IdP — opaque string, без обязательной нормализации формата; поле не теряется на пути к evidence (см. `requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md` §5).

## Read models
- board read model (SPA fields only);
- issue details read model (enriched but contract-safe);
- evidence drill-down read model (internal).

## Automation / scheduled execution (post-demo)

Фоновые и cron-задачи **не** являются отдельным источником доменной истины: они должны вызывать те же application use-case, что и API. Детали — `16-automation-orchestration-and-scheduled-jobs.md` и требования `requirements/20-post-demo-orchestration-and-scheduled-jobs.md`.
