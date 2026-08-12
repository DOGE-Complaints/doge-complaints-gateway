# task-gw-rc-04-t11

## Meta
- **Story:** [STORY-GW-RC-04](../STORY-GW-RC-04-columnar-model-migration.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** — (audit override, вне pkg-000033)
- **Skill declared:** python-pro
- **Depends on:** T01–T09 (columnar migration Done)
- **Wave:** audit override (`run_mode=gw_rc_04_audit_followup`)
- **Decision Ref:** [`audit-gw-rc-04-columnar-model-migration-2026-06-20.md`](../../../../../../analysis/audit-gw-rc-04-columnar-model-migration-2026-06-20.md) §3 G2

## Purpose
Закрыть audit G2: добавить выделенный RC-04 тест columnar write→read round-trip и legacy `legacy_payload_json`-fallback. RC-01/02/03 contract-тесты доказывают неизменность формы, но не покрывают columnar storage path напрямую.

## Code Facts
- Columnar converter — [`columnar_storage.py`](../../../../../../../src/core/projection/columnar_storage.py): `payload_to_storage_fields`, `assemble_public_issue_from_storage_row`
- Legacy fallback — [`columnar_storage.py:113-119`](../../../../../../../src/core/projection/columnar_storage.py#L113-L119): `legacy_payload_json` param
- Stores use columnar — [`repositories.py`](../../../../../../../src/core/infrastructure/repositories.py), [`db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- No `test_gw_rc_04_*.py` — verified absent in `tests/`

## Acceptance / DoD
- (P0) `tests/test_gw_rc_04_columnar_storage.py`: round-trip `save_projection` → `get_projection` (InMemory + SQLite) with full contract fields (i18n, labels, geo, optional scalars)
- (P0) Unit test: `assemble_public_issue_from_storage_row` with empty columnar row + `legacy_payload_json` dict (simulates pre-migration row; no live `payload_json` column after T07)
- (P1) Unit suite без регрессий
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `tests/test_gw_rc_04_columnar_storage.py` (new)

## Out of scope
- Новый pkg / смена [`gateway-active-package.current.yaml`](../../../../../../gateway-active-package.current.yaml)
- Prod-код changes (unless test helpers require minimal export)
- G1 readiness (T10)
- Duplicating RC-01/02/03 contract suite

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_04_columnar_storage.py -q
cd doge-complaints-gateway && python3 -m pytest --ignore=tests/integration --ignore=tests/smoke -q
```
