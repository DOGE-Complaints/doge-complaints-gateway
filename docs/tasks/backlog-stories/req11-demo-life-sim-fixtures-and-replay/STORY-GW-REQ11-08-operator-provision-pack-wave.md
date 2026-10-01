# STORY-GW-REQ11-08 — Operator provision pack wave (CLI + wave-state + RU manual)

## Meta
- **Key:** `STORY-GW-REQ11-08-operator-provision-pack-wave`
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) P3 2026-10-01T10:31:41Z · gate PASS
- **Pipeline:** [`../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-08-operator-provision-pack-wave/STORY-GW-REQ11-08-operator-provision-pack-wave.md`](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-08-operator-provision-pack-wave/STORY-GW-REQ11-08-operator-provision-pack-wave.md) · [`pkg-000106`](../../gateway-active-packages/pkg-000106-20261001-gw-req11-08-operator-provision-pack-wave.yaml)
- **Тип:** tooling / operator CLI for life-sim Auth provision
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md) §4 multi-fixture submitter / Auth model; improves live Pass after REQ11-05
- **Parent product:** REQ11 §3.3 Auth model, §7.2 K1/K4
- **Justification:** operator 2026-10-01 — нужен **понятный терминальный** прогон provision из **pack** `users.json` с отдельным wave-status, resume, wipe-or-skip; жёстко `SMS_PROVIDER=file` + `@dogestonia.me`; без агентского чата на каждый прогон
- **Siblings:** soft STORY-GW-REQ11-05 (Present tooling — **reuse/refactor**); soft STORY-GW-REQ11-06 (content wipe — **orthogonal**, не Auth users); soft pack layout / REQ11-01 scale
- **Skill declared (future P3):** `python-pro`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Зависит от:** soft STORY-GW-REQ11-05; pack `users.json` Present (e.g. `life_sim_packs/<pack_id>/users.json`)
- **Blocks:** operator self-serve full 200 verified accounts → life-sim replay
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Name ≠ create:** пути скрипта / shared config / wave JSON / RU manual ниже — **acceptance targets** до P3; эта постановка **не** materialize код/мануал
- **Note:** **STORY-GW-REQ11-07 removed** (pack-gen) — номер **07 не переиспользовать**

---

## Goal

Дать оператору **один чистый вход** (CLI + Make/shell) для создания и phone-верификации life-sim жителей из **pack** `users.json`: жёсткие shared settings (`SMS_PROVIDER=file`, email `@dogestonia.me`, Auth = Identity Supabase), **отдельный wave-state** по каждому `fixture_user_id` (не внутри fixture JSON), **resume**, на старте выбор **wipe fixture-auth users** или **skip-if-exists**, и **мануал на русском** — чтобы прогон делался из терминала без агента.

---

## Scope

1. **Операторский CLI** (target names — lock in P3): e.g. `tests/sandbox/life_sim_provision_pack_wave.py` **или** рефактор существующего [`life_sim_provision_users.py`](../../../tests/sandbox/life_sim_provision_users.py) в чистую раскладку (`config` / `wave_store` / `auth_ops` / `cli`) + Make/shell entry. Допускается **reuse или copy-then-delete** disposable forks из execute-волны; целевая архитектура — **один** понятный модуль, без параллельных «почти одинаковых» скриптов.
2. **Shared settings (hard, fail-closed):**
   - OTP path: только **`SMS_PROVIDER=file`** + readable outbox (`FILE_SMS_OUTBOX_DIR` / `LIFE_SIM_FILE_SMS_OUTBOX_DIR`); если Identity не file / outbox отсутствует → STOP (не silent fallback на mock/Telnyx; **не** invent `GET /dev/last-otp`).
   - Email domain: **`@dogestonia.me`** (вынести из ad-hoc `_EMAIL_DOMAIN`; не `dogestonia.com`).
   - Auth Supabase credentials = **Identity project** (не gateway content DB) — иначе JWT не проходит `GET /me` (execute evidence 2026-09-30).
3. **Input:** `LIFE_SIM_PACK_DIR` (или эквивалент) → immutable [`users.json`](../../../tests/sandbox/life_sim_packs/ls-20260930T0938Z-veerenni-yard-construction/users.json). **Запрет:** писать статусы provision в fixture `users.json`.
4. **Wave-state JSON (отдельно от fixture):** per wave под pack, target layout e.g. `life_sim_packs/<pack_id>/waves/<wave_id>/state.json` (точный path — P3). На каждого `fixture_user_id`: `pending` | `created` | `verified` | `failed` (+ utc, error). **Checkpoint после каждого** успешного/неуспешного шага. **Resume:** skip entries already `verified`.
5. **Secrets:** по-прежнему gitignored (reuse `.secrets/life_sim_users_creds_*` или wave-colocated gitignored secrets — P3; **never commit**). Min fields совместимы с replay 1:1 Bearer (`fixture_user_id`, `email`, `password`, `phone_e164`, …).
6. **Startup mode (входящая переменная/флаг — выбор оператора):**
   - **`skip`** (default): не дублировать — если Auth+`phone_verified` уже есть и/или wave=`verified` → skip.
   - **`wipe-fixture-users`:** удалить **только** Auth-пользователей, детерминированно выведенных из **этой** фикстуры (email/phone derive); **не** content wipe REQ11-06; **не** чужих admin/Identity users вне фикстуры; require explicit confirm (`--confirm-wipe-fixture-users` / env).
7. **Provision path (reuse 05):** signup/admin-confirm → password grant → phone request → read OTP from **file outbox** → confirm → `GET /me` `phone_verified=true`. Pace: phone rate-limit **per-user**; для file-mode default pace **не** обязан быть 65s (lock numeric default in P3).
8. **Smoke:** `--limit N` + full pack N. Offline tests where feasible (config fail-closed, wave checkpoint/resume, derive email domain).
9. **RU manual (target):** [`docs/runtime-docs/manuals/life-sim-provision-pack-wave-manual-ru.md`](../../../runtime-docs/manuals/life-sim-provision-pack-wave-manual-ru.md) — env, pack_id, wipe vs skip, smoke, где смотреть wave/secrets, preconditions Identity file SMS. Cross-link из [`life-sim-demo-node-load-manual-ru.md`](../../../runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md) § provision.

## Out of scope

- Content wipe stories/issues/threads (STORY-GW-REQ11-06 — отдельно).
- Threads seed / SPA verify / full `Life_sim_load` replay (siblings / later operator run).
- Mutating pack `users.json` / `stories.json` for status.
- Invent Identity OTP HTTP backdoor; pilot/Telnyx as default for this CLI.
- SPA resident browser login for demo Pass (K1).
- Regenerating fixtures scale (REQ11-01).
- Implementing script/manual/code in the same turn as this backlog story (**name ≠ create**).
- Reopening removed STORY-GW-REQ11-07 pack-gen.

---

## Verified current state (As-of-Done 2026-10-01T10:31:41Z)

| Fact | Evidence |
|------|----------|
| Pack-wave CLI + Make | `tests/sandbox/life_sim_provision_pack_wave.py`, `make life-sim-provision-pack-wave` |
| Shared config fail-closed | `tests/sandbox/life_sim_provision_config.py` — `SMS_PROVIDER=file`, `@dogestonia.me`, Identity Auth force |
| Wave-state | `tests/sandbox/life_sim_wave_store.py` → `pack/waves/<wave_id>/state.json` (gitignored under packs) |
| Modes | `skip` (default) \| `wipe-fixture-users` (+ confirm); wipe refuse exit 2 without confirm |
| RU manual | [`life-sim-provision-pack-wave-manual-ru.md`](../../../runtime-docs/manuals/life-sim-provision-pack-wave-manual-ru.md) + load-manual § provision cross-link |
| Offline tests | `tests/test_gw_req11_08_provision_pack_wave.py` 6 passed |
| REQ11-05 foundation Present | `life_sim_provision_users.py`, `life_sim_provision_lib.py`, `make life-sim-provision-users` |
| Secrets gitignored | `tests/sandbox/.secrets/` + gateway `.gitignore` |
| File OTP path | Identity `SMS_PROVIDER=file` + outbox parse; no invent `GET /dev/last-otp` |
| Pack users fixture | `tests/sandbox/life_sim_packs/<pack_id>/users.json` (read-only for status) |
| Content wipe orthogonal | STORY-GW-REQ11-06 / `life_sim_wipe_node_content.py` |
| Live Auth leftover (G1 WAIVED) | full/smoke live provision + live wipe **not** run in P3 (documented) |

## Verified current state (Historical — backlog scaffold 2026-10-01T10:09:09Z / pre-P3)

| Fact | Evidence |
|------|----------|
| Pack-wave state JSON | **Absent** |
| Operator RU pack-wave manual | **Absent** |
| Hard shared config module | **Absent** as dedicated module |
| `wipe-fixture-users` vs `skip` switch | **Absent** |
| Flat `dogestonia_life_sim_users_v0_1.json` | **Absent** as SSOT (cleaned 2026-09-30); pack is users source |
| REQ11-05 / pack / secrets / file OTP | Present foundation (unchanged) |

---

## Target / AC

- [x] **AC-GW-REQ1108-01:** CLI читает pack `users.json`; **никогда** не пишет туда статусы provision.
- [x] **AC-GW-REQ1108-02:** Shared config жёстко требует `SMS_PROVIDER=file` + `@dogestonia.me` + Identity Auth Supabase; иначе fail-closed.
- [x] **AC-GW-REQ1108-03:** Wave-state JSON per wave отслеживает каждого `fixture_user_id`; checkpoint; resume skips `verified`.
- [x] **AC-GW-REQ1108-04:** Входящий режим `skip` (default) **или** `wipe-fixture-users` (+ confirm); wipe только fixture-derived Auth users; не REQ11-06 content.
- [x] **AC-GW-REQ1108-05:** RU manual Present; оператор может smoke/`--limit` и full из терминала без чата.
- [x] **AC-GW-REQ1108-06:** Чистая раскладка на базе REQ11-05 tooling (reuse/refactor); secrets gitignored; K1 соблюдён; offline tests на config/wave где feasible.

---

## Code touchpoints (As-of-Done)

- `tests/sandbox/life_sim_provision_pack_wave.py` + `make life-sim-provision-pack-wave` (Present)
- `tests/sandbox/life_sim_provision_config.py` (Present)
- `tests/sandbox/life_sim_wave_store.py` (Present)
- `docs/runtime-docs/manuals/life-sim-provision-pack-wave-manual-ru.md` (Present)
- Reuse: `life_sim_provision_users.py` / `life_sim_provision_lib.py` (Present)
- Orthogonal: `life_sim_wipe_node_content.py` (REQ11-06)

### Historical (scaffold «named only» / pre-P3)

- Pack-wave CLI / shared config / wave store / RU manual (Absent)
- Mode `skip` \| `wipe-fixture-users` (Absent)

---

## Dependencies

- Soft: STORY-GW-REQ11-05 Present (foundation to refactor).
- Pack with `users.json` on disk.
- Identity up with **file** SMS + outbox; `APP_PROFILE` ≠ `pilot` for file (PV-10).
- Operator: never commit secrets; confirm before wipe-fixture-users; content wipe = REQ11-06 if needed separately.
