# STORY-GW-ES-06 — Network Pulse SQL / count perf (evidence-gated)

## Meta
- **Key:** `STORY-GW-ES-06-network-pulse-sql-count-perf`
- **Пакет:** [`early-signal-pre-cluster/`](./INDEX.md)
- **Status:** ⏸ Deferred — **evidence-gated** (open Q5); activate when hosted scale evidence exists
- **Приоритет:** ⚪ LOW — perf successor; ES-02 DoD = in-memory fold
- **Тип:** implement (repository / SQL count path)
- **Gaps:** [audit GW-ES-02 **G3**](../../../analysis/audit-gw-es-02-public-network-pulse-l1-aggregates-2026-08-10.md); REQ-48 / REQ-49 open Q5
- **Зависит от:** [GW-ES-02](./STORY-GW-ES-02-public-network-pulse-l1-aggregates.md) Done; hosted latency/size evidence
- **Не reopen:** ES-02 first-DoD in-memory fold as incorrect

## Зачем простыми словами

Pulse сейчас делает `list_stories` + in-memory fold. На большом hosted объёме это может стать bottleneck. SQL/`count` (или RPC) — follow-up **только** при evidence, не silent rewrite ES-02.

## Что наблюдаю сейчас (verified)

| Fact | Ref |
|------|-----|
| In-memory fold | [`network_pulse.py`](../../../../src/core/application/network_pulse.py) |
| Explicit out-of-DoD | ES-02 backlog / REQ-49 open Q5; audit §G3 |
| Stories list path | [`db_supabase.py`](../../../../src/core/infrastructure/db_supabase.py) `list_stories` |

## Требование / целевое состояние (при активации)

1. Evidence: latency / row counts на hosted (или load test) justifying SQL path.
2. Repository/`count` (or equivalent) for dims that dominate cost; preserve non-PII + public disposition for topics.
3. Same public contract `GET /tallinn/network-pulse` payload shape (or versioned bump with REQ).
4. Tests + honesty notes if sampling/limits change.

## Acceptance Criteria (при активации)

- [ ] Documented evidence gate met (or explicit N/A close)
- [ ] SQL/count path + parity tests vs fold on fixture set
- [ ] Public disposition / Topic≠Issue preserved
- [ ] No silent change of public payload without REQ update

## Границы

- **In scope:** perf successor for Pulse aggregates.
- **Вне scope:** handler envelope (ES-05); Emerging L2; spa layout; inventing thresholds.

## Условие реактивации

- Hosted evidence of Pulse latency/scale pain **или** explicit ops/product request.
- Иначе остаётся Deferred; ES-02 in-memory = acceptable MVP.
