# STORY-GW-REQ9-02 — Makefile `test` + `test-live` (REQ9 G7)

## Meta
- **Key:** `STORY-GW-REQ9-02-make-test`
- **Parent Epic:** [`../../../EPIC-req9-ops-parity-env-naming.md`](../../../EPIC-req9-ops-parity-env-naming.md)
- **Пакет:** [`req9-ops-parity-env-naming/`](../../../../backlog-stories/req9-ops-parity-env-naming/INDEX.md)
- **Status:** 🔵 Done
- **Тип:** Makefile / ops ritual
- **source:** [`../../../../backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-02-make-test.md`](../../../../backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-02-make-test.md)
- **Parent REQ:** [`53-req9-ops-parity-env-naming.md`](../../../../requirements/53-req9-ops-parity-env-naming.md) §2, §4, §5 G7
- **Parent product:** REQ9 G7
- **Tech-arch:** [`01-runtime-and-probes.md`](../../../../../../docs/architecture/req9-ops-naming/01-runtime-and-probes.md) (Make parity class)
- **decision_ref:** backlog REQ9-02 · REQ53 · tech-arch `01-runtime-and-probes.md` · operator lock C
- **Skill declared:** python-pro
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000097-20260926-gw-req9-02-make-test.yaml`](../../../../gateway-active-packages/pkg-000097-20260926-gw-req9-02-make-test.yaml)
- **Git:** `semantic-schema-runtime`
- **Operator lock:** **C** — `make test` offline (`not live_integration`); separate `make test-live`
- **Зависит от:** — (parallel to REQ9-01)
- **Etalon:** identity/threads `Makefile` `test:`; gateway marker `live_integration` in `pyproject.toml:34-35`
- **Scaffolded:** 2026-09-26T12:17:44Z
- **Done:** 2026-09-26T12:22:28Z · P3 pkg-000097 T01–T03

## Nested tasks (pkg-000097)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req9-02-t01-make-test-offline`](./task-gw-req9-02-t01-make-test-offline/README.md) | Done |
| T02 | [`task-gw-req9-02-t02-make-test-live`](./task-gw-req9-02-t02-make-test-live/README.md) | Done |
| T03 | [`task-gw-req9-02-t03-story-gate`](./task-gw-req9-02-t03-story-gate/README.md) | Done |
| T04 | [`task-gw-req9-02-t04-audit-g1-as-of-done-ssot`](./task-gw-req9-02-t04-audit-g1-as-of-done-ssot/README.md) | Done (audit follow-up) |

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
| `test:` offline marker expression | `Makefile:50–51` |
| `test-live:` live marker | `Makefile:53–54` |
| Marker `live_integration` unchanged | `pyproject.toml:34–35` |
| serve/dev/simulate/check-env bodies | unchanged beyond PHONY/usage |

### Historical (pre-P3)

| Fact | Path |
|------|------|
| `.PHONY: serve dev simulate check-env` — no `test` | `Makefile:1` |
| Targets serve/dev/simulate/check-env | `Makefile:14-42` |

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

## Code touchpoints

- `Makefile`

## Dependencies

- None on REQ9-01.

## Gate

[`task-gw-req9-02-t03-story-gate/story-acceptance-gate-STORY-GW-REQ9-02.md`](./task-gw-req9-02-t03-story-gate/story-acceptance-gate-STORY-GW-REQ9-02.md) — PASS
