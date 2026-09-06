# DOGEstonia — Complaints Gateway

**API Gateway & Story Intelligence Layer for DOGEstonia**

DOGEstonia Complaints Gateway turns individual civic stories into structured, traceable collective signals.

The service sits between citizen-facing interfaces, DOGEstonia identity services, persistent storage, and downstream civic applications. It preserves each submitted story as an independent source record while building higher-level representations such as dynamic clusters, emerging signals, network-level indicators, and distinct civic issues.

> **Core principle:** stories remain first-class records. Aggregation creates additional views of reality rather than replacing the original human narratives.

---

## What this service does

The gateway currently provides the operational Web2 core for the DOGEstonia story-to-issue pipeline.

It supports:

* story draft creation and submission;
* authenticated access to a user's drafts and story activity;
* identity introspection and verification gates;
* structured civic story persistence;
* configurable multi-lens story clustering;
* cluster readiness and promotion logic;
* creation and retrieval of distinct civic issues;
* traceability between stories, clusters, and issues;
* geographic scoping and filtering;
* emerging-signal discovery;
* network pulse aggregation;
* node-specific schema configuration;
* runtime health, readiness, metrics, and diagnostics;
* in-memory, SQLite, and Supabase/PostgreSQL persistence.

---

## Why story-first?

Traditional complaint systems tend to turn a person's experience directly into a ticket.

DOGEstonia uses a different model:

```text
Citizen experience
        │
        ▼
      Story
        │
        ├── remains an independent record
        │
        ▼
Structured civic signals
        │
        ▼
Dynamic cluster views
        │
        ▼
Emerging collective pattern
        │
        ▼
Distinct Issue
        │
        ▼
Downstream civic workflows
```

A Story is not discarded when an Issue is created.

The system keeps the original narrative and maintains lineage between derived collective objects and their contributing stories. This makes it possible to aggregate recurring experiences without losing the human context behind them.

---

## Current capabilities

### Story drafts

The API supports a draft workflow before a civic story becomes part of the operational dataset.

Available operations include:

* create a story draft;
* retrieve the current user's active draft;
* retrieve a specific draft;
* submit a completed draft;
* retrieve the authenticated user's story activity.

Draft reads require an active user session.

Final submission additionally passes the DOGEstonia verification gate.

---

### Identity and verification

The gateway integrates with the DOGEstonia identity boundary rather than treating authentication as application-local state.

For protected user operations it:

1. extracts the browser Bearer token;
2. calls the configured identity `/me` service;
3. validates that the user session is active;
4. applies the verification gate where required.

Story submission currently requires the verification condition used by the identity service, including the `phone_verified` gate.

The gateway also supports service-to-service authentication for protected backend operations.

---

## Story intelligence

The service contains a configurable clustering runtime that groups stories across multiple analytical lenses.

Current configuration supports concepts such as:

* a primary clustering lens;
* multiple active lenses;
* per-lens minimum cluster sizes;
* readiness thresholds;
* geographic grouping;
* node geographic scope;
* canonical signal sources;
* deterministic tie-breaking;
* type-resolution rules.

The exact clustering behaviour is configurable per DOGEstonia node through its schema.

Example configuration:

```env
CLUSTER_MIN_SIZE=8
CLUSTER_READINESS_THRESHOLD=60

CLUSTER_ACTIVE_LENSES=composite_primary_micro,civic_domain_micro,failure_pattern_micro,civic_weight_systemic,desired_outcome_local,affected_group_local,geographic_district_micro,service_object_micro,deep_need_local,ecosystem_signal_systemic

CLUSTER_PRIMARY_LENS=composite_primary_micro
CLUSTER_SIGNAL_SOURCE=canonical
CLUSTER_GEO_FILTER=country
CLUSTER_TIE_BREAKER=alpha
CLUSTER_TYPE_RESOLUTION=canonical_priority
```

A background cluster orchestration job can also be enabled to periodically evaluate the current story corpus.

---

## Node-aware configuration

DOGEstonia is designed around configurable nodes rather than one globally hard-coded civic taxonomy.

The gateway loads a node schema using:

```env
NODE_SCHEMA_ID=...
NODE_SCHEMA_VERSION=...
```

Node configuration can influence the story intelligence runtime, including clustering behaviour and geographic scope.

For example:

```env
CLUSTER_GEO_SCOPE=settlement:tallinn
```

can restrict a node to stories within its configured geographic responsibility.

Stories outside a configured node scope can be rejected during intake rather than silently entering the wrong civic dataset.

---

## Issues

Distinct Issues are higher-level civic objects produced from structured collective patterns or created through the public-content service boundary.

The API supports:

* issue creation;
* issue retrieval by ID;
* issue listing;
* filtering by status;
* filtering by type;
* filtering by labels;
* filtering by institution;
* creation-date filtering;
* geographic filtering.

Geographic filters currently include:

* latitude / longitude bounds;
* district;
* settlement;
* region;
* country;
* postal code.

This allows downstream applications to expose the same underlying civic data at neighbourhood, city, regional, or broader levels.

---

## Network Pulse

```http
GET /node/network-pulse
```

provides a node-level view of the current civic network state.

It is intended for interfaces that need an aggregate signal rather than individual story or issue records.

---

## Emerging Signals

```http
GET /node/emerging-signals
```

exposes collective patterns that are beginning to form before they necessarily become established civic issues.

The endpoint supports a configurable result limit:

```http
GET /node/emerging-signals?top_n=10
```

This creates an intermediate observability layer between isolated citizen stories and mature collective issues.

---

## API overview

### Runtime

| Method | Endpoint            | Purpose                        |
| ------ | ------------------- | ------------------------------ |
| `GET`  | `/health`           | Application health             |
| `GET`  | `/ready`            | Runtime / dependency readiness |
| `GET`  | `/protected/status` | Protected service status       |
| `GET`  | `/metrics`          | Runtime metrics                |

### Stories

| Method | Endpoint                          | Purpose                               |
| ------ | --------------------------------- | ------------------------------------- |
| `POST` | `/story-drafts`                   | Create a story draft                  |
| `GET`  | `/story-drafts/current`           | Get the current user's draft          |
| `GET`  | `/story-drafts/{draft_id}`        | Get a specific draft                  |
| `POST` | `/story-drafts/{draft_id}/submit` | Submit a draft as a story             |
| `GET`  | `/story-activity`                 | Get the current user's story activity |

### Civic intelligence

| Method | Endpoint                 | Purpose                              |
| ------ | ------------------------ | ------------------------------------ |
| `GET`  | `/node/network-pulse`    | Aggregate node signal                |
| `GET`  | `/node/emerging-signals` | Discover emerging collective signals |

### Issues

| Method | Endpoint                  | Purpose              |
| ------ | ------------------------- | -------------------- |
| `GET`  | `/node/issues`            | Search / list issues |
| `GET`  | `/node/issues/{issue_id}` | Retrieve an issue    |
| `POST` | `/node/issues`            | Create an issue      |

### Telemetry

| Method | Endpoint                  | Purpose                                    |
| ------ | ------------------------- | ------------------------------------------ |
| `POST` | `/telemetry/label-misses` | Record taxonomy / translation label misses |

### Demo

| Method | Endpoint          | Purpose                         |
| ------ | ----------------- | ------------------------------- |
| `GET`  | `/demo/auth-page` | Authentication integration demo |

FastAPI also exposes its generated OpenAPI interface when running locally.

---

## Persistence

The runtime supports three storage modes.

### In-memory

```env
DB_BACKEND=in_memory
```

Useful for tests, demos, and isolated development.

Data is not durable.

---

### SQLite

```env
DB_BACKEND=sqlite
DATABASE_URL=sqlite:////absolute/path/to/doge_gateway.db
```

Provides lightweight local SQL persistence for development and end-to-end scenarios.

---

### Supabase / PostgreSQL

```env
DB_BACKEND=supabase

SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_SERVICE_ROLE=<service-role-key>

DATABASE_URL=postgresql://...
```

The Supabase runtime performs readiness checks covering database connectivity and expected storage contracts before treating the persistence layer as ready.

Server-side service credentials must never be exposed to browser clients or committed to the repository.

---

## Architecture

The runtime follows explicit domain and application boundaries rather than placing business logic directly inside HTTP handlers.

```text
┌─────────────────────────────────────┐
│             API Layer               │
│     FastAPI / auth / envelopes      │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│         Application Layer           │
│                                     │
│ Story Intake                        │
│ Cluster Orchestration               │
│ Issue Creation                      │
│ Emerging Signals                    │
│ Network Pulse                       │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│            Domain Layer             │
│                                     │
│ Stories • Drafts • Contracts        │
│ Civic signals • repositories        │
└──────────────────┬──────────────────┘
                   │
          ┌────────┴─────────┐
          ▼                  ▼
┌─────────────────┐  ┌─────────────────┐
│ Cluster Engine  │  │ Infrastructure  │
│ lenses / rules  │  │ DB / identity   │
└─────────────────┘  └─────────────────┘
```

Key source areas:

```text
src/core/
├── api/             # FastAPI routes, security, handlers, metrics
├── application/     # use cases and orchestration
├── cluster/         # clustering engine and vocabulary
├── config/          # runtime and node configuration
├── domain/          # domain contracts and business entities
├── identity/        # DOGEstonia identity integration
├── infrastructure/  # persistence implementations and providers
└── scheduler/       # background clustering orchestration
```

---

## Repository structure

```text
.
├── .github/
│   └── workflows/          # CI and live integration workflows
│
├── demo/
│   └── auth-page/          # identity/auth integration demo
│
├── docs/
│   ├── analysis/           # architecture and implementation analysis
│   ├── requirements/       # product and system requirements
│   └── solution architecture/
│
├── schema-packs/           # node/schema configuration assets
├── scripts/                # operational and smoke scripts
├── src/
│   └── core/               # application runtime
│
├── tests/                  # automated test suite
├── example.env
├── pyproject.toml
├── railpack.json
└── README.md
```

---

## Tech stack

The current runtime is intentionally compact.

* **Python 3.11+**
* **FastAPI**
* **Uvicorn**
* **PostgreSQL / Supabase**
* **SQLite**
* **psycopg**
* **HTTPX**
* **JSON Schema**
* **pytest**
* **pytest-asyncio**

---

## Local development

### 1. Clone the repository

```bash
git clone https://github.com/DOGE-Complaints/doge-complaints-gateway.git
cd doge-complaints-gateway
git checkout dev
```

### 2. Create a virtual environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install the project

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

### 4. Configure the environment

```bash
cp example.env .env
```

For the simplest local runtime, use:

```env
DB_BACKEND=in_memory
```

Do not commit real credentials.

### 5. Start the API

```bash
python -m uvicorn --app-dir src core.api.asgi_app:app \
  --host 127.0.0.1 \
  --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Readiness:

```bash
curl http://127.0.0.1:8000/ready
```

---

## Testing

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run the offline test suite:

```bash
python -m pytest -q -m "not live_integration"
```

Tests requiring a real Supabase project are marked:

```text
live_integration
```

and are intentionally separated from the normal offline CI suite.

---

## CI

GitHub Actions currently separates:

* normal offline test execution;
* live Supabase integration testing.

The offline suite runs on pushes and pull requests using Python 3.11.

---

## Deployment

The repository includes a Railpack configuration.

The production-style ASGI command is:

```bash
python -m uvicorn \
  --app-dir src \
  core.api.asgi_app:app \
  --host 0.0.0.0 \
  --port ${PORT:-8000}
```

Deployment environments should configure persistence, identity integration, service authentication, node schema, and clustering behaviour through environment variables rather than modifying application code.

---

## Observability

The gateway includes several runtime observability mechanisms:

* health checks;
* readiness checks;
* protected runtime status;
* application metrics;
* request trace IDs;
* structured runtime logging;
* startup persistence diagnostics;
* graceful lifecycle logging;
* cluster scheduler lifecycle reporting.

Supplied `x-trace-id` headers are propagated into the API diagnostic envelope; otherwise a trace ID is generated by the gateway.

---

## What is intentionally outside this repository

This service is an operational **Story Intelligence and civic API layer**, not the entire DOGEstonia platform.

The current module does **not** own:

* the conversational AI interview itself;
* the complete DOGEstonia user interface;
* policy or legal rules as normative sources;
* blockchain tokenization;
* on-chain voting;
* final government workflow state;
* external Smart City integrations.

Upstream systems can provide narratives and structured signals.

This gateway turns them into durable operational civic objects and exposes normalized outputs to downstream DOGEstonia or external systems.

---

## Project status

This repository is under active development.

The `dev` branch contains the current working runtime and should not be confused with earlier architecture-only baselines still referenced by some historical documents in the repository.

The API and data contracts may continue to evolve as the DOGEstonia node architecture is generalized.

---

## Documentation

Detailed product requirements, architecture decisions, audits, and implementation analysis are kept under [`docs/`](./docs).

Useful starting points include:

* [`docs/requirements/01-module-mission.md`](./docs/requirements/01-module-mission.md)
* [`docs/requirements/03-scope-and-boundaries.md`](./docs/requirements/03-scope-and-boundaries.md)
* [`docs/requirements/07-dynamic-clusters-product-model.md`](./docs/requirements/07-dynamic-clusters-product-model.md)
* [`docs/requirements/08-distinct-issue-product-logic.md`](./docs/requirements/08-distinct-issue-product-logic.md)
* [`docs/solution architecture/`](./docs/solution%20architecture/)

Some documents preserve historical architecture and planning context. For runtime behaviour, the current `dev` source code is authoritative.

---

## DOGEstonia

DOGEstonia explores a civic infrastructure model in which individual lived experiences can become structured collective signals without erasing the people and context behind them.

This repository implements one part of that architecture: the operational layer that turns stories into usable civic intelligence.

---

## License

MIT License.

See [`LICENSE`](./LICENSE).
