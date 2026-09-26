# acceptance-verification — task-gw-thr-01-t01

- **Result:** PASS
- **Date:** 2026-09-21T20:29:51Z
- **Evidence:** `src/core/schema/shell_capabilities.py`; `SchemaContext.shell_capabilities` in `contracts.py`; wired from `resolver.load_pack`. Capability ids = REQ7 vocabulary; on-disk home = sidecar (not pack.json product keys).

```text
rg -n 'shell_capabilities|ShellCapabilitiesBlock' doge-complaints-gateway/src/core/schema
```
