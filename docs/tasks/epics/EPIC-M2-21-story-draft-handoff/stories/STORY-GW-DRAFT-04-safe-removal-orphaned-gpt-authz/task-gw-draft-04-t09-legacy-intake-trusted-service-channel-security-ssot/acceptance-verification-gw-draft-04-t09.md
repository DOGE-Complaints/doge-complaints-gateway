# Acceptance verification — task-gw-draft-04-t09-legacy-intake-trusted-service-channel-security-ssot

- **Task:** T09 legacy intake trusted-service channel security SSOT
- **Status:** PASS
- **Date:** 2026-07-03

## Checklist

- [x] Trust model documented: `/intake/stories` + `/tallinn/issues` = service-only trusted channel
- [x] Product submit pointer: browser `/story-drafts/{id}/submit` only
- [x] `security-env-api-access.md` — no stale OAuth introspection contrast
- [x] `server-env-quickstart.md` — no `IDENTITY_INTROSPECT_*` / two-layer intake auth
- [x] Audit G1 traceability noted
- [x] `rg 'IDENTITY_INTROSPECT|X-User-Token|require_user_token|IdentityIntrospection'` → 0 in target files
