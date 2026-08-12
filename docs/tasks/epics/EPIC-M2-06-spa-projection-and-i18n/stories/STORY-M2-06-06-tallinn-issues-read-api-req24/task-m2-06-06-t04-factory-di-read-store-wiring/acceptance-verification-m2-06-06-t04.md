# Acceptance verification — TASK-M2-06-06-T04

- **Task:** Factory + DI wiring
- **Result:** PASS
- **Evidence:** `service_factory.py`, `factory.py`, `dependencies.py` — `issue_projection_read_store`, `issue_create_service` on `ApiDependencies`
- **Commands:** `python3 -m pytest tests/test_api_security_and_ops.py -q -k health`
