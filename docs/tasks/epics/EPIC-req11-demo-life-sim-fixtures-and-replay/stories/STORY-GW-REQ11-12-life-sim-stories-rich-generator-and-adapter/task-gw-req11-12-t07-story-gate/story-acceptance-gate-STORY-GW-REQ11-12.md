# Story acceptance gate — STORY-GW-REQ11-12

- **Story:** Life-sim rich `stories.json` generator + adapter (v2)
- **Package:** `pkg-000110-20261002-gw-req11-12-life-sim-stories-rich-generator-and-adapter.yaml`
- **Result:** PASS
- **Date:** 2026-10-02T09:10:26Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ1112-01: Generator emits fixture v2 fields; scale/lang/2026 locks preserved | PASS | `life_sim_stories_v2_lib.py` / CLI; lang lock = v0_1 (1000/486/175); T01 |
| AC-GW-REQ1112-02: Diversity ≥ N unique bodies via composed templates (no LLM) | PASS | **1661/1661** unique bodies; full uniqueness; T02 |
| AC-GW-REQ1112-03: Optional params.json foci/tags; empty → defaults | PASS | params consume + civic defaults; pack params.json; T03 |
| AC-GW-REQ1112-04: Adapter prefers v2; 6-key thin remains | PASS | `life_sim_story_to_intake_payload` + fail-closed restored; T04 |
| AC-GW-REQ1112-05: Offline tests schema/diversity/round-trip + REQ11-10 smoke | PASS | pytest 15 passed; T05 |
| AC-GW-REQ1112-06: Pack under life_sim_packs/; Partial→Pass manual | PASS | `ls-20261002T0906Z-veerenni-v2-rich`; load-manual; T06 |

## Commands (live verification 2026-10-02T09:10:26Z)

```text
builder_resolve_queue.py --project gateway --verify → ok (pkg-000110)
builder_resolve_queue.py --project gateway --verify --check-dates → (post gate)
.venv/bin/python -m pytest tests/test_gw_req11_12*.py tests/test_gw_req11_10_replay_pack_wave.py -q → 15 passed
diversity: unique_bodies=1661 / N=1661 (full uniqueness; no 90% floor)
pack: tests/sandbox/life_sim_packs/ls-20261002T0906Z-veerenni-v2-rich/
branch: dev · no push · no P8 · 07 not reused · no invent HTTP/gpt_signals/taxonomy axis IDs
```
