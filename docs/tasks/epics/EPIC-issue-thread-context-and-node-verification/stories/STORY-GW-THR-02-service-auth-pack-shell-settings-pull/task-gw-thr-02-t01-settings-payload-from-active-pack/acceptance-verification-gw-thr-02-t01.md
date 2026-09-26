# acceptance-verification — GW-THR-02 T01

- **Date:** 2026-09-21T20:48:13Z
- **Package:** pkg-000094 (immutable)
- **Result:** PASS
- **Evidence:** `src/core/schema/shell_settings.py` maps `ShellCapabilitiesBlock` → `pack_shell_settings` DTO from active NODE_SCHEMA only; fail-closed via `resolve_pack`.
