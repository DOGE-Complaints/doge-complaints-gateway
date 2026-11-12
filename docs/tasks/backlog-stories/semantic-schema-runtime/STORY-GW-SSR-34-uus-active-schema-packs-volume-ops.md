# STORY-GW-SSR-34 — uus active: local warehouse + Railway Volume (REQ4 §5.3 ops)

## Meta
- **Key:** `STORY-GW-SSR-34-uus-active-schema-packs-volume-ops`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** Done (Awaiting Commits) pkg-000091 · G34 PASS 2026-09-07T08:32:02Z
- **Приоритет:** P1 — операторский путь «код в git / pack не в git / Volume на Railway»
- **Тип:** docs / env / gitignore / node activation (без remote-fetch кода)
- **Parent product:** [`REQ4` §5.3](../../../../../docs/requirements%20backlog/REQ4-Node-Onboarding-Schema-Pack-Federation-Gate.md) (Volume + `NODE_SCHEMA_*` + `SCHEMA_PACKS_ROOT`)
- **Parent REQ:** [`51-semantic-schema-runtime.md`](../../../requirements/51-semantic-schema-runtime.md) · INDEX **D-SSR-8** · **D-SSR-12** (ниже)
- **Operator decision (2026-09-07):** local = in-tree `schema-packs/` + `NODE_SCHEMA_*`; node packs **не в git**; Railway = Volume + **`SCHEMA_PACKS_ROOT`** (не `SCHEMA_ROOT_URL`); remote URL → SSR-35 later (federation registry)
- **Evidence (ops path works when pack loadable):** [`uus-veerenni-civic-v2-active-volume-smoke-2026-09-06.md`](../../../analysis/uus-veerenni-civic-v2-active-volume-smoke-2026-09-06.md) §3.3 / §5
- **Plan source (trimmed):** [`.cursor/plans/ssr-34_uus_v2_volume_be7b0334.plan.md`](../../../../../.cursor/plans/ssr-34_uus_v2_volume_be7b0334.plan.md) — **без** pack content repair / layout rename / geo enum patch
- **Skill declared (future P3):** `code-documenter` · soft `python-pro` только если правка `.env*.example` / `.gitignore`
- **Git:** только `semantic-schema-runtime`
- **Зависит от:** SSR-16 Done (active pair + boot resolve); **precondition** — loadable nested pack `uus_veerenni_civic/<ver>/` (operator repair + retest **вне** этой стори)
- **Blocks:** операторский local+Volume playbook; soft handoff к SSR-35 (federation later)
- **Sibling (не эта стори):** GPT-PB-12 / SCR-NODEONB-02 / GPT-PB-13 (Pack Builder + validator geo); pack instance repair
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Delivery class этой волны постановки:** story + INDEX only — **не** Railway UI clicks, **не** remote-fetch code, **не** materialize `.gitignore` до P3

---

# Layer 1 — Постановка задачи

## Зачем простыми словами

Git / image = **общий код**. Характер ноды = schema pack (три JSON). Активная пара всегда **`NODE_SCHEMA_ID` + `NODE_SCHEMA_VERSION`**.

**Локально:** тот же путь, что сейчас — `doge-complaints-gateway/schema-packs/<id>/<ver>/`. `SCHEMA_PACKS_ROOT` обычно **не** нужен (default root). Кастом ноды (uus и т.п.) лежит на диске для запуска, но **не коммитится**. Demo/seed для pytest (`tallinn_civic`, `legal_process`, `mobility_observation`, …) могут оставаться в git.

**Railway:** Volume с mount path → env **`SCHEMA_PACKS_ROOT`** = этот mount → copy nested tree → те же `NODE_SCHEMA_*` → redeploy.  
**Не путать:** путь Volume = `SCHEMA_PACKS_ROOT`, **не** `SCHEMA_ROOT_URL`.

**Потом (SSR-35):** когда схемы в удалённом реестре федерации — `SCHEMA_ROOT_URL` (+ refresh) качает в тот же cache-корень. Для текущей волны ops **не** требуется.

## Precondition (не scope SSR-34)

| Precondition | Owner |
|--------------|-------|
| Nested layout `pack.json` / `payload.schema.json` / `taxonomy.json` | Operator pack wave |
| `resolve_pack(SchemaRef(uus…, ver))` SUCCESS при `NODE_SCHEMA_*` | Operator retest |
| Geo / civic knobs ∈ gateway enums | Pack repair / GPT-PB-* / SCR-NODEONB-* — **не** Volume docs |

Если precondition не выполнен — **не** закрывать AC «обходом» через silent tallinn fallback.

## Scope

1. Зафиксировать **D-SSR-12** в INDEX + manuals: local warehouse path, git policy, Railway Volume via `SCHEMA_PACKS_ROOT`.
2. Активация uus (loadable ver) через `NODE_SCHEMA_*` (env examples; dual demo/node допустим).
3. Railway Volume playbook: create → mount → `SCHEMA_PACKS_ROOT` → copy → `NODE_SCHEMA_*` → redeploy → fail-fast.
4. Local playbook: files under `schema-packs/`; без Volume; node packs gitignored (правило + пример ignore для uus; demo packs stay tracked).
5. Env inventory: `NODE_SCHEMA_*`, `SCHEMA_PACKS_ROOT`; `SCHEMA_ROOT_URL` / refresh = **later / SSR-35 / federation** (не pretend present).
6. Sibling note: GPT `schema_binding` == active pair (без правки GPT files).

## Out of scope

- Pack.json content repair / geo enum expand.
- Реализация `SCHEMA_ROOT_URL` / `SCHEMA_PACK_REFRESH` (→ **SSR-35**, federation later).
- F4 Arweave upload / federation registry product.
- GPT Pack Builder / scripts validator bodies.
- Вынос local warehouse в каталог **вне** `doge-complaints-gateway/schema-packs/` (отвергнуто оператором 2026-09-07).

## Short AC (Layer 1)

- [x] **AC-GW-SSR34-01:** Manuals: local `schema-packs/` + `NODE_SCHEMA_*` (без Volume); Railway Volume + `SCHEMA_PACKS_ROOT` + `NODE_SCHEMA_*`.
- [x] **AC-GW-SSR34-02:** Явно: Volume mount path ≠ `SCHEMA_ROOT_URL`; remote = SSR-35 later.
- [x] **AC-GW-SSR34-03:** Node packs (uus) не в git; demo packs для тестов — tracked; fail-fast без silent foreign default.
- [x] **AC-GW-SSR34-04:** Precondition loadable pack; content repair **не** в DoD.

---

# Layer 2 — Реализация (техническая проработка)

## Verified as-built (pre-P3) → As-of-Done (post-P3 / G34)

| Fact | Evidence |
|------|----------|
| Active pair required | `NODE_SCHEMA_ID` / `NODE_SCHEMA_VERSION` (SSR-16) — **unchanged** |
| Pack root | `SCHEMA_PACKS_ROOT` **или** `<gateway>/schema-packs/` — `resolver.py` `default_packs_root`, **не** поле `AppConfig` — **unchanged** |
| Layout | nested `<id>/<ver>/{pack,payload.schema,taxonomy}.json` — **unchanged** |
| Volume в manuals | **As-of-Done:** Local + Railway playbooks (`server-env-quickstart.md`) + warehouse D-SSR-12 (`schema-packs-node-data-model-ru.md`). **Historical:** Volume почти не описан. |
| `SCHEMA_ROOT_URL` / refresh | **absent** in `src/` → SSR-35 later — **unchanged** |
| Local gitignore node packs | **As-of-Done:** `.gitignore` ignores `schema-packs/uus_veerenni_civic/`; demo packs tracked. **Historical (pre-P3):** gitignore **не** исключал uus — gap. |
| Volume-sim | smoke 2026-09-06: loadable pack + `SCHEMA_PACKS_ROOT` OK — evidence kept |

## D-SSR-12 (operator lock — document in INDEX + manuals)

| Среда | Корень склада | Active | Git |
|-------|---------------|--------|-----|
| Local | default `doge-complaints-gateway/schema-packs/` (`SCHEMA_PACKS_ROOT` unset) | `NODE_SCHEMA_*` | demo/seed tracked; **node packs (uus…) ignored / not committed** |
| Railway | Volume mount = `SCHEMA_PACKS_ROOT` (напр. `/data/schema-packs`) | те же `NODE_SCHEMA_*` | N/A (Volume, не git) |
| Federation later | fetch → тот же cache root | без смены identity | SSR-35 |

## Map REQ4 §5.3 → эта стори

| REQ4 mechanism | SSR-34 |
|----------------|--------|
| Railway Volume | Manuals + mount = **`SCHEMA_PACKS_ROOT`** |
| `NODE_SCHEMA_ID` / `VERSION` | Activate uus (loadable ver); local + Railway |
| Fail-fast | As-built boot; manuals: no foreign default |
| Local imitation | Same nested layout under in-tree `schema-packs/` |
| `SCHEMA_ROOT_URL` / refresh | **Out** → SSR-35 (federation registry later) |

## Подзадачи (P3)

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **T01** | Docs | Local + Railway sections в [`server-env-quickstart.md`](../../../runtime-docs/manuals/server-env-quickstart.md); env ≠ URL | Remote fetch code |
| **T02** | Docs | Warehouse model в [`schema-packs-node-data-model-ru.md`](../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md): local path, git policy, Volume precedence | Pack content invent |
| **T03** | Git policy | `.gitignore` (или documented equivalent): ignore node packs e.g. `schema-packs/uus_veerenni_civic/`; **keep** tallinn/legal/mobility tracked | Ignore entire `schema-packs/` |
| **T04** | Env docs | `.env.example` / `.env.test.example` / inventory: uus active (или dual); `SCHEMA_PACKS_ROOT` Railway-only note | Claim `SCHEMA_ROOT_URL` shipped |
| **T05** | Gate note | Sibling: GPT `schema_binding` == env pair | Edit GPT Instructions |
| **T06** | Verify | Boot checklist local + Railway prose after loadable pack | «Починить» pack.json в этой стори |

## Concrete AC (P3 gate)

- [x] **AC-GW-SSR34-01:** Local prose: put pack under `schema-packs/<id>/<ver>/`; set `NODE_SCHEMA_*`; no Volume; no `SCHEMA_ROOT_URL`.
- [x] **AC-GW-SSR34-02:** Railway prose: create Volume → mount (напр. `/data/schema-packs`) → **`SCHEMA_PACKS_ROOT`** → copy nested uus → `NODE_SCHEMA_*` → redeploy → boot shows pair.
- [x] **AC-GW-SSR34-03:** Explicit glossary: `SCHEMA_PACKS_ROOT` = disk/mount; `SCHEMA_ROOT_URL` = remote manifest (**SSR-35 / federation later**, not for Volume path).
- [x] **AC-GW-SSR34-04:** Missing/invalid pack → fail-fast; **не** подставлять tallinn.
- [x] **AC-GW-SSR34-05:** Node packs not committed (gitignore or equivalent documented + applied for uus); demo packs remain available for pytest.
- [x] **AC-GW-SSR34-06:** INDEX **D-SSR-12** + wave 34–35; no claim remote fetch Done.

## Risks

- Closing AC while pack unloadable = false Done.
- Ignoring **entire** `schema-packs/` breaks CI (tallinn fixtures) — ignore only node trees.
- If uus already tracked — P3 must untrack (`git rm --cached`) carefully; не удалять файлы с диска оператора.
- Changing active pair without GPT binding → intake 4xx (SSR-17).

## Related

| Artifact | Role |
|----------|------|
| REQ4 §5.3 | Product parent |
| SSR-16…18 | Active schema as-built |
| SSR-35 | Federation remote fetch (**later**) |
| Smoke analysis 2026-09-06 | Ops path evidence |

## DoD

Manuals + env + git policy enable local uus + Railway Volume ops; no remote-fetch code; no pack content repair.

## Claims (Layer 2)

**As-of-Done:** D-SSR-12 ops docs + gitignore + env inventory landed; G34 PASS 2026-09-07T08:32:02Z (pkg-000091); G1 CLOSED P6 2026-09-07T08:38:47Z.  
**Historical:** Volume undocumented / uus not gitignored verified pre-P3.
