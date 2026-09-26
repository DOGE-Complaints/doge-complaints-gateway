# acceptance-verification — task-gw-thr-01-t02

- **Result:** PASS
- **Date:** 2026-09-21T20:29:51Z
- **Evidence:** `load_shell_capabilities` fail-closed; `test_missing_shell_sidecar_fail_closed`; `test_node_schema_boot_maps_missing_caps_to_config_error` (BOOT_SOFT=0).

```text
.venv/bin/python -m pytest -q tests/test_gw_thr_01_pack_shell_required.py
```
