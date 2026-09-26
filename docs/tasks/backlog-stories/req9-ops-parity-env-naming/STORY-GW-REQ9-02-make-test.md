# STORY-GW-REQ9-02 — Makefile `test` + `test-live` (REQ9 G7)

## Meta
- **Key:** `STORY-GW-REQ9-02-make-test`
- **Пакет:** [`req9-ops-parity-env-naming/`](./INDEX.md)
- **Status:** Todo
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

| Fact | Path |
|------|------|
| `.PHONY: serve dev simulate check-env` — no `test` | `Makefile:1` |
| Targets serve/dev/simulate/check-env | `Makefile:14-42` |
| Marker `live_integration` declared | `pyproject.toml:34-35` |
| Profile `test_command` | `profiles.yaml` gateway: `cd doge-complaints-gateway && python3 -m pytest -q` |

## Target / AC

- [ ] **AC-GW-REQ902-01:** `make test` exists and runs offline pytest with `-m "not live_integration"` (G7 primary).
- [ ] **AC-GW-REQ902-02:** `.PHONY` includes `test`.
- [ ] **AC-GW-REQ902-03:** `make test-live` exists for live_integration suite (operator lock C; hygiene, not extra product scope).

## Техническое решение (projected)

```make
test:
	.venv/bin/python -m pytest -q -m "not live_integration"
test-live:
	.venv/bin/python -m pytest -q -m live_integration
```

(Exact interpreter path align with existing Makefile `.venv/bin/python` style at P3.)

## Nested tasks (planned — folders at P1.3 only; name ≠ create)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-gw-req9-02-t01-make-test-offline` | Todo | `test` target + PHONY; `-m "not live_integration"` |
| **T02** | `task-gw-req9-02-t02-make-test-live` | Todo | `test-live` target + PHONY |
| **T03** | `task-gw-req9-02-t03-story-gate` | Todo | AC-GW-REQ902-01…03 gate |

## Code touchpoints

- `Makefile`

## Dependencies

- None on REQ9-01.
