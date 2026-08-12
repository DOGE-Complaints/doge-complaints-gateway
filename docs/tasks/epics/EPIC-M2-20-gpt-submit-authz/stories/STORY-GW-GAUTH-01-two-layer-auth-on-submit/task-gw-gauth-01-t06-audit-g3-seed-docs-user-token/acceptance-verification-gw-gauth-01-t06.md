# Acceptance — TASK-GW-GAUTH-01-T06

- **Result:** PASS
- **Date:** 2026-06-25

| AC (audit G3) | Status | Evidence |
|---------------|--------|----------|
| `simulation-runner-manual.md` documents `GATEWAY_USER_TOKEN` + `X-User-Token` | PASS | env-таблица + строка `GATEWAY_USER_TOKEN` (→ `X-User-Token`, дефолт = `GATEWAY_API_TOKEN`, [`simulation_runner.py:172`](../../../../../../../tests/simulation_runner.py#L172)); пример `.env.test`; 401-троублшутинг упоминает оба слоя. |
| `seed-demo-data-runbook-ru.md` cross-ref user-token layer | PASS | предусловие «Двухслойная auth (GW-GAUTH-01)» + `GATEWAY_USER_TOKEN` в Шаг-1; ссылка на runner-manual SSOT (без дублирования). |
| GAUTH-01 stub vs GAUTH-02 real token noted | PASS | оба мануала: дефолт проходит пока user-слой = заглушка присутствия; после реального introspection (GW-GAUTH-02) нужен настоящий пользовательский OAuth-токен, иначе 401. |

**Verification:**
```
rg -n 'GATEWAY_USER_TOKEN|X-User-Token' docs/runtime-docs/testing/simulation-runner-manual.md docs/runtime-docs/manuals/seed-demo-data-runbook-ru.md
# → matches in both files
```
Закрывает audit G3 ([`audit-gw-gauth-01-...md §3 G3`](../../../../../../analysis/audit-gw-gauth-01-two-layer-auth-on-submit-2026-06-25.md)).
