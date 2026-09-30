.PHONY: serve dev simulate simulate-life-sim life-sim-provision-users life-sim-wipe-node-content check-env test test-live

# ─── Local server launch ────────────────────────────────────────────────────
#
# Both targets load .env into the process environment before starting uvicorn.
# Without this, DB_BACKEND defaults to in_memory and no data reaches Supabase.
#
# Usage:
#   make serve          — production-like local run (no reload)
#   make dev            — hot-reload mode for active development
#   make simulate       — run simulation_runner.py against GATEWAY_URL
#   make simulate-life-sim — REQ11-05 profiled life-sim replay (1:1 secrets; see note)
#   make life-sim-provision-users — REQ11-05 provision verified accounts + gitignored secrets
#   make life-sim-wipe-node-content — REQ11-06 wipe stories+derivatives+threads (confirm required)
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

# REQ11-05: wipe DB first, provision secrets (make life-sim-provision-users),
# set DEMO_LIFE_SIM_PROFILE, then confirm wipe. Primary = API+JSON 1:1 Bearer
# (no SPA resident login). Pool M=20 deprecated (LIFE_SIM_USE_POOL_M20=1 emergency).
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

# REQ11-05 provision: Supabase signup + Identity file-OTP → gitignored .secrets/
# Smoke: make life-sim-provision-users LIMIT=2
# Full:  make life-sim-provision-users   (paces ~65s/user for phone rate limits)
life-sim-provision-users:
	.venv/bin/python tests/sandbox/life_sim_provision_users.py \
	  $${LIMIT:+--limit $${LIMIT}} \
	  $${LIFE_SIM_PROVISION_PACE_S:+--pace-s $${LIFE_SIM_PROVISION_PACE_S}} \
	  $${LIFE_SIM_PROVISION_DRY_RUN:+--dry-run}

# REQ11-06 wipe: stories + REQUIRED_READINESS_TABLES derivatives + threads tables.
# Dry-run: LIFE_SIM_WIPE_DRY_RUN=1 make life-sim-wipe-node-content
# Live:    LIFE_SIM_WIPE_CONFIRMED=1 make life-sim-wipe-node-content
# Or:      make life-sim-wipe-node-content CONFIRM_WIPE=1
# Does NOT delete Identity auth.users. No invent wipe HTTP.
life-sim-wipe-node-content:
	@if [ "$${LIFE_SIM_WIPE_DRY_RUN}" = "1" ]; then \
	  .venv/bin/python tests/sandbox/life_sim_wipe_node_content.py --dry-run; \
	elif [ "$${LIFE_SIM_WIPE_CONFIRMED}" = "1" ] || [ "$${CONFIRM_WIPE}" = "1" ]; then \
	  LIFE_SIM_WIPE_CONFIRMED=1 .venv/bin/python tests/sandbox/life_sim_wipe_node_content.py --confirm-wipe; \
	else \
	  .venv/bin/python tests/sandbox/life_sim_wipe_node_content.py; \
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
