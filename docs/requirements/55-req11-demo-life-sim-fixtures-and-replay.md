# 55. REQ11 — demo life sim: fixtures, profiles, story API replay

Parent: docs/requirements backlog/REQ11-DOGEstonia-Uus-Veerenni-Demo-Life-Simulation.md §1–§4, §3.1–3.4, §3.6, §6.1, §7.1 D1–D3/D5–D6, §7.2 K1/K3/K4, §8 Waves A–C/E  
Parent-id: dogestonia-uus-veerenni-demo-life-simulation  
Siblings:  
- doge-threads/docs/requirements/04-req11-demo-life-sim-threads-reactions-seed.md (contract: after issues exist — issue_id list + density=story count; fixture actor ids for comment/reaction attribution — **TBD auth**; optional shared profile URLs for threads base)  
- spa-app/docs/requirements/20-req11-demo-life-sim-board-threads-verify.md (contract: none invent; spa consumes existing board/`/node/issues` + threads tree after replay)  
Status: Draft — awaiting PA.2  
Justification: docs/analysis/brief-req-uus-veerenni-demo-life-simulation-2026-09-29.md; doge-complaints-gateway/docs/analysis/status-simulation-story-data-assembly-2026-09-29.md  
Дата: 2026-09-29 · materialized: 2026-09-29T11:39:39Z  

---

## 1) Goal

Дать воспроизводимый **JSON users + stories** и **profiled API replay** (local + Uus Veerenni deploy), чтобы нулевая контент-БД заполнялась через gateway intake → clustering → board cards; масштаб и языки/даты по parent; без SPA-логина демо-жителей.

## 2) Scope / Out of scope

**In:** GW-11-01…07 — fixtures scale; language mix; exponential 2026 timestamps; profiles; scripted stash→submit (or equivalent documented intake); multi-fixture submitter model; backdate contract; clustering wait handoff before social seed.  

**Out:** Threads comment/reaction HTTP (sibling); new spa chrome; Identity SPA accounts (K1); REQ8; SQL dump as primary Pass path (K4); inventing undocumented public field names without PA.2 proof.

## 3) Verified current state

| Fact | Evidence |
|------|----------|
| Runner loads canvas → stash→submit | `tests/simulation_runner.py`; `tests/simulation_intake_http.py`; `Makefile` `simulate` — status analysis §2.1 |
| Single user Bearer via email+password | `docs/runtime-docs/testing/simulation-runner-manual.md` (`GATEWAY_USER_EMAIL`/`PASSWORD`); SEED-04 |
| Canvas sizes 130 / 18 | `tests/sandbox/dogestonia_simulation_canvas_v0_1.json`, `…_v0_2.json` |
| Stories ≠ cards until cron / min size | `docs/runtime-docs/manuals/seed-demo-data-runbook-ru.md`; status §1; `CLUSTER_MIN_SIZE` in `example.env` |
| Live content empty after wipe | status analysis §3; parent D1 |
| Multi-user fixtures / profiles / threads seed / 2026 exp curve | **Absent** in current runner/canvas (parent D2–D5) |
| Intake backdate of fixture timestamps | **Unknown** — no verified runner/API field found at materialize |

## 4) Target behavior

1. On-disk users + stories JSON (~couple hundred users; Gaussian mean ~8–9 stories/user).  
2. Languages ≈ 60% et / 30% ru / 10% en.  
3. Timestamps span calendar 2026 with exponential intensity (steep from ~2026-09-30).  
4. Named profiles: at least `local` + Uus Veerenni deploy (URLs + token env refs).  
5. Script replays via gateway APIs into zero/wiped env; first run fills connected DB.  
6. Fixture times survive intake (documented backdate path — design in PA.2/implement; do not invent column here).  
7. Multi-fixture submitters (not only one `GATEWAY_USER_*`).  
8. Document wait for clustering before sibling social seed; card count follows clustering (K3).

## 5) Acceptance criteria

- [ ] D1/D2: wipe/zero → replay → board issues appear; scale ≈ couple hundred users × ~8–9 mean stories (Gaussian)  
- [ ] D3: `local` + Uus Veerenni profiles selectable  
- [ ] D5/D6: language mix measurable; timestamps not all `now()` — follow 2026 exponential curve  
- [ ] K1/K4: no SPA resident login requirement; primary path API+JSON  
- [ ] GW-11-07: runbook/script documents clustering wait before threads seed handoff  

## 6) Open questions

1. Exact user/story N and Gaussian params.  
2. Backdate: API field vs controlled seed endpoint vs DB assist after API create — **must lock before invent**.  
3. ~~How fixture submitters obtain verified Bearer…~~ → **Locked via** [`STORY-GW-REQ11-05`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-05-provision-fixture-users-identity.md): provision **200** real accounts (Supabase signup + Identity phone with `SMS_PROVIDER=file`); secrets file; 1:1 Bearer for replay. K1: no SPA resident login required for Pass. (Supersedes pool M=20 for new Pass.)  
4. Literal Uus Veerenni deploy base URLs / which services in profile.  
5. Exponential λ.

## 7) Dependencies

Parent §1–4, §6.1, §7, §8 Waves A–C/E; sibling threads `04-…` (post-issue seed); sibling spa `20-…` (verify); leverage EPIC-M2-19 / SEED-01…04 tooling where fit.
