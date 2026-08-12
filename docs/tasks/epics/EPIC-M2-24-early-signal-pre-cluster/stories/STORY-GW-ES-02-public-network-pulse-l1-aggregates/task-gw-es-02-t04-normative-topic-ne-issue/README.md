# task-gw-es-02-t04-normative-topic-ne-issue

## Meta
- **Story:** [STORY-GW-ES-02](../STORY-GW-ES-02-public-network-pulse-l1-aggregates.md)
- **Type:** docs / verify
- **Status:** 🟢 Done
- **Package:** pkg-000059
- **Skill declared:** python-pro
- **Depends on:** T01 (payload keys); soft T03
- **decision_ref:** backlog ES-02 §D; REQ-48 AC-GW-ES-04 Topic≠Issue

## Purpose
Гарантировать Topic ≠ Issue в ключах ответа и связанных notes; нет поля/копи «N Stories until Issue»; Issues L3 unchanged; no PII/Voices in Pulse surface.

## Code Facts
- Issues L3 route — `/tallinn/issues` in [`asgi_app.py:57-64`](../../../../../../../../src/core/api/asgi_app.py)
- Normative constraints — REQ-48 AC-GW-ES-03/04 [`48-…md`](../../../../../../../requirements/48-early-signal-pre-cluster-data-readiness.md)
- Gap note G-ES-INV-01 `/metrics` unfit — gap-analysis package

## Acceptance / DoD
- [x] Traces parent AC: Topic ≠ Issue; no «N Stories until Issue»; no PII / Voices
- [x] Response keys / service docs say topic/label, never Issue for taxonomy dims
- [x] No threshold-gaming counter field
- [x] `GET /tallinn/issues` behavior not altered by this task
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-es-02-t04.md` signed (Date post P3 verify only)

## Where to change
- Pulse payload key naming in `network_pulse.py` / handler envelope data
- Short normative note if needed (runtime-docs full pass = T06)

## Out of scope
- Full OpenAPI rewrite (T06); Emerging L2; Voices

## Verification commands
```bash
rg -n 'Issue|until Issue|stories_until|submitter_' doge-complaints-gateway/src/core/application/network_pulse.py || true
rg -n 'tallinn/issues' doge-complaints-gateway/src/core/api/asgi_app.py
```
