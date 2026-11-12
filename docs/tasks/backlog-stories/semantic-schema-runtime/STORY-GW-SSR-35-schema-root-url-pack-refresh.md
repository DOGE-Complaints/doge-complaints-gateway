# STORY-GW-SSR-35 — SCHEMA_ROOT_URL + SCHEMA_PACK_REFRESH (federation remote registry)

## Meta
- **Key:** `STORY-GW-SSR-35-schema-root-url-pack-refresh`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) · G35 PASS 2026-09-07T08:54:22Z (pkg-000092) · P6 G1 CLOSED 2026-09-07T08:58:54Z
- **Приоритет:** P1 shipped — federation consume stub (operator-forced overnight)
- **Тип:** implement (config + boot fetch + refresh + tests + docs) — **As-of-Done**
- **Parent product:** [`REQ4` §5.3](../../../../../docs/requirements%20backlog/REQ4-Node-Onboarding-Schema-Pack-Federation-Gate.md) (`SCHEMA_ROOT_URL`, boot fetch, `SCHEMA_PACK_REFRESH`, fail-fast)
- **Parent REQ:** [`51-semantic-schema-runtime.md`](../../../requirements/51-semantic-schema-runtime.md) · INDEX **D-SSR-8** / **D-SSR-4** / **D-SSR-12**
- **Prior ops:** [`STORY-GW-SSR-34`](./STORY-GW-SSR-34-uus-active-schema-packs-volume-ops.md) — local warehouse + Railway Volume **без** remote
- **Operator decision (2026-09-07):** `SCHEMA_ROOT_URL` **не** путь Volume; это URL удалённого реестра схем. Volume mount = только `SCHEMA_PACKS_ROOT`.
- **Plan source (trimmed):** [`.cursor/plans/ssr-34_uus_v2_volume_be7b0334.plan.md`](../../../../../.cursor/plans/ssr-34_uus_v2_volume_be7b0334.plan.md) T04 / AC-remote
- **Skill declared:** `python-pro`
- **Git:** только `semantic-schema-runtime`
- **Зависит от:** soft SSR-34 Done (ops path); hard SSR-16; stub manifest (не invent full registry product)
- **Blocks:** full §5.3 remote closure when live federation registry SSOT exists (stub consume shipped)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Delivery:** product + tests + manuals shipped pkg-000092 (P3); G1 SSOT As-of-Done (P6)

---

# Layer 1 — Постановка задачи

## Зачем простыми словами

SSR-34 закрывает повседневный путь: положил pack локально в `schema-packs/` или на Railway Volume (`SCHEMA_PACKS_ROOT`) → `NODE_SCHEMA_*`.

Когда схемы живут в **удалённом реестре федерации**, ноде нужна: **`SCHEMA_ROOT_URL`** → boot (cache miss) скачать файлы **в** cache-корень → опционально **`SCHEMA_PACK_REFRESH`** → fail-fast → `resolve_pack`.

## Scope

1. Config: `SCHEMA_ROOT_URL` + `SCHEMA_PACK_REFRESH` (env contract).
2. Boot: URL set + cache miss (или refresh) → fetch → nested `<id>/<ver>/` → `resolve_pack`.
3. Refresh overwrite; fail-fast on invalid/missing after attempt.
4. Tests: tmp_path + HTTP mock; no live registry in CI.
5. Manuals: federation remote vs SSR-34 Volume; vars marked shipped.

## Out of scope

- Railway Volume UI / local gitignore / uus activate (SSR-34).
- Using `SCHEMA_ROOT_URL` как mount path (запрещено D-SSR-12).
- Pack content / geo repair; Pack Builder / validators.
- F4 Arweave **upload** / membership registry product (соседняя federation волна; эта стори = **consume** stub manifest URLs).
- Changing `NODE_SCHEMA_*` semantics.

## Short AC (Layer 1)

- [x] **AC-GW-SSR35-01:** `SCHEMA_ROOT_URL` boot fetch into cache when miss (federation registry).
- [x] **AC-GW-SSR35-02:** Refresh overwrite; fail-fast; no foreign default.
- [x] **AC-GW-SSR35-03:** After fetch, `resolve_pack` + `NODE_SCHEMA_*` unchanged conceptually.
- [x] **AC-GW-SSR35-04:** SSR-34 Volume/local path remains valid **without** URL.

---

# Layer 2 — Реализация (техническая проработка)

## Verified as-built (pre-P3) → As-of-Done (post-P3 / G35)

| Fact | Evidence |
|------|----------|
| `SCHEMA_ROOT_URL` / `SCHEMA_PACK_REFRESH` in `src/` | **As-of-Done:** [`schema.py`](../../../src/core/config/schema.py) + [`remote_fetch.py`](../../../src/core/schema/remote_fetch.py); 12 tests PASS. **Historical (pre-P3):** grep empty 2026-09-06. |
| Local + Volume without remote | D-SSR-12 / SSR-34 — **unchanged** (URL unset path) |
| URL ≠ mount | Operator 2026-09-07 — path reject in config — **As-of-Done** |

## REQ4 map (эта стори — shipped stub consume)

| Mechanism | Requirement |
|-----------|-------------|
| `SCHEMA_ROOT_URL` | Registry root URL → stub manifest → file URLs |
| Boot / init | Fetch unless fresh cache |
| Persist | Under `SCHEMA_PACKS_ROOT` или default local root |
| `SCHEMA_PACK_REFRESH` | Re-fetch overwrite |
| Fail-fast | No silent foreign pack |

## Подзадачи (pkg-000092 — Done)

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **T01** | Config | Env contract URL + refresh; server-env | Treat URL as Volume path |
| **T02** | Fetch | Manifest + download into nested cache | Live registry mandatory in CI |
| **T03** | Boot wire | Fetch before `resolve_pack` when URL set / miss | Skip resolve on success |
| **T04** | Refresh | Overwrite + fail-fast | Silent foreign fallback |
| **T05** | Tests | `test_gw_ssr_35_*` + httpx mock | Depend on uus content bugs |
| **T06** | Docs | Federation remote vs SSR-34 hand-copy; inventory shipped | |
| **T07** | Gate | G35 | |
| **T08** | Audit docs | G1 As-of-Done SSOT | §Актуальная точка (G2 WAIVED) |

## Manifest shape (stub — refine with federation SSOT)

Минимум: `GET {SCHEMA_ROOT_URL}/{id}/{ver}/manifest.json` → `files` map → nested layout. Точная registry product schema + F4 upload — вне этой стори.

## Concrete AC (P3 gate)

- [x] **AC-GW-SSR35-01:** URL + empty cache + `NODE_SCHEMA_*` → files under cache root → `resolve_pack` SUCCESS (fixture).
- [x] **AC-GW-SSR35-02:** Fresh cache → no unnecessary re-fetch (or documented policy).
- [x] **AC-GW-SSR35-03:** Refresh overwrite; corrupt remote → ConfigError-class; not tallinn default.
- [x] **AC-GW-SSR35-04:** pytest mocked HTTP; no network in CI.
- [x] **AC-GW-SSR35-05:** Manuals: URL = federation registry; Volume path = `SCHEMA_PACKS_ROOT` only.

## Order vs SSR-34

```text
SSR-34 AC-ops (local + Volume hand-copy)  →  Done pkg-000091
SSR-35 AC-remote (federation consume stub) →  Done pkg-000092 G35
```

**Claims:** As-of-Done = product shipped. **Historical:** deferred / «не писать fetch сейчас» = pre-P3 постановка only.

## Risks

- Full live registry contract still external — stub format documented; refine when federation SSOT exists.
- Largest code slice — fetch isolated from resolver parse.
- Race refresh during boot — single-writer assumption.

## Related

| Artifact | Role |
|----------|------|
| REQ4 §5.3 | Product parent |
| SSR-34 / D-SSR-12 | Ops sibling; URL ≠ mount |
| `resolver.py` | Post-fetch consumer |

## DoD

Remote fetch/refresh implemented + tested + documented; SSR-34 path still works with URL unset. G1 SSOT As-of-Done CLOSED.
