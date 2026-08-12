# STORY-GW-ES-08 — Emerging L2 label-fold perf (evidence-gated)

## Meta
- **Key:** `STORY-GW-ES-08-emerging-label-fold-perf`
- **Пакет:** [`early-signal-pre-cluster/`](./INDEX.md)
- **Status:** ⏸ Deferred — **evidence-gated**; activate when hosted scale evidence exists
- **Приоритет:** ⚪ LOW — perf successor; ES-03 DoD = in-memory fold + per-story `list_by_story`
- **Тип:** implement (repository / batch label fold / SQL path)
- **Gaps:** [audit GW-ES-03 **G2**](../../../analysis/audit-gw-es-03-public-emerging-l2-read-2026-08-10.md); family Pulse [ES-06](./STORY-GW-ES-06-network-pulse-sql-count-perf.md)
- **Зависит от:** [GW-ES-03](./STORY-GW-ES-03-public-emerging-l2-read.md) Done; hosted latency/size evidence
- **Не reopen:** ES-03 first-DoD in-memory fold as incorrect

## Зачем простыми словами

Emerging сейчас делает `list_stories` + N× `list_by_story` + in-memory top-N. На большом hosted объёме это может стать bottleneck. Batch/`count` (или RPC) — follow-up **только** при evidence, не silent rewrite ES-03.

## Что наблюдаю сейчас (verified)

| Fact | Ref |
|------|-----|
| In-memory fold + per-story labels | [`emerging_signals.py`](../../../../src/core/application/emerging_signals.py) |
| Explicit out-of-DoD | ES-03 audit §G2; REQ-50 / open Q family |
| Pulse twin Deferred | [ES-06](./STORY-GW-ES-06-network-pulse-sql-count-perf.md) |

## Требование / целевое состояние (при активации)

1. Evidence: latency / row counts на hosted (или load test) justifying batch/SQL path.
2. Repository batch or `count` for label frequencies after published-exclusion; preserve public disposition + Topic≠Issue.
3. Same public contract `GET /tallinn/emerging-signals` payload shape (or versioned bump with REQ).
4. Tests + honesty notes if sampling/limits change.

## Acceptance Criteria (при активации)

- [ ] Documented evidence gate met (or explicit N/A close)
- [ ] Batch/SQL path + parity tests vs fold on fixture set
- [ ] Published-exclusion + public disposition preserved
- [ ] No silent change of public payload without REQ update

## Границы

- **In scope:** perf successor for Emerging aggregates.
- **Вне scope:** handler envelope (ES-07); Pulse SQL (ES-06); spa layout; inventing thresholds.

## Условие реактивации

- Hosted evidence of Emerging latency/scale pain **или** explicit ops/product request.
- Иначе остаётся Deferred; ES-03 in-memory = acceptable MVP.
