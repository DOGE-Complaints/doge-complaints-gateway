# STORY-GW-ES-05 — Network Pulse handler error-envelope parity

## Meta
- **Key:** `STORY-GW-ES-05-network-pulse-handler-error-envelope`
- **Пакет:** [`early-signal-pre-cluster/`](./INDEX.md)
- **Status:** ⚪ Todo (draft — optional PA.3 refine; not in active pkg)
- **Приоритет:** ⚪ LOW — resilience hygiene; не MVP Pulse AC
- **Тип:** implement (handler wrap only)
- **Gaps:** [audit GW-ES-02 **G2**](../../../analysis/audit-gw-es-02-public-network-pulse-l1-aggregates-2026-08-10.md)
- **Зависит от:** [GW-ES-02](./STORY-GW-ES-02-public-network-pulse-l1-aggregates.md) Done pkg-000059
- **Не reopen:** ES-02 product AC/DoD; Issues L3 semantics

## Зачем простыми словами

`GET /tallinn/network-pulse` при исключении из store отдаёт default FastAPI 500, а Issues list — `build_error_envelope`. Нужна parity try/except вокруг `build_pulse` для предсказуемого error envelope.

## Что наблюдаю сейчас (verified)

| Fact | Ref |
|------|-----|
| Pulse handler без try/except | [`handlers.py`](../../../../src/core/api/handlers.py) `handle_network_pulse` |
| Issues list с envelope | same file `handle_tallinn_issues_list` |
| Audit G2 | [`audit-gw-es-02-…§G2`](../../../analysis/audit-gw-es-02-public-network-pulse-l1-aggregates-2026-08-10.md) — out-of-DoD ES-02 |

## Требование / целевое состояние

1. Обернуть `dependencies.network_pulse_service.build_pulse(...)` в try/except по образцу Issues list.
2. На exception → `build_error_envelope` + HTTP 500 (тот же shape, что public Issues).
3. Тест: mock store raise → envelope keys / status, без PII в body.
4. Не менять success payload / PUBLIC_ROUTES / Pulse dims.

## Acceptance Criteria

- [ ] `handle_network_pulse` try/except + `build_error_envelope` parity с Issues list
- [ ] Regression: happy-path Pulse + Issues list green
- [ ] Unit/HTTP test на failure path
- [ ] ES-02 AC не reopen

## Границы

- **In scope:** handler resilience only.
- **Вне scope:** SQL count (→ ES-06); OpenAPI tag / story SSOT (audit T08–T10); spa-15; Emerging L2.
