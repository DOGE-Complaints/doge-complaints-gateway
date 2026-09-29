.PHONY: serve dev simulate simulate-life-sim check-env test test-live

# ─── Local server launch ────────────────────────────────────────────────────
#
# Both targets load .env into the process environment before starting uvicorn.
# Without this, DB_BACKEND defaults to in_memory and no data reaches Supabase.
#
# Usage:
#   make serve          — production-like local run (no reload)
#   make dev            — hot-reload mode for active development
#   make simulate       — run simulation_runner.py against GATEWAY_URL
#   make simulate-life-sim — REQ11-03 profiled life-sim replay (pool M=20; see note)
#   make check-env      — print which DB backend and Supabase URL the server will use
#   make test           — offline pytest (excludes live_integration marker)
#   make test-live      — live_integration-marked pytest suite only
#
serve:
	set -a && . ./.env && set +a && \
	.venv/bin/python -m uvicorn --app-dir src core.api.asgi_app:app \
	  --host 127.0.0.1 --port $${PORT:-8000}

dev:
	set -a && . ./.env && set +a && \
	.venv/bin/python -m uvicorn --app-dir src core.api.asgi_app:app \
	  --host 127.0.0.1 --port $${PORT:-8000} --reload --reload-dir src

# ─── Simulation runner ──────────────────────────────────────────────────────
# simulation_runner.py loads .env and .env.test internally via _load_env().
# No shell-level export needed here; GATEWAY_URL / GATEWAY_API_TOKEN come
# from .env.test (copy example.env.test → .env.test and configure).

simulate:
	.venv/bin/python tests/simulation_runner.py

# REQ11-03: wipe DB first, set LIFE_SIM_POOL_00..19_* + DEMO_LIFE_SIM_PROFILE,
# then confirm wipe. Primary path = API+JSON (no SPA resident login).
# Offline contract: LIFE_SIM_DRY_RUN=1 make simulate-life-sim
simulate-life-sim:
	@if [ "$${LIFE_SIM_DRY_RUN}" = "1" ]; then \
	  .venv/bin/python tests/simulation_runner.py --life-sim --wipe-confirmed --dry-run \
	    $${DEMO_LIFE_SIM_PROFILE:+--profile $${DEMO_LIFE_SIM_PROFILE}} \
	    $${SIMULATION_MAX_STORIES:+--max $${SIMULATION_MAX_STORIES}}; \
	else \
	  .venv/bin/python tests/simulation_runner.py --life-sim --wipe-confirmed \
	    $${DEMO_LIFE_SIM_PROFILE:+--profile $${DEMO_LIFE_SIM_PROFILE}} \
	    $${SIMULATION_MAX_STORIES:+--max $${SIMULATION_MAX_STORIES}}; \
	fi

# ─── Diagnostics ────────────────────────────────────────────────────────────
# Shows the effective DB_BACKEND and Supabase URL that the server will see
# when launched via make serve / make dev.

check-env:
	@set -a && . ./.env && set +a && \
	echo "DB_BACKEND     = $${DB_BACKEND:-<not set, defaults to in_memory>}" && \
	echo "SUPABASE_URL   = $${SUPABASE_URL:-<not set>}" && \
	echo "APP_PROFILE    = $${APP_PROFILE:-demo}" && \
	echo "CLUSTER_ACTIVE_LENSES  = $${CLUSTER_ACTIVE_LENSES:-<default>}" && \
	echo "CLUSTER_PRIMARY_LENS   = $${CLUSTER_PRIMARY_LENS:-<default: civic_domain_micro>}"

# ─── Test rituals (REQ9 G7 / lock C) ────────────────────────────────────────
# Offline ≠ hosted/Railway verify. Marker `live_integration` is declared in
# pyproject.toml — do not invent new markers here.

test:
	.venv/bin/python -m pytest -q -m "not live_integration"

test-live:
	.venv/bin/python -m pytest -q -m live_integration
