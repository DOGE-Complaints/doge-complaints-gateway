# Story acceptance gate — STORY-GW-SSR-34

- **Story:** uus active local warehouse + Railway Volume ops (D-SSR-12)
- **Package:** `pkg-000091-20260907-gw-ssr-34-uus-active-schema-packs-volume-ops.yaml`
- **Result:** PASS
- **Date:** 2026-09-07T08:32:02Z

## AC checklist

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-SSR34-01: Local prose schema-packs + NODE_SCHEMA_* | PASS | `server-env-quickstart.md` Local playbook |
| AC-GW-SSR34-02: Railway Volume → SCHEMA_PACKS_ROOT | PASS | Railway playbook same manual |
| AC-GW-SSR34-03: SCHEMA_PACKS_ROOT ≠ SCHEMA_ROOT_URL | PASS | Glossary tables in server-env + warehouse manual |
| AC-GW-SSR34-04: fail-fast no tallinn fallback | PASS | manuals + example.env notes |
| AC-GW-SSR34-05: gitignore uus_*; demo tracked | PASS | `.gitignore`; `check-ignore` uus; tallinn/legal/mobility ls-files |
| AC-GW-SSR34-06: INDEX D-SSR-12; no remote fetch Done | PASS | INDEX D-SSR-12 + wave 34–35; `rg SCHEMA_ROOT_URL src/` empty |

## Commands (live verification — P3)

```text
--verify ok 6 (pkg-000091) + ok date-check
utc_now: 2026-09-07T08:32:02Z
git check-ignore schema-packs/uus_veerenni_civic/v2/pack.json → .gitignore:18
no SCHEMA_ROOT_URL in src/; no pack repair; §Актуальная точка not rewritten; push=no
```
