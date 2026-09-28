# 54. REQ10 — lifecycle_status normalize + debug cleanup

Parent: docs/requirements backlog/REQ10-DOGEstonia-Threads-Board-Architecture-Hardening.md §3.1, §3.4, §6.3, §7.1 H1/H4, §7.2 H8  
Parent-id: dogestonia-threads-board-architecture-hardening  
Siblings:  
- doge-threads/docs/requirements/03-req10-tree-marks-read-and-contract.md (contract: none for lifecycle; threads continues to consume gateway Issue envelope `{data,trace_id}`)  
- spa-app/docs/requirements/19-req10-threads-reaction-reload-honesty.md (contract: none)  
Status: Draft — awaiting PA.2  
Justification: docs/analysis/audit-threads-board-persist-clean-vs-hack-2026-09-27.md §3, §8  
Дата: 2026-09-28 · materialized: 2026-09-28T11:05:54Z  

---

## 1) Goal

Нормализовать legacy `lifecycle_status` в данных (`RECEIVED`/`received` → `accepted`), убрать постоянный спецкейс (или жёстко загейтить), удалить debug file I/O из lifecycle parse. Stretch: note on `list_all` labels scale (H8).

## 2) Scope / Out of scope

**In:** Inventory distinct values; Supabase (and sqlite fixtures if used) backfill; slim `_parse_lifecycle_status`; remove absolute debug log path (H1 gateway / H4).  

**Out:** Threads tree/reactions; spa UI; inventing new public APIs; mandatory SQL aggregate for pulse labels (H8 stretch only); REQ8.

## 3) Verified current state

| Fact | Evidence |
|------|----------|
| Enum `ACCEPTED = "accepted"` | `src/core/domain/contracts.py` `StoryLifecycleStatus` |
| Read adapter maps `RECEIVED`/`received` → ACCEPTED | `src/core/infrastructure/db_supabase.py` `_parse_lifecycle_status` |
| Debug write to absolute `.cursor/debug-ba94c7.log` inside mapper | same function |
| Used from story row hydrate | `_story_record_from_supabase_row` calls `_parse_lifecycle_status` |
| Distinct live DB value set | **Unknown** — requires inventory (GW-10-01) |

## 4) Target behavior

1. Persisted legacy RECEIVED strings normalized to `accepted`.  
2. After backfill, mapper does not need a growing legacy dict for those values; unknown values fail closed.  
3. No absolute debug-file I/O in lifecycle parse.  
4. Stretch: document scale limits of `StoryLabelRepository.list_all` — not Pass.

## 5) Acceptance criteria

- [ ] H1 (gateway): no `.cursor/debug-*.log` writes from production lifecycle path  
- [ ] H4: backfill done for known legacy RECEIVED; board/story reads no longer depend on permanent RECEIVED special-case (prefer remove)  
- [ ] Unknown lifecycle values still fail closed  
- [ ] H8 stretch optional

## 6) Open questions

1. Full set of distinct `lifecycle_status` in hosted Supabase — Unknown until inventory.  
2. sqlite-only demos: same backfill required? — Unknown until fixture scan.

## 7) Dependencies

Parent §3.1, §3.4, §6.3, §7.1; no reaction seam with spa/threads children.
