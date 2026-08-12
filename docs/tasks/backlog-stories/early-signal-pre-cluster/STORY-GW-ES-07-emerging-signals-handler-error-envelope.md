# STORY-GW-ES-07 — Emerging Signals handler error-envelope parity

## Meta
- **Key:** `STORY-GW-ES-07-emerging-signals-handler-error-envelope`
- **Пакет:** [`early-signal-pre-cluster/`](./INDEX.md)
- **Status:** ⚪ Todo (draft — optional PA.3 refine; not in active pkg)
- **Приоритет:** ⚪ LOW — resilience hygiene; не MVP Emerging AC
- **Тип:** implement (handler wrap only)
- **Gaps:** [audit GW-ES-03 **G1**](../../../analysis/audit-gw-es-03-public-emerging-l2-read-2026-08-10.md)
- **Зависит от:** [GW-ES-03](./STORY-GW-ES-03-public-emerging-l2-read.md) Done pkg-000060; soft twin [GW-ES-05](./STORY-GW-ES-05-network-pulse-handler-error-envelope.md)
- **Не reopen:** ES-03 product AC/DoD; Issues L3 / Pulse L1 semantics

## Зачем простыми словами

`GET /tallinn/emerging-signals` при исключении из store отдаёт default FastAPI 500, а Issues list — `build_error_envelope`. Нужна parity try/except вокруг `build_emerging` (как ES-05 для Pulse).

## Что наблюдаю сейчас (verified)

| Fact | Ref |
|------|-----|
| Emerging handler без try/except | [`handlers.py`](../../../../src/core/api/handlers.py) `handle_emerging_signals` |
| Issues list с envelope | same file `handle_tallinn_issues_list` |
| Pulse twin draft | [ES-05](./STORY-GW-ES-05-network-pulse-handler-error-envelope.md) |
| Audit G1 | [`audit-gw-es-03-…§G1`](../../../analysis/audit-gw-es-03-public-emerging-l2-read-2026-08-10.md) — out-of-DoD ES-03 |

## Требование / целевое состояние

1. Обернуть `dependencies.emerging_signals_service.build_emerging(...)` в try/except по образцу Issues list / ES-05 Pulse.
2. На exception → `build_error_envelope` + HTTP 500 (тот же shape, что public Issues).
3. Тест: mock raise → envelope keys / status, без PII в body.
4. Не менять success payload / PUBLIC_ROUTES / MVP L2 rule.

## Acceptance Criteria

- [ ] `handle_emerging_signals` try/except + `build_error_envelope` parity с Issues list
- [ ] Regression: happy-path Emerging + Issues list (+ Pulse if touched) green
- [ ] Unit/HTTP test на failure path
- [ ] ES-03 AC не reopen

## Границы

- **In scope:** handler resilience only.
- **Вне scope:** SQL/N+1 fold (→ ES-08); story SSOT (audit T08–T10); spa-15; Pulse envelope (→ ES-05).
