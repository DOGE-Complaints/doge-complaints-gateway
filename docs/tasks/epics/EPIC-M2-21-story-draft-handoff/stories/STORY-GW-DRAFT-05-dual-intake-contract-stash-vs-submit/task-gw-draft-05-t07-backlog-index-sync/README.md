# task-gw-draft-05-t07-backlog-index-sync

## Meta
- **Story:** [STORY-GW-DRAFT-05](../STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md)
- **Type:** docs
- **Status:** ⚪ Todo
- **Package:** pkg-000049
- **Skill declared:** python-pro
- **Depends on:** T01–T06 (content accurate before sync)

## Purpose
Backlog T07: update GW-DRAFT-01 cross-ref («тот же StoryIntakeRequest» → link GW-DRAFT-05); update story-draft-handoff INDEX row for GW-DRAFT-05.

## Code Facts
- GW-DRAFT-01 backlog already partial ref — [`STORY-GW-DRAFT-01-story-draft-stash.md`](../../../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-01-story-draft-stash.md) lines on GW-DRAFT-05
- Package INDEX — [`story-draft-handoff/INDEX.md`](../../../../../../backlog-stories/story-draft-handoff/INDEX.md) row 5 Todo

## Acceptance / DoD
- [ ] GW-DRAFT-01 backlog: stale «тот же StoryIntakeRequest для stash» → explicit GW-DRAFT-05 dual-contract link
- [ ] `story-draft-handoff/INDEX.md` GW-DRAFT-05 row reflects pipeline link + In Progress/scaffolded state
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-draft-05-t07.md`](./acceptance-verification-gw-draft-05-t07.md) signed (Date post P3 verify only)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/STORY-GW-DRAFT-01-story-draft-stash.md`
- `doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/INDEX.md`

## Out of scope
- Deleting backlog GW-DRAFT-05 source file; pipeline story edits beyond cross-links

## Verification commands
```bash
cd doge-complaints-gateway && rg 'GW-DRAFT-05|StoryDraftStashRequest' docs/tasks/backlog-stories/story-draft-handoff/STORY-GW-DRAFT-01-story-draft-stash.md
cd doge-complaints-gateway && rg 'GW-DRAFT-05' docs/tasks/backlog-stories/story-draft-handoff/INDEX.md
```
