# Life-sim provision pack-wave — операторский мануал (RU)

**Story:** STORY-GW-REQ11-08 · **Package:** `pkg-000106`  
**CLI:** `tests/sandbox/life_sim_provision_pack_wave.py` · **Make:** `life-sim-provision-pack-wave`  
**Связанный load-мануал:** [`life-sim-demo-node-load-manual-ru.md`](./life-sim-demo-node-load-manual-ru.md) § provision.

---

## Цель

Один терминальный вход: создать/верифицировать жителей из **pack** `users.json` с отдельным **wave-state**, resume и режимом `skip` | `wipe-fixture-users` — без агентского чата на каждый прогон.

---

## Preconditions (fail-closed)

| Требование | Значение |
|------------|----------|
| OTP | Identity `SMS_PROVIDER=file` + readable outbox (`FILE_SMS_OUTBOX_DIR` / `LIFE_SIM_FILE_SMS_OUTBOX_DIR`) |
| Email | только `*@dogestonia.me` |
| Auth DB | Supabase **Identity** project (скрипт форсит Identity `SUPABASE_*`) |
| Pack | `LIFE_SIM_PACK_DIR` → каталог с `users.json` |
| Секреты | пишутся только в `tests/sandbox/.secrets/` — **never commit** |
| Запрет | invent `GET /dev/last-otp`; писать статусы в fixture `users.json`; content wipe (это REQ11-06) |

Если `SMS_PROVIDER≠file` или outbox недоступен — CLI **STOP** (exit ≠ 0).

---

## Команды

Из `doge-complaints-gateway/`:

```bash
# Smoke (2 пользователя)
LIFE_SIM_PACK_DIR=tests/sandbox/life_sim_packs/ls-20260930T0938Z-veerenni-yard-construction \
  make life-sim-provision-pack-wave LIMIT=2

# Full pack
LIFE_SIM_PACK_DIR=tests/sandbox/life_sim_packs/ls-20260930T0938Z-veerenni-yard-construction \
  make life-sim-provision-pack-wave

# Явный wave id + dry-run (без Auth HTTP)
LIFE_SIM_PACK_DIR=… LIFE_SIM_PROVISION_DRY_RUN=1 WAVE_ID=demo-wave-1 \
  make life-sim-provision-pack-wave LIMIT=5

# Wipe только fixture-derived Auth users, затем provision
LIFE_SIM_PACK_DIR=… LIFE_SIM_PACK_WAVE_MODE=wipe-fixture-users \
  LIFE_SIM_WIPE_FIXTURE_USERS=1 make life-sim-provision-pack-wave LIMIT=2
```

Эквивалент без Make:

```bash
LIFE_SIM_PACK_DIR=tests/sandbox/life_sim_packs/<pack_id> \
  .venv/bin/python tests/sandbox/life_sim_provision_pack_wave.py --limit 2
```

---

## Режимы старта

| Mode | Поведение |
|------|-----------|
| `skip` (default) | Не трогает Auth wipe; resume **пропускает** `wave=verified` |
| `wipe-fixture-users` | Удаляет **только** Auth users, чьи email/phone выводятся из **этой** фикстуры; нужен `--confirm-wipe-fixture-users` или `LIFE_SIM_WIPE_FIXTURE_USERS=1` |

**Не** content wipe (stories/issues/threads) — для этого [`life-sim-wipe-node-content`](./life-sim-demo-node-load-manual-ru.md) (REQ11-06).

---

## Где смотреть артефакты

| Артефакт | Путь |
|----------|------|
| Fixture (read-only для status) | `$LIFE_SIM_PACK_DIR/users.json` |
| Wave-state | `$LIFE_SIM_PACK_DIR/waves/<wave_id>/state.json` (gitignored under packs) |
| Secrets | `tests/sandbox/.secrets/life_sim_users_creds_<generation_id>.json` |
| File OTP outbox | Identity `var/sms-outbox` или `LIFE_SIM_FILE_SMS_OUTBOX_DIR` |

Статусы wave: `pending` | `created` | `verified` | `failed`. Checkpoint после каждого шага.

---

## Pace

File-mode default pace **5s** после успешного phone OTP (не обязан 65s Telnyx). Override: `LIFE_SIM_PROVISION_PACE_S`.

---

## Связанные stories

- REQ11-05 foundation: `make life-sim-provision-users`
- REQ11-06 content wipe: `make life-sim-wipe-node-content`
- Backlog: `docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-08-operator-provision-pack-wave.md`
