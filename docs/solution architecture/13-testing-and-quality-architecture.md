# 13. Testing & Quality Architecture

## Test pyramid
- Unit: domain/services/validators.
- Integration: db adapters + external stubs.
- Contract: SPA projection compatibility.
- E2E (demo): intake -> cluster -> issue projection -> evidence.

## Minimal mandatory suite for demo
1. Story intake validation + persistence.
2. Profile enrichment correctness.
3. Multi-membership clustering behavior.
4. Candidate promotion gate checks.
5. SPA projection contract test.
6. Evidence lineage reversibility test.
7. Geo resolver cache + fallback test.

## Quality gates
- lints/type checks mandatory;
- no critical security findings;
- projection contract tests 100%;
- acceptance-verification doc per milestone.

## Pilot expansion
- add full sign/callback/broadcast e2e;
- add replay/idempotency tests;
- add load profile for clustering and projection.
