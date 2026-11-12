# task-gw-req57-02-t03-corpus-from-issue-stories

## Task: implement — corpus from Issue Stories (T03)

## Meta
- **Story:** [STORY-GW-REQ57-02](../STORY-GW-REQ57-02-nudge-on-create-publish.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Done:** 2026-10-15T11:41:13Z
- **Package:** pkg-000114
- **Skill declared:** python-pro
- **Depends on:** T02
- **Scaffolded:** 2026-10-15T11:34:35Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-02-nudge-on-create-publish.md`
- **AC trace:** REQ §2; arch 02

## Purpose
Optional corpus from Issue Stories membership; no clustering change

## Code Facts
### Live (post-P3 close) — 2026-10-15T11:41:13Z
1. `build_corpus_from_stories` Present — optional corpus from Story membership.
2. Path: `sense_brief_nudge.py` (wired from create hook).

### Historical (scaffold / pre-P3) — 2026-10-15T11:34:35Z
1. Scaffold only.

## Gap
**Closed P3 2026-10-15T11:41:13Z.**

## Acceptance / DoD
- [x] Optional corpus built from Issue↔Stories membership
- [x] No clustering algorithm change
- [x] Passes through client when present
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-02-t03.md` signed (P3)

## Where to change
- Corpus builder from Issue Stories membership (read path)
- Client body optional field

## Out of scope
Clustering changes; client auth (T02); hook (T04)

## Verification commands
```bash
rg -n "corpus|sense_brief_nudge" doge-complaints-gateway/src --glob '*.py' | head -40
```
