# 50. Early Signal — Public Emerging L2 API (path + payload + MVP rule)

Parent: docs/requirements backlog/DOGEstonia-Early-Signal-Dashboard-Pre-Cluster-Product-Requirements.md §5.2 L2, §6.2 Emerging Signal, §12, §22–23, §33  
Parent-id: early-signal-dashboard-pre-cluster  
Predecessor: [`48-early-signal-pre-cluster-data-readiness.md`](./48-early-signal-pre-cluster-data-readiness.md) (inventory; open Q2)  
Sibling L1: [`49-early-signal-network-pulse-l1-api.md`](./49-early-signal-network-pulse-l1-api.md)  
Siblings: spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md (Emerging Signals consumer)  
Implements: STORY-GW-ES-03 T00 / pkg-000060  
Status: Accepted (operator P3 go-ahead 2026-08-10)  

Дата: 2026-08-10  
Проект: doge-complaints-gateway  
Фокус: **named** public GET path + non-PII Emerging L2 payload; MVP derivation rule closes REQ-48 open Q2 for this MVP

---

## 1) Goal

Зафиксировать HTTP path и JSON payload schema для публичного Emerging L2, чтобы GW-ES-03 мог wire handler без invent path в story body (AC T00), и закрыть MVP-ответ на REQ-48 §6 Q2.

---

## 2) Path (authoritative)

| Method | Path | Auth |
|--------|------|------|
| `GET` | `/tallinn/emerging-signals` | **Public** — no `require_*_service_auth` (same class as `GET /tallinn/issues` / Network Pulse) |

- Must be listed in `PUBLIC_ROUTES` (`asgi_app.py`).
- CORS: register `@app.options("/tallinn/emerging-signals")` returning 200.
- **Do not** reuse `/tallinn/issues` (L3 Issues projections) or `/tallinn/network-pulse` (L1 Pulse).

### Query parameters

| Param | Type | Default | Semantics |
|-------|------|---------|-----------|
| `top_n` | integer | `10` | Max number of emerging signals returned; clamp to `[1, 50]` |

---

## 3) Success envelope `data` payload

Envelope: existing `build_success_envelope(data=…)` shape.

| Key | Type | Semantics |
|-----|------|-----------|
| `signals` | `array` of `{ "label": string, "axis": string, "story_count": integer }` | Top-N public taxonomy label frequencies after published-exclusion (see §4); sorted by `story_count` desc, then `label`, then `axis` |
| `top_n` | `integer` | Applied `top_n` after clamp |

### Forbidden in payload

- Any `submitter_*`, narrative text, contacts, Voices / unique submitters
- Field or copy implying «N Stories until Issue» / threshold gaming
- Issue ids as the **primary** emerging identity; keys named `issues` / `issue_count`
- Treating Emerging rows as Issues projections

### Honesty note (docs only)

Emerging is **derived / ephemeral** (parent §6.2) — not a persistent `EmergingSignal` entity in this REQ.

---

## 4) MVP derivation rule (closes REQ-48 open Q2 for MVP)

**Emerging L2 = top-N taxonomy label frequencies** across stories, **excluding** any story that links to an Issue projection whose status maps to cabinet **published** (`map_issue_status_to_cabinet` / `canonicalize_status_on_read`).

- **Source of labels:** `StoryLabelRepository.list_by_story` (public dispositions only via `is_public_label_disposition`) — **not** `IssueProjectionReadStore.list_projections` as the emerging source.
- **Axis:** all axes present on public labels (no single-axis hard filter in MVP).
- **Default `top_n`:** `10` (query override §2).
- **Not equal** to Issues list shape/source.
- **No** persistent `EmergingSignal` table in this REQ / GW-ES-03.
- Clustering / promotion gates **unchanged** (parent §33).

---

## 5) Acceptance criteria

1. AC-50-01: Path `GET /tallinn/emerging-signals` is the sole SSOT path for Emerging L2 in this REQ.
2. AC-50-02: Payload keys match §3; Topic/label language; `top_n` present.
3. AC-50-03: MVP rule §4 is normative for GW-ES-03 implementation.
4. AC-50-04: Public route (no service-auth); Issues L3 and Pulse L1 paths unchanged.
5. AC-50-05: Implementation story = GW-ES-03 (pkg-000060).

---

## 6) Out of scope

- Network Pulse L1 (→ REQ-49 / ES-02); Voices; `EmergingSignal` DDL; inventing alternate paths; spa layout; k-anonymity floor (follow-up); replacing labels with `story_signals` / memberships (successor + ADR).
