# Story acceptance gate — STORY-GW-REQ11-10

- **Story:** Operator pack-wave replay жалоб (CLI + wave-state + RU manual)
- **Package:** `pkg-000108-20261001-gw-req11-10-operator-pack-replay-complaints-wave.yaml`
- **Result:** PASS
- **Date:** 2026-10-01T11:35:43Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ1110-01 | PASS | Make/CLI fail-closed without `LIFE_SIM_PACK_DIR`; mtime guard on `stories.json` |
| AC-GW-REQ1110-02 | PASS | `ReplayWaveStore` + offline resume skips `submitted` |
| AC-GW-REQ1110-03 | PASS | `_preflight_missing_creds` + secrets by `fixture_user_id` |
| AC-GW-REQ1110-04 | PASS | `life_sim_replay_pack_wave.py` + Make Present; reuse runner submit |
| AC-GW-REQ1110-05 | PASS | RU manual Present; load-manual pack-wave primary |
| AC-GW-REQ1110-06 | PASS | Offline 8 passed; K1; no invent intake/force-cluster |

## Leftover (documented, not FAIL)

- Live LIMIT=2 / full pack (~1661) submit: Supabase password-grant `Tunnel connection failed: 403 Forbidden` to `SUPABASE_URL`. Re-run when Identity Auth reachable. Wave marks `failed` for those attempts.

## Commands (live verification 2026-10-01T11:35:43Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_req11_10_replay_pack_wave.py
make life-sim-replay-pack-wave  # exit 2 without pack
LIFE_SIM_PACK_DIR=tests/sandbox/life_sim_packs/<id> LIFE_SIM_REPLAY_PACK_WAVE_DRY_RUN=1 make life-sim-replay-pack-wave LIMIT=2
```
