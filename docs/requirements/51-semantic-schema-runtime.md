# 51. Semantic Schema Runtime (gateway platform capability)

Parent: docs/requirements backlog/REQ3-Semantic-Schema-Runtime-and-Node-Specific-Data-Processing.md including REQ3-WAVE-001, SCHEMA-005, CL-006, FLOW-003, SPA-003/004, GPT-001/002, AC-013…018, DoD §33.1 T-wave vs §33.2 remainder  
Parent-id: req3-semantic-schema-runtime  
Siblings: doge-identity-service/docs/requirements/20-semantic-schema-identity-boundary.md (contract: identity **не** хранит semantic schemas / `structured_payload` / `geo_detail`; REQ3-AC-011; FLOW-002 claim keys для schema policy **не** required для SSR 01–25 Done — sibling 20) · spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md (contract: public read `GET /node/issues`; `structured_payload` MUST NOT auto-become Issue — SPA-003; overlay via named **`schema_card`** when pack `card_fields` — SPA-004; board MAY list|map toggle when Issue has `geo.lat`+`geo.lon`) · GPT UI/docs/requirements/REQ-45-semantic-schema-intake-envelope-compatibility.md (contract: required envelope `schema_version` = `m2.story_intake_envelope.v2`; MUST emit root **`schema_binding`** matching node `NODE_SCHEMA_ID`/`NODE_SCHEMA_VERSION`; MAY emit root **`geo_detail`** and/or `location_query` per pack **`geo_intake`**)  
Status: Accepted — package delivered (SSR-01…05, 08–25 Done); SSR-06/07 later; PA.2 closed by operator 2026-09-01T10:12:26Z  

Дата: 2026-08-27; T-cover 2026-08-28; sibling-seam sync 2026-08-31T09:40:45Z; Status sync 2026-09-01T10:12:26Z  
Проект: doge-complaints-gateway  
Фокус: Schema Runtime, pack-driven node model, intake wire, Issue projection — **без** invented HTTP для generic filter / `GET /schema-active` / schema-metadata

Пакет backlog: [`docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md`](../tasks/backlog-stories/semantic-schema-runtime/INDEX.md) — SSR-01…05, 08–25 **Done**; SSR-06/07 **Draft later**; SSR-12 Draft experimental.

---

## 1) Goal

Сделать добавление node-specific semantic model **публикацией schema pack**, а не правкой `StoryRecord` / intake parser / колонок `stories` / hard-coded `ClusterLens` для declared exact lenses (parent §1, REQ3-AC-001, §32, §35). На ноде одна активная модель (`NODE_SCHEMA_*`); публичная доска читает контролируемую Issue projection, не сырой payload.

---

## 2) Scope / Out of scope

### In scope — delivered package (T-wave + post-T-wave through geo-detail)

- Schema Runtime in-process + SCHEMA-005 pack load (`schema-packs/`).
- Persist binding + `structured_payload` + `payload_hash` (DATA-001…004).
- Wire: root sidecar **`schema_binding`** (required on node) + optional **`geo_detail`**; pack **`geo_intake`**.
- Pack exact lenses + dual civic opt-in; civic knobs in pack **`node_clustering.civic`** (не семантические `CLUSTER_*` env).
- Issue projection: civic keys + optional **`schema_card`** from pack `card_fields`; Issue.`geo` with `lat`/`lon`/label/admin_* when present on dominant story.
- Public HTTP `/node/*` (D-SSR-7); ClusterLens enum **не** расширять.

### In scope — later 51 (SSR-06/07 Draft; not required to close current package)

- Analytical index + rebuildability (REQ3-IDX).
- Generic processor delivery (REQ3-PROC-*).

### Out of scope

- Full Federation Schema Registry / marketplace (§30).
- WASM / third-party executable plugins.
- Identity-service semantic models (sibling 20).
- SPA form builder / product epic; SPA map **UI** lives in sibling 16 (this REQ only guarantees Issue.`geo.lat`/`lon` on projection when available).
- Invented public HTTP: generic dimension filter, `GET /schema-active`, schema UI metadata (SPA-002).
- Microservice-per-schema; fifth child REQ «51-T».

---

## 3) Verified current state

| Fact | Path |
|------|------|
| Intake envelope constant | `src/core/intake/contracts.py` `INTAKE_SCHEMA_VERSION = "m2.story_intake_envelope.v2"` |
| Root `schema_binding` + `geo_detail` parse | `src/core/intake/contracts.py` (`SchemaBinding`, `GeoDetail`) |
| Binding MUST match `NODE_SCHEMA_ID`/`VERSION` | `src/core/application/services.py` (omit/`{}`/mismatch → 4xx) |
| Active pack env | `src/core/config/schema.py` `NODE_SCHEMA_ID`, `NODE_SCHEMA_VERSION` required |
| SchemaRuntime + packs | `src/core/schema/`; `schema-packs/<id>/<version>/` |
| `StoryGeoSnapshot` address depth | `src/core/domain/contracts.py` (street/house/house_range/houses/address_line + admin + lat/lon) |
| Pack `geo_intake` / `node_clustering.civic` | pack.json + `src/core/schema/contracts.py` |
| Issue public + optional `schema_card` | `src/core/projection/dto.py` `to_public_dict`; `card_fields.py` |
| Issue.`geo` keys | mapper: `lat`, `lon`, `label`, `district`, `settlement`, `region`, `country` (street/house **не** на Issue) |
| Public Issue list | `GET /node/issues` (`asgi_app.py`) |
| ClusterLens members | baseline **10** (`src/core/cluster/types.py`) |
| Identity claims → schema policy | **Not used** in SSR 01–25 (D-SSR-3; sibling 20) |
| `story_dimensions` / IDX HTTP | **Not delivered** (SSR-06 Draft) |

---

## 4) Target behavior

1. Stable `SchemaRuntime` in gateway; pack data under `schema-packs/`; active pair from `NODE_SCHEMA_*`.
2. Envelope id remains `m2.story_intake_envelope.v2`. Inner semantic version lives in `schema_binding.schema_version` / persist binding columns — **не** переиспользовать корневой envelope key.
3. **New intake:** root `schema_binding` **required**; pair MUST equal active node pack; `structured_payload` validated by that pack. Omit / mismatch → 4xx. (Legacy «omit binding = civic» **закрыт** для нового intake — D-SSR-8.)
4. Optional root `geo_detail` + `location_query` subject to pack `geo_intake.mode` (`optional` \| `require_location_or_detail` \| `require_detail`); merge + optional `mirror_to_payload` into `structured_payload.geo`.
5. Clustering: **two contours** — `exact_lenses` on payload paths; `node_clustering.civic` for `ClusterLens` (dual + unbound). Civic geo filter uses snapshot admin_*; pack geo lenses use mirrored `geo.*` when declared.
6. Issue create: civic projection + optional `schema_card` from allowlist; **no** dump `structured_payload`. Coords on Issue when dominant story has lat/lon.
7. IDX / processors — later (SSR-06/07); no QRY HTTP in this package close.
8. Sibling contracts: GPT emits binding (+ optional geo_detail); SPA overlays `schema_card` and MAY map-toggle on `geo.lat`/`lon`; identity unchanged.

---

## 5) Acceptance criteria

**Package (T-wave + post through geo-detail) — met in backlog Done stories; formal REQ Status Accepted (operator 2026-09-01).**

1. AC-GW-REQ3-01…04, 07, 10, 14, 15, 18 — as parent T-wave (pack, persist, wire, lenses, promote, no QRY).
2. AC-GW-NODE-01: active `NODE_SCHEMA_*`; intake without matching binding → 4xx.
3. AC-GW-GEO-01: `geo_detail` / `geo_intake` enforced; no silent skip when scope requires geo service.
4. AC-GW-PROJ-01: `schema_card` only from `card_fields`; Issue.`geo` exposes lat/lon/admin when present; no street auto-public unless later allowlisted into `schema_card`.
5. AC-GW-CL-01: civic knobs from `node_clustering.civic`; ClusterLens members unchanged (10).

**Later 51 (SSR-06/07)**

6. AC-GW-REQ3-05/06/09: IDX without inventing HTTP path in this Draft.
7. AC-GW-REQ3-08: processors when delivered.

---

## 6) Open questions

1. HTTP path/query for REQ3-QRY-001/002 / AC-005 — still unnamed (SSR-06 later).
2. **Closed:** intake wire names = `schema_binding`, `structured_payload`, `geo_detail` (gateway parser); GPT MUST/MAY per sibling REQ-45.
3. **Closed for SSR 01–25:** identity claim list for schema policy — not required (sibling 20; D-SSR-3).
4. **Closed for board overlay/map:** SPA-002 UI metadata path **not** required — SPA uses Issue body (`schema_card`, `geo.lat`/`lon`) from `GET /node/issues` (sibling 16).

---

## 7) Dependencies

- Parent: REQ3-PR / DATA / SCHEMA / RUNTIME / COMPAT / FLOW / CL / SPA / GPT, SEC, §23–29, §32–35.
- Siblings: identity 20, spa 16, GPT REQ-45 (seams in header).
- Package INDEX + runtime manual [`schema-packs-node-data-model-ru.md`](../runtime-docs/manuals/schema-packs-node-data-model-ru.md).
- Existing M2: inbound API, multilingual v2 envelope, clustering REQ 25/26/34 — compatibility baseline.
