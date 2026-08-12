# Acceptance verification — GW-TAX-03 T03

- **Task:** task-gw-tax-03-t03-rls-grant-parity-bootstrap
- **Result:** PASS
- **Date:** 2026-08-07T09:59:37Z

## Evidence

- Same migration file append:
  - `ALTER TABLE story_labels ENABLE ROW LEVEL SECURITY`
  - policy `story_labels_service_role_all` FOR ALL TO `service_role`
  - `GRANT ALL … TO service_role`; `GRANT SELECT … TO anon, authenticated`
- Parity refs: bootstrap policy `:325-331`; proposed DRAFT-07 SQL
- No hosted Public Node re-apply
