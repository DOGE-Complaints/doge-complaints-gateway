# Fix summary — STORY-GW-RC-07 T04

**Date:** 2026-07-10  
**Corrected (audit G1, T06):** 2026-07-10

## Root cause (corrected per audit G1)

### CF-B 2026-06-22 (original story scope)

- **Operational:** hosted `GET /tallinn/issues` returned `INTERNAL_ERROR` while `/ready` green and 8 PUBLISHED rows existed (audit CF-B).
- **Isolation (T03):** no poisoned row among 9 PUBLISHED issues on 2026-07-10 probe.
- **Diagnosis:** **causa undetermined** — prod self-resolved before P3 fix session; no code/data fix applied in P3.
- **Retracted attribution:** missing `columnar_storage.py` is **not** the June root cause (import introduced `e832302` 2026-07-03; file `543a38b` 2026-07-08 — both **after** CF-B date).

### July missing-module incident (separate, GW-DRAFT-01)

- Lazy import of `core.projection.columnar_storage` in [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) (`list_projections` L737, `get_projection` L782, etc.) can fail at **runtime** if deploy artifact omits the module — `/ready` may still pass (DB column checks only).
- Resolved on prod before 2026-07-10 verify via deploy including `543a38b` (commit body attributes fix to GW-DRAFT-01, not RC-04).

## Fix applied (P3 session)

| Action | Status |
|--------|--------|
| Code fix for June CF-B | **N/A** — prod already healthy at P3 |
| Data repair | **Not required** (9/9 rows read OK) |
| New `src/core/` in P3 | **None** |
| Regression guard for packaging drift | **Deferred** → audit G2 / T07 |

## Verification

```bash
curl -sS "https://dogestonia-tallinn.up.railway.app/tallinn/issues"  # 9 issues, no INTERNAL_ERROR
cd doge-complaints-gateway && python3 -m pytest -q tests/test_req24_tallinn_issues_read_api.py tests/test_gw_rc_03_contract_guarantee.py  # 26 passed
```

## Parent AC #2 (fix leg) — operational note

Board API restored on hosted (verified 2026-07-10). Causal link «P3 fix → recovery» **not demonstrated** — recovery predated fix session. Diagnosis corrected in T06; packaging guard added in T07.
