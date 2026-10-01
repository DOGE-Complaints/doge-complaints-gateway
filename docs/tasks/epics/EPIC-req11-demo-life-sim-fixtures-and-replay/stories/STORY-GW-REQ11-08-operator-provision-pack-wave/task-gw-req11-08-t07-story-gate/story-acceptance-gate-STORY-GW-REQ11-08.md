# Story acceptance gate — STORY-GW-REQ11-08

- **Story:** Operator provision pack wave (CLI + wave-state + RU manual)
- **Package:** `pkg-000106-20261001-gw-req11-08-operator-provision-pack-wave.yaml`
- **Result:** PASS
- **Date:** 2026-10-01T10:31:41Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ1108-01 | PASS | CLI reads pack `users.json`; dry-run/wave never mutate fixture; mtime guard |
| AC-GW-REQ1108-02 | PASS | `life_sim_provision_config.py` fail-closed: `SMS_PROVIDER=file`, `@dogestonia.me`, Identity Auth |
| AC-GW-REQ1108-03 | PASS | `life_sim_wave_store.py` + pack `waves/<id>/state.json`; resume skips `verified` |
| AC-GW-REQ1108-04 | PASS | `--mode skip` default; wipe-fixture-users refuses without confirm (exit 2) |
| AC-GW-REQ1108-05 | PASS | `docs/runtime-docs/manuals/life-sim-provision-pack-wave-manual-ru.md` + load-manual cross-link |
| AC-GW-REQ1108-06 | PASS | Pack-wave entry reuses `provision_one` / lib; secrets under `.secrets/`; offline tests 6 passed |

## Commands (live verification 2026-10-01T10:31:41Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_req11_08_provision_pack_wave.py
# dry-run smoke + wipe refuse (no live Auth wipe this P3)
LIFE_SIM_PACK_DIR=tests/sandbox/life_sim_packs/ls-20260930T0938Z-veerenni-yard-construction \
  .venv/bin/python tests/sandbox/life_sim_provision_pack_wave.py --limit 2 --dry-run --wave-id p3-smoke2
.venv/bin/python tests/sandbox/life_sim_provision_pack_wave.py --limit 1 --mode wipe-fixture-users --dry-run  # exit 2
```

SSOT дат: `guides/builder-artifact-dates.md`
