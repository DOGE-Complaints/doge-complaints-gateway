# Acceptance verification — TASK-M2-02-12-T10

- **Task:** geo lookup length-DESC collision tests.
- **Result:** PASS
- **Evidence:** `tests/test_geo_providers_estonia.py` (Põhja-Tallinn / RU alias vs plain Tallinn).
- **Commands:** `python3 -m pytest -q tests/test_geo_providers_estonia.py`
