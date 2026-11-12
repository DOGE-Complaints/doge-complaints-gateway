# Run summary — GW-REQ11-06 P6 audit follow-up

| Field | Value |
|-------|--------|
| **utc** | `2026-09-30T08:02:52Z` |
| **Story** | STORY-GW-REQ11-06-wipe-node-content-stories-derivatives |
| **Package** | pkg-000105 (immutable · unchanged) |
| **activation** | `run_mode=gw_req11_06_audit_followup` |
| **Branch** | `dev` (no push) |
| **Result** | T07 G1 CLOSED · T08 G2 CLOSED · G3 WAIVED |

## What closed

- **T07 / G1:** backlog §Verified + Code touchpoints As-of-Done vs Historical; T01 Code Facts Present
- **T08 / G2:** manual §8 Wipe inventory → Present/Done
- **G3:** WAIVED operator — §«Актуальная точка» untouched

## Verification

```text
--verify ok 6 (pkg-000105)
--verify --check-dates → ok
rg Absent/As-of-Done/Historical on backlog + T01 → Historical only for Absent
rg §8 Wipe → Present Done (no «ожидаем»)
current.yaml stays pkg-000105
```

## Next

Operator **P7** / optional **P8** commits. Empty OPEN gap-list = yes (G1/G2 CLOSED; G3 WAIVED).
