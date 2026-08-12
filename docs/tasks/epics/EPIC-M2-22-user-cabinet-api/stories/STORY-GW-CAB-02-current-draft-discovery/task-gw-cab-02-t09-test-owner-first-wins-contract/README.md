# task-gw-cab-02-t09-test-owner-first-wins-contract

## Meta
- **Story:** [STORY-GW-CAB-02](../STORY-GW-CAB-02-current-draft-discovery.md)
- **Type:** test (audit follow-up)
- **Status:** 🟢 Done
- **Package:** pkg-000053 (audit follow-up; **run_mode override**, no pkg change)
- **Skill declared:** python-pro
- **Depends on:** T08 (first-wins semantics)
- **Audit report:** [`docs/analysis/audit-gw-cab-02-current-draft-discovery-2026-07-14.md`](../../../../../../analysis/audit-gw-cab-02-current-draft-discovery-2026-07-14.md)
- **Gap ID:** G2 (LOW-MEDIUM)

## Purpose
G2: закрепить first-wins тестом — user-A stash+read associates draft; user-B reads same `draft_id`; `/current` для A still returns draft, B gets `{data: null}`.

## Code Facts (verified)
- Existing isolation test only when B **does not know** `draft_id` — [`test_gw_cab_02_isolation_user_b_does_not_see_user_a_draft`](../../../../../../../../tests/test_gw_cab_02_current_draft_discovery.py)
- grep hijack/overwrite/reassoc in CAB-02 tests = 0 (audit §3 G2)
- Pattern/helpers: [`tests/story_draft_intake_helpers.py`](../../../../../../../../tests/story_draft_intake_helpers.py), CAB-01/CAB-02 client fixtures

## Gap
- **G2 (LOW-MEDIUM):** семантика ownership overwrite не запинена тестом.

## AC/DoD
- [ ] New test: user-A owner preserved after user-B read of same `draft_id`
- [ ] user-B `/current` → `{data: null}` after B's read (B not owner under first-wins)
- [ ] `pytest tests/test_gw_cab_02_current_draft_discovery.py` green
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-cab-02-t09.md`](./acceptance-verification-gw-cab-02-t09.md) signed (Date post live-run only)

## Where to change
- [`tests/test_gw_cab_02_current_draft_discovery.py`](../../../../../../../../tests/test_gw_cab_02_current_draft_discovery.py)

## Out of scope
- Story gate re-sign (optional post-P6)
- Runtime impl (T08)

## Verification commands (post live-run only)
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_cab_02_current_draft_discovery.py -m "not live_integration"
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"
```
