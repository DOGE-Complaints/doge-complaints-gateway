# task-gw-req11-12-t02-diversity-composed-templates

## Task: implement/tooling — diversity composed templates (T02)

## Meta
- **Story:** [STORY-GW-REQ11-12](../STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md)
- **Type:** implement/tooling
- **Status:** 🟢 Done
- **Package:** pkg-000110
- **Skill declared:** python-pro
- **Depends on:** soft T01
- **Scaffolded:** 2026-10-02T09:02:38Z
- **Decision Ref:** backlog STORY-GW-REQ11-12

## Purpose
Deterministic composed templates so Pass = **≥ N unique `body` strings** at locked story count N (prefer full uniqueness); if infeasible without LLM, document floor + ≥90% with rationale. Scope #2 · **AC-GW-REQ1112-02**. **No LLM**.

## Code Facts
1. Unique bodies today **15** / 1661 — scarcity analysis §2.
2. Current BLURBS pool small — `generate_dogestonia_life_sim_fixtures_v0_1.py`.

## Gap
Composed-template diversity not Present (scaffold).

## Acceptance / DoD
- [x] Pass: ≥ N unique bodies via composed templates **or** documented floor + ≥90% rationale
- [x] Prefer full uniqueness when feasible; no LLM
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-12-t02.md` signed (P3)

## Where to change
- Generator/successor template composition (same sandbox tooling as T01)

## Out of scope
params.json (T03); adapter (T04); invent story texts via LLM; invent taxonomy/gpt_signals.

## Verification commands
```bash
# P3: count unique body in pack stories.json vs N
python3 -c "import json; from pathlib import Path; p=Path('doge-complaints-gateway/tests/sandbox/life_sim_packs'); print('packs', list(p.glob('*/stories.json'))[:5])"
```
