# STORY-GW-REQ11-08 — Operator provision pack wave (CLI + wave-state + RU manual)

## Meta
- **Key:** `STORY-GW-REQ11-08-operator-provision-pack-wave`
- **Parent Epic:** [`../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md`](../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md)
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) P3 2026-10-01T10:31:41Z · gate PASS
- **Тип:** tooling / operator CLI for life-sim Auth provision
- **source:** [`../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-08-operator-provision-pack-wave.md`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-08-operator-provision-pack-wave.md)
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md) §4 multi-fixture submitter / Auth model
- **decision_ref:** backlog REQ11-08 · REQ55 §4 · REQ11 §3.3/§7.2 K1/K4 · operator 2026-10-01 pack-wave
- **Skill declared:** python-pro
- **Operative package:** [`../../../../gateway-active-packages/pkg-000106-20261001-gw-req11-08-operator-provision-pack-wave.yaml`](../../../../gateway-active-packages/pkg-000106-20261001-gw-req11-08-operator-provision-pack-wave.yaml)
- **Git:** `dev`
- **Operator locks:** `SMS_PROVIDER=file`; email `@dogestonia.me`; Identity Auth Supabase; pack `users.json` read-only for status; wave-state separate; `skip`|`wipe-fixture-users`; never invent `GET /dev/last-otp`; never commit secrets; **do not reuse** REQ11-07
- **Зависит от:** soft STORY-GW-REQ11-05; pack `users.json` Present
- **Scaffolded:** 2026-10-01T10:23:41Z

## Nested tasks (pkg-000106)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req11-08-t01-cli-pack-users-entry`](./task-gw-req11-08-t01-cli-pack-users-entry/README.md) | Done |
| T02 | [`task-gw-req11-08-t02-shared-config-fail-closed`](./task-gw-req11-08-t02-shared-config-fail-closed/README.md) | Done |
| T03 | [`task-gw-req11-08-t03-wave-state-checkpoint-resume`](./task-gw-req11-08-t03-wave-state-checkpoint-resume/README.md) | Done |
| T04 | [`task-gw-req11-08-t04-skip-or-wipe-fixture-auth-provision`](./task-gw-req11-08-t04-skip-or-wipe-fixture-auth-provision/README.md) | Done |
| T05 | [`task-gw-req11-08-t05-ru-manual-pack-wave`](./task-gw-req11-08-t05-ru-manual-pack-wave/README.md) | Done |
| T06 | [`task-gw-req11-08-t06-offline-unit-tests`](./task-gw-req11-08-t06-offline-unit-tests/README.md) | Done |
| T07 | [`task-gw-req11-08-t07-story-gate`](./task-gw-req11-08-t07-story-gate/README.md) | Done |
| T08 | [`task-gw-req11-08-t08-audit-g2-as-of-done-ssot`](./task-gw-req11-08-t08-audit-g2-as-of-done-ssot/README.md) | Done (audit wave `gw_req11_08_audit_followup`) |

## Goal

Дать оператору **один чистый вход** (CLI + Make/shell) для создания и phone-верификации life-sim жителей из **pack** `users.json`: жёсткие shared settings (`SMS_PROVIDER=file`, email `@dogestonia.me`, Auth = Identity Supabase), **отдельный wave-state** по каждому `fixture_user_id` (не внутри fixture JSON), **resume**, на старте выбор **wipe fixture-auth users** или **skip-if-exists**, и **мануал на русском** — чтобы прогон делался из терминала без агента.

## Scope

1. **Операторский CLI** (target names — lock in P3): e.g. `tests/sandbox/life_sim_provision_pack_wave.py` **или** рефактор существующего [`life_sim_provision_users.py`](../../../../../../tests/sandbox/life_sim_provision_users.py) в чистую раскладку (`config` / `wave_store` / `auth_ops` / `cli`) + Make/shell entry. Допускается **reuse или copy-then-delete** disposable forks из execute-волны; целевая архитектура — **один** понятный модуль, без параллельных «почти одинаковых» скриптов.
2. **Shared settings (hard, fail-closed):**
   - OTP path: только **`SMS_PROVIDER=file`** + readable outbox (`FILE_SMS_OUTBOX_DIR` / `LIFE_SIM_FILE_SMS_OUTBOX_DIR`); если Identity не file / outbox отсутствует → STOP (не silent fallback на mock/Telnyx; **не** invent `GET /dev/last-otp`).
   - Email domain: **`@dogestonia.me`** (вынести из ad-hoc `_EMAIL_DOMAIN`; не `dogestonia.com`).
   - Auth Supabase credentials = **Identity project** (не gateway content DB) — иначе JWT не проходит `GET /me` (execute evidence 2026-09-30).
3. **Input:** `LIFE_SIM_PACK_DIR` (или эквивалент) → immutable pack `users.json`. **Запрет:** писать статусы provision в fixture `users.json`.
4. **Wave-state JSON (отдельно от fixture):** per wave под pack, target layout e.g. `life_sim_packs/<pack_id>/waves/<wave_id>/state.json` (точный path — P3). На каждого `fixture_user_id`: `pending` | `created` | `verified` | `failed` (+ utc, error). **Checkpoint после каждого** успешного/неуспешного шага. **Resume:** skip entries already `verified`.
5. **Secrets:** по-прежнему gitignored (reuse `.secrets/life_sim_users_creds_*` или wave-colocated gitignored secrets — P3; **never commit**). Min fields совместимы с replay 1:1 Bearer (`fixture_user_id`, `email`, `password`, `phone_e164`, …).
6. **Startup mode (входящая переменная/флаг — выбор оператора):**
   - **`skip`** (default): не дублировать — если Auth+`phone_verified` уже есть и/или wave=`verified` → skip.
   - **`wipe-fixture-users`:** удалить **только** Auth-пользователей, детерминированно выведенных из **этой** фикстуры (email/phone derive); **не** content wipe REQ11-06; **не** чужих admin/Identity users вне фикстуры; require explicit confirm (`--confirm-wipe-fixture-users` / env).
7. **Provision path (reuse 05):** signup/admin-confirm → password grant → phone request → read OTP from **file outbox** → confirm → `GET /me` `phone_verified=true`. Pace: phone rate-limit **per-user**; для file-mode default pace **не** обязан быть 65s (lock numeric default in P3).
8. **Smoke:** `--limit N` + full pack N. Offline tests where feasible (config fail-closed, wave checkpoint/resume, derive email domain).
9. **RU manual (target):** [`docs/runtime-docs/manuals/life-sim-provision-pack-wave-manual-ru.md`](../../../../runtime-docs/manuals/life-sim-provision-pack-wave-manual-ru.md) — env, pack_id, wipe vs skip, smoke, где смотреть wave/secrets, preconditions Identity file SMS. Cross-link из [`life-sim-demo-node-load-manual-ru.md`](../../../../runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md) § provision.

## Out of scope

- Content wipe stories/issues/threads (STORY-GW-REQ11-06 — отдельно).
- Threads seed / SPA verify / full `Life_sim_load` replay (siblings / later operator run).
- Mutating pack `users.json` / `stories.json` for status.
- Invent Identity OTP HTTP backdoor; pilot/Telnyx as default for this CLI.
- SPA resident browser login for demo Pass (K1).
- Regenerating fixtures scale (REQ11-01).
- Implementing script/manual/code in the same turn as this scaffold (**name ≠ create** / no product execute this APPLY).
- Reopening removed STORY-GW-REQ11-07 pack-gen.

## Verified current state (As-of-Done P3 2026-10-01T10:31:41Z)

| Fact | Evidence |
|------|----------|
| Pack-wave CLI Present | `tests/sandbox/life_sim_provision_pack_wave.py` + `make life-sim-provision-pack-wave` |
| Shared config fail-closed | `life_sim_provision_config.py` |
| Wave-state Present | `life_sim_wave_store.py` → `pack/waves/<id>/state.json` |
| RU manual Present | `docs/runtime-docs/manuals/life-sim-provision-pack-wave-manual-ru.md` |
| Offline tests | `tests/test_gw_req11_08_provision_pack_wave.py` 6 passed |
| Gate | [`story-acceptance-gate-STORY-GW-REQ11-08.md`](./task-gw-req11-08-t07-story-gate/story-acceptance-gate-STORY-GW-REQ11-08.md) PASS |
| Run summary | [`run-summary-20261001-1031-gw-req11-08-p3.md`](../../../../run-reports/run-summary-20261001-1031-gw-req11-08-p3.md) |

## Verified current state (Historical scaffold 2026-10-01T10:23:41Z)

| Fact | Evidence |
|------|----------|
| REQ11-05 provision Present | `tests/sandbox/life_sim_provision_users.py`, `life_sim_provision_lib.py`, `make life-sim-provision-users` |
| Secrets gitignored | `tests/sandbox/.secrets/` + gateway `.gitignore` |
| File OTP path | Identity `SMS_PROVIDER=file` + outbox parse; no `GET /dev/last-otp` |
| Pack users fixture | `tests/sandbox/life_sim_packs/<pack_id>/users.json` |
| Pack-wave state JSON | **Absent** |
| Operator RU pack-wave manual | **Absent** |
| Hard shared config module | **Absent** as dedicated module |
| `wipe-fixture-users` vs `skip` switch | **Absent** |

## Target / AC

- [x] **AC-GW-REQ1108-01:** CLI читает pack `users.json`; **никогда** не пишет туда статусы provision.
- [x] **AC-GW-REQ1108-02:** Shared config жёстко требует `SMS_PROVIDER=file` + `@dogestonia.me` + Identity Auth Supabase; иначе fail-closed.
- [x] **AC-GW-REQ1108-03:** Wave-state JSON per wave отслеживает каждого `fixture_user_id`; checkpoint; resume skips `verified`.
- [x] **AC-GW-REQ1108-04:** Входящий режим `skip` (default) **или** `wipe-fixture-users` (+ confirm); wipe только fixture-derived Auth users; не REQ11-06 content.
- [x] **AC-GW-REQ1108-05:** RU manual Present; оператор может smoke/`--limit` и full из терминала без чата.
- [x] **AC-GW-REQ1108-06:** Чистая раскладка на базе REQ11-05 tooling (reuse/refactor); secrets gitignored; K1 соблюдён; offline tests на config/wave где feasible.

## Code touchpoints (named targets + Present reuse)

| Area | Path / note |
|------|-------------|
| **Reuse Present** | `tests/sandbox/life_sim_provision_users.py`, `life_sim_provision_lib.py`, `make life-sim-provision-users` |
| **Target CLI / modules** | clean pack-wave entry (name lock P3); shared settings module |
| **Wave state** | `life_sim_packs/<pack_id>/waves/<wave_id>/…` |
| **Fixture input** | `life_sim_packs/<pack_id>/users.json` — read-only for status |
| **RU manual** | `docs/runtime-docs/manuals/life-sim-provision-pack-wave-manual-ru.md` + link from life-sim load manual |
| **Orthogonal** | `life_sim_wipe_node_content.py` (content only) |

## Dependencies

- Soft: STORY-GW-REQ11-05 Present.
- Pack with `users.json` on disk.
- Identity up with **file** SMS + outbox; `APP_PROFILE` ≠ `pilot` for file (PV-10).
- Operator: P2 → P3; never commit secrets; confirm before wipe-fixture-users.
