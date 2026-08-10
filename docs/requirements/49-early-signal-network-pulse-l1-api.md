# 49. Early Signal — Public Network Pulse L1 API (path + payload)

Parent: docs/requirements backlog/DOGEstonia-Early-Signal-Dashboard-Pre-Cluster-Product-Requirements.md §5.1, §10 Network Pulse, §22–23, §29  
Parent-id: early-signal-dashboard-pre-cluster  
Predecessor: [`48-early-signal-pre-cluster-data-readiness.md`](./48-early-signal-pre-cluster-data-readiness.md) (inventory only; **no** path)  
Siblings: spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md (Network Pulse consumer)  
Implements: STORY-GW-ES-02 T00 / pkg-000059  
Status: Accepted (operator P3 go-ahead 2026-08-10)  

Дата: 2026-08-10  
Проект: doge-complaints-gateway  
Фокус: **named** public GET path + non-PII L1 aggregate payload for Network Pulse

---

## 1) Goal

Зафиксировать HTTP path и JSON payload schema для публичного Network Pulse L1, чтобы GW-ES-02 мог wire handler без invent path в story body (AC T00).

---

## 2) Path (authoritative)

| Method | Path | Auth |
|--------|------|------|
| `GET` | `/tallinn/network-pulse` | **Public** — no `require_*_service_auth` (same class as `GET /tallinn/issues`) |

- Must be listed in `PUBLIC_ROUTES` (`asgi_app.py`).
- CORS: register `@app.options("/tallinn/network-pulse")` returning 200 (parity with Issues list).
- **Do not** reuse `/metrics` (service-auth; no Story counts).

---

## 3) Success envelope `data` payload

Envelope: existing `build_success_envelope(data=…)` shape.

| Key | Type | Semantics |
|-----|------|-----------|
| `stories_collected` | `integer` | `len(StoryRepository.list_stories())` |
| `languages` | `array` of `{ "key": string, "count": integer }` | Distinct counts by `narrative_language`; skip null/empty; sorted by count desc then key |
| `areas` | `array` of `{ "key": string, "count": integer }` | Distinct counts by `geo.admin_district`, else `admin_settlement`, else `admin_region`; skip if all empty |
| `topics` | `array` of `{ "label": string, "axis": string, "count": integer }` | Frequency of **public** taxonomy labels via `StoryLabelRepository` where `is_public_label_disposition` is true — **canonical-only** (TAX §24 / [`disposition.py`](../../src/core/taxonomy/disposition.py) `PUBLIC_LABEL_DISPOSITIONS`); not «всё кроме internal». Keys say **topic/label**, never Issue |
| `recent_stories_7d` | `integer` | Count of stories with `created_at` ≥ `now - 7 days` (UTC) |

### Forbidden in payload

- Any `submitter_*`, narrative text, contacts, Voices / unique submitters
- Field or copy implying «N Stories until Issue» / threshold gaming
- Keys named `issues`, `issue_count`, or treating topic frequencies as Issues

### Honesty note (docs only)

Small sample `areas` ≠ city coverage. Document in API_REFERENCE.

---

## 4) Acceptance criteria

1. AC-49-01: Path `GET /tallinn/network-pulse` is the sole SSOT path for Pulse L1 in this REQ.
2. AC-49-02: Payload keys match §3 table; Topic≠Issue naming.
3. AC-49-03: Public route (no service-auth); Issues L3 path unchanged.
4. AC-49-04: Implementation story = GW-ES-02 (pkg-000059); no Emerging L2 here (→ ES-03).

---

## 5) Out of scope

- Emerging L2; Voices; SQL/`count` RPC optimization; inventing alternate paths; spa layout.
