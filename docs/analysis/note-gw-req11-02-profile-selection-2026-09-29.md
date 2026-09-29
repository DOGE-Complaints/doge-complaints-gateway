# Note — GW-REQ11-02 named profiles selection (local + Uus Veerenni)

| Field | Value |
|-------|--------|
| **utc** | `2026-09-29T14:00:57Z` (P3 live) |
| **Story** | STORY-GW-REQ11-02 · AC-GW-REQ1102-01…03 |
| **Package** | pkg-000101 |
| **Method** | disk facts only; env refs; no invent public APIs; no replay |

## Verdict

Operators select a **named profile** for future profiled replay (REQ11-03) via env `DEMO_LIFE_SIM_PROFILE` or an explicit `load_profile(id)` / `select_profile(id)` call. Profile JSON holds **URL defaults / documented example hosts** and **token env names** — never secret values in git.

## Profiles on disk

| Id | Path | Role |
|----|------|------|
| `local` | [`tests/sandbox/profiles/local.json`](../../tests/sandbox/profiles/local.json) | local-five defaults 8100/8000/8001/8080/5173; `GATEWAY_API_TOKEN` env ref |
| `uus-veerenni` | [`tests/sandbox/profiles/uus-veerenni.json`](../../tests/sandbox/profiles/uus-veerenni.json) | deploy; `GATEWAY_URL` + `GATEWAY_API_TOKEN` env refs; documented example host from `.env.test.example` |
| registry | [`tests/sandbox/profiles/index.json`](../../tests/sandbox/profiles/index.json) | selectable ids + default=`local` |
| loader | [`tests/sandbox/profiles/demo_life_sim_profiles.py`](../../tests/sandbox/profiles/demo_life_sim_profiles.py) | `list_profile_ids` / `load_profile` / `select_profile` |

## How to select (operator)

1. Copy `.env.test.example` → `.env.test` (gitignored). Fill token/password values **only** in `.env.test` / ops env.
2. Choose profile:
   - Local five-serve: `export DEMO_LIFE_SIM_PROFILE=local` (default if unset).
   - Uus Veerenni deploy: `export DEMO_LIFE_SIM_PROFILE=uus-veerenni` and set `GATEWAY_URL` (example pattern: `https://uus-veerenni-civic-gateway.dogestonia.me`) + `GATEWAY_API_TOKEN`.
3. Programmatic: `from demo_life_sim_profiles import select_profile; select_profile("local")`.
4. Today's `make simulate` / `tests/simulation_runner.py` still reads `GATEWAY_URL` + `GATEWAY_API_TOKEN` directly — **replay loop wiring is REQ11-03**. This story only provides selectable profile artifacts + selection handoff.

## Runtime PORT overrides (`local`)

`local-five-serve-and-health.sh` reads each service `.env` `PORT=` when present; profile defaults are the documented operator lock. Overriding PORT in a service `.env` at runtime is allowed and does not require editing the profile file.

## Secrets policy (AC-03)

| In git (profiles) | In env / `.env.test` only |
|-------------------|---------------------------|
| `*_env` names (`GATEWAY_API_TOKEN`, …) | Actual token / password / anon key values |
| Public/local URLs & documented example host | — |

## Out of scope here

- Fixture JSON (REQ11-01).
- Replay / multi-submitter loop (REQ11-03).
- Literal secrets; inventing undocumented public HTTP APIs.
