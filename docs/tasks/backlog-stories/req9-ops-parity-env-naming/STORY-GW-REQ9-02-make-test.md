# STORY-GW-REQ9-02 — Makefile `test` + `test-live` (REQ9 G7)

## Meta
- **Key:** `STORY-GW-REQ9-02-make-test`
- **Пакет:** [`req9-ops-parity-env-naming/`](./INDEX.md)
- **Status:** Done
- **Тип:** Makefile / ops ritual
- **Parent REQ:** [`53-req9-ops-parity-env-naming.md`](../../../requirements/53-req9-ops-parity-env-naming.md) §2, §4, §5 G7
- **Parent product:** REQ9 G7
- **Tech-arch:** [`01-runtime-and-probes.md`](../../../../../docs/architecture/req9-ops-naming/01-runtime-and-probes.md) (Make parity class)
- **Skill declared (future P3):** `python-pro`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Operator lock:** **C** — `make test` offline (`not live_integration`); separate `make test-live`
- **Зависит от:** — (parallel to REQ9-01)
- **Etalon:** identity/threads `Makefile` `test:`; gateway marker `live_integration` in `pyproject.toml:34-35`
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Pipeline:** [`../../epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-02-make-test/STORY-GW-REQ9-02-make-test.md`](../../epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-02-make-test/STORY-GW-REQ9-02-make-test.md)
- **Done:** 2026-09-26T12:22:28Z · pkg-000097 T01–T03 · gate PASS

---

## Scope

1. Add `make test` that runs pytest excluding `live_integration` (existing marker — do not invent new markers).
2. Add `make test-live` that runs the live_integration-marked suite (or documented equivalent).
3. Register both in `.PHONY`.
4. Do not change `serve` / `dev` / `simulate` / `check-env` semantics beyond PHONY list.

## Out of scope

- Env / SPA rename (→ STORY-GW-REQ9-01).
- aibridge Makefile.
- Inventing CI workflows.
- Claiming Railway verify from `make test` alone (honesty: offline ≠ hosted).

## Verified current state

### As-of-Done (post-P3 · pkg-000097 · gate 2026-09-26T12:22:28Z)

| Fact | Path |
|------|------|
| `.PHONY` includes `test` + `test-live` | `Makefile:1` |
| `test:` offline `-m "not live_integration"` | `Makefile:50–51` |
| `test-live:` `-m live_integration` | `Makefile:53–54` |
| Marker `live_integration` unchanged | `pyproject.toml:34–35` |
| serve/dev/simulate/check-env bodies | unchanged beyond PHONY/usage |
| Profile `test_command` | `profiles.yaml` gateway: `cd doge-complaints-gateway && python3 -m pytest -q` |

### Historical (pre-P3)

| Fact | Path (was) |
|------|------------|
| `.PHONY: serve dev simulate check-env` — no `test` | `Makefile:1` |
| Targets serve/dev/simulate/check-env only | `Makefile:14-42` |

## Target / AC

- [x] **AC-GW-REQ902-01:** `make test` exists and runs offline pytest with `-m "not live_integration"` (G7 primary).
- [x] **AC-GW-REQ902-02:** `.PHONY` includes `test`.
- [x] **AC-GW-REQ902-03:** `make test-live` exists for live_integration suite (operator lock C; hygiene, not extra product scope).

## Техническое решение (as-shipped)

```make
test:
	.venv/bin/python -m pytest -q -m "not live_integration"
test-live:
	.venv/bin/python -m pytest -q -m live_integration
```

(Interpreter path aligned with existing Makefile `.venv/bin/python` style.)

## Nested tasks (pipeline Done pkg-000097 · P3 2026-09-26T12:22:28Z · T04 P6 2026-09-26T12:31:20Z)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | [`task-gw-req9-02-t01-make-test-offline`](../../epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-02-make-test/task-gw-req9-02-t01-make-test-offline/README.md) | Done | `test` target + PHONY; `-m "not live_integration"` |
| **T02** | [`task-gw-req9-02-t02-make-test-live`](../../epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-02-make-test/task-gw-req9-02-t02-make-test-live/README.md) | Done | `test-live` target + PHONY |
| **T03** | [`task-gw-req9-02-t03-story-gate`](../../epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-02-make-test/task-gw-req9-02-t03-story-gate/README.md) | Done | AC-GW-REQ902-01…03 gate PASS |
| **T04** | [`task-gw-req9-02-t04-audit-g1-as-of-done-ssot`](../../epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-02-make-test/task-gw-req9-02-t04-audit-g1-as-of-done-ssot/README.md) | Done | G1 CLOSED As-of-Done SSOT · `gw_req9_02_audit_followup` |

## Code touchpoints

- `Makefile`

## Dependencies

- None on REQ9-01.
