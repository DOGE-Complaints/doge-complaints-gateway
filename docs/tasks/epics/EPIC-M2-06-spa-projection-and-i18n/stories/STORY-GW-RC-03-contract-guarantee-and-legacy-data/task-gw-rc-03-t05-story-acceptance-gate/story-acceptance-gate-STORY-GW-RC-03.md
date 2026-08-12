# Story acceptance gate — STORY-GW-RC-03

- **Story:** Contract guarantee + legacy data hygiene
- **Package:** `pkg-000032-20260529-gw-rc-03-contract-guarantee-and-legacy-data.yaml`
- **Result:** PASS
- **Date:** 2026-05-29

## AC checklist (verbatim from backlog)

| AC | Status | Evidence |
|----|--------|----------|
| Регресс-тест: неполный payload → ответ содержит `id`, `status`, канон `type` | PASS | `test_gw_rc_03_contract_guarantee.py` (T01) |
| Проведён аудит legacy-записей; принято и зафиксировано решение по бэкфиллу | PASS | `legacy-audit-five-records.md` — decision **defer** (T02) |
| (Если решено) legacy-issue получили недостающие поля | N/A | T03 skipped — defer per D-RC-3 |
| Тест-суит без регрессий | PASS | `508 passed in 15.74s` — live run 2026-05-29 |
| `builder_resolve_queue.py --verify` ok 5 paths | PASS | live run 2026-05-29 |

## Commands (live verification 2026-05-29)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_03_contract_guarantee.py -q
cd doge-complaints-gateway && python3 -m pytest --ignore=tests/integration --ignore=tests/smoke -q
```
