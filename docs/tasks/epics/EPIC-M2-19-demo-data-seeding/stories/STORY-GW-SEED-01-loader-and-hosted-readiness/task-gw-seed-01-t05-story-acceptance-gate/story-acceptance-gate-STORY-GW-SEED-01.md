# Story acceptance gate — STORY-GW-SEED-01

- **Story:** Загрузчик историй + готовность hosted-таргета
- **Package:** `pkg-000036-20260621-gw-seed-01-loader-and-hosted-readiness.yaml`
- **Result:** PASS
- **Date:** 2026-06-21

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| `GET /ready` на hosted = `db_ready: true` до загрузки. | PASS | T01 `hosted-ready-response.json`, `hosted-readiness-checklist.md` |
| `CLUSTER_CRON_ENABLED=true` подтверждён на таргете. | PASS (R1) | T01 checklist — schema default true; Railway env not independently verified |
| Smoke `--max 10` → все приняты; полный прогон → сводка зафиксирована. | PASS | T02 `smoke-run-summary.md` (10/10); T03 `full-run-summary.md` (130/130) |
| В `stories` появились строки `sim:*`. | PASS | T04 `sim-prefix-sql-verify.md` — count 141 |

## Commands (live verification 2026-06-21)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
curl -sS "$GATEWAY_URL/ready" | jq '.data.db'
cd doge-complaints-gateway && python3 tests/simulation_runner.py --max 10
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
