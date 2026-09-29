#!/usr/bin/env bash
# GW-REQ11-04 T04 — wait for clustering before threads seed handoff.
# Docs-only helper: uses existing CLUSTER_* knobs; does not invent cluster APIs.
set -euo pipefail
MIN="${CLUSTER_MIN_SIZE:-8}"
ENABLED="${CLUSTER_CRON_ENABLED:-true}"
INTERVAL="${CLUSTER_CRON_INTERVAL_S:-60}"
echo "life-sim clustering wait (K3: board cards follow clustering)"
echo "  CLUSTER_MIN_SIZE=${MIN}"
echo "  CLUSTER_CRON_ENABLED=${ENABLED}"
echo "  CLUSTER_CRON_INTERVAL_S=${INTERVAL}"
echo "Sleeping 2× interval before threads seed handoff…"
sleep "${INTERVAL}"
sleep "${INTERVAL}"
echo "Handoff: sibling threads social seed (out of scope for gateway REQ11-04)."
