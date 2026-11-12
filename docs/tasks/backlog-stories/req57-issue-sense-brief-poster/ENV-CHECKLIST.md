# REQ57 — Gateway env checklist (operator fill before / during stories)

**UTC:** 2026-10-15T10:42:18Z  
**Why:** Dev dialogs cannot read `.env`. Set these on the gateway host / local env **before** P3 so stories can use real names without inventing alternatives.

Peer SSOT: [`handoff-gateway-req13-sense-brief-worker-2026-10-15.md`](../../../../doge-ai-bridge/docs/analysis/handoff-gateway-req13-sense-brief-worker-2026-10-15.md) §6.

---

## Gateway variables (names locked)

| Variable | Required | Example / how to fill | Used by |
|----------|----------|----------------------|---------|
| `AIBRIDGE_BASE_URL` | Yes for nudge | `https://<aibridge-host>` — **HTTPS origin only**, no path, no trailing slash | REQ57-02, 03, 04 |
| `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN` | Yes for nudge | **Same secret** as aibridge `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN` | REQ57-02, 03, 04 |
| `SERVICE_API_TOKEN` | Yes for bind receive | **Already Present** on gateway (`config/schema.py`). Must equal aibridge `GATEWAY_SERVICE_API_TOKEN` | REQ57-01 (bind), 04 (regenerate) |
| `AIBRIDGE_SENSE_BRIEF_NUDGE_ENABLED` | Schema-defaulted (`false`) | Set `true` to enable outbound nudge. **Unset** → ENV_SCHEMA default `false` via `_require_value` (boot OK; nudge disabled). **`false`** → runtime fail-closed (no HTTP, no pretend success; pending may remain). When `true`, missing `AIBRIDGE_BASE_URL` / S2S token → runtime fail-closed. Prefer explicit `=false` in ops `.env` (`example.env`). | REQ57-02+ |

Nudge full URL (derived, not a separate env):  
`{AIBRIDGE_BASE_URL}/v1/worker/sense-brief/accept`

**Fail-closed (REQ57-02, clarified P6 T08 vs code):**  
- Unset/`false` ENABLED → no accept call (not «silent success»).  
- Enabled but missing base URL or S2S token → no accept call; pending may remain.  
- Not the same as boot failure: unset does **not** abort `load_config_from_env` (default applies).

Bind path (gateway serves):  
`POST /v1/issue-sense-brief/bind`

---

## aibridge peer (ops must already have)

| Variable | Role |
|----------|------|
| `AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED=true` | Worker on |
| `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN` | Accept auth (= gateway copy) |
| `GATEWAY_BASE_URL` | HTTPS origin of **this** gateway |
| `GATEWAY_SERVICE_API_TOKEN` | = gateway `SERVICE_API_TOKEN` |
| Model/storage slots | Per aibridge handoff §6 |

---

## Local / CI test doubles

| Setting | Value |
|---------|--------|
| Unit/ASGI | Stub HTTP transport for nudge; POST bind with forged service token in tests |
| Live E2E | Optional ops — not merge gate for backlog scaffold |

---

## Operator action (copy)

```bash
# gateway .env (fill secrets yourself — do not paste production tokens into chat)
AIBRIDGE_BASE_URL=https://YOUR_AIBRIDGE_HOST
AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN=SAME_AS_AIBRIDGE_WORKER_S2S
AIBRIDGE_SENSE_BRIEF_NUDGE_ENABLED=true
# SERVICE_API_TOKEN=...   # must already match aibridge GATEWAY_SERVICE_API_TOKEN
```
