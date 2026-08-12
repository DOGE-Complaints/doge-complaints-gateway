# Acceptance verification — TASK-M2-06-06-T06

- **Task:** Routes + CORS
- **Result:** PASS
- **Evidence:** `asgi_app.py` — GET/POST/OPTIONS `/tallinn/issues`; `PUBLIC_ROUTES`; CORSMiddleware (AC-9)
- **Commands:** `python3 -m pytest tests/test_req24_tallinn_issues_read_api.py::test_req24_ac9_cors_options -q`
