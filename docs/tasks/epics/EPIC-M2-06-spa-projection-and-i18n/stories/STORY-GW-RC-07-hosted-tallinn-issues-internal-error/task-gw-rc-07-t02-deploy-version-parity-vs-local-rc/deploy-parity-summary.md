# Deploy parity summary — STORY-GW-RC-07 T02

**Date:** 2026-07-10  
**Corrected (audit G1, T06):** 2026-07-10

## Local HEAD

```
8c70624 docs(GW-DRAFT-05): add backlog story for dual stash vs submit intake
87fc272 fix(GW-DRAFT): accept story-draft stash without submitter
543a38b fix(GW-RC-04): add missing columnar_storage module for deploy startup
```

Local `HEAD`: `8c706244ff5d51a238326491149e8efe576c835a`

## Hosted `/ready` (2026-07-10)

```json
{
  "data": {
    "status": "ready",
    "db": {
      "backend": "supabase",
      "ready": true,
      "checks": {
        "connectivity": true,
        "schema": true,
        "columns": true,
        "columns_geo_admin": true,
        "columns_v2": true,
        "policy_probe": true
      }
    }
  },
  "trace_id": "9d39281b-9964-4b8a-9bf4-98c5f58f60b6"
}
```

## RC-04→06 feature parity assessment (2026-07-10)

| Signal | Hosted | Local expectation |
|--------|--------|-------------------|
| `columns_v2` check | `true` | RC-04 **DB column** readiness ([`dependencies.py:79`](../../../../../../../src/core/api/dependencies.py)) — distinct from Python module presence |
| `columns_geo_admin` | `true` | RC-04 geo admin columns |
| List read with 8+ INCIDENT rows | **PASS** (9 cards) | [`read_filters.py`](../../../../../../../src/core/projection/read_filters.py) + columnar assembly |
| INCIDENT type on read | PASS | [`enums.py:19`](../../../../../../../src/core/projection/enums.py) |

## CF-B root-cause assessment (corrected per audit G1)

| Event | Date | Source |
|-------|------|--------|
| CF-B observed (`INTERNAL_ERROR` on list) | **2026-06-22** | [`audit-gw-seed-02`](../../../../../../analysis/audit-gw-seed-02-dataset-expansion-for-clustering-2026-06-22.md) §CF-B |
| `columnar_storage` import introduced in `db_supabase.py` | **2026-07-03** | `e832302` (GW-DRAFT-01) |
| `columnar_storage.py` file created | **2026-07-08** | `543a38b` (body: GW-DRAFT-01 Railway startup) |

**Conclusion on CF-B 2026-06-22:** missing `columnar_storage.py` **cannot** explain June INTERNAL_ERROR — import did not exist until July. **Causa undetermined**; prod **self-resolved** before P3 re-verify 2026-07-10 (9 cards, no error). Candidate (unproven without June hosted schema snapshot): RC-04 **DB column** drift on Supabase, not missing Python module.

**Separate July incident:** missing-module packaging drift (GW-DRAFT-01 → `543a38b`) — distinct from original CF-B; closed by deploy catch-up before 2026-07-10 verify.

## Railway build SHA

Not exposed via public API. Parity inferred from:
- `/ready` column checks (RC-04+ DB schema)
- Successful multi-row INCIDENT list (behavioral parity with local HEAD)
- No `INTERNAL_ERROR` on 2026-07-10 live curl

## Conclusion

Hosted read-path **operational** as of 2026-07-10 (9 cards). Historical CF-B June cause **not established**; per-row probe ruled out poisoned rows on current prod.
