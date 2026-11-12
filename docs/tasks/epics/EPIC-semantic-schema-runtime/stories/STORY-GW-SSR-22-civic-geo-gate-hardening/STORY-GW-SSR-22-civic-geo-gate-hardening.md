# STORY-GW-SSR-22 — Civic geo-gate hardening

## Meta
- **Key:** `STORY-GW-SSR-22-civic-geo-gate-hardening`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — geo-detail wave (sequence **22**)
- **Тип:** implement (handlers + boot fail; дыры scope-gate)
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-22-civic-geo-gate-hardening.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-22-civic-geo-gate-hardening.md)
- **Parent REQ:** 35 geo scope / 51; INDEX **D-SSR-10**
- **Decision:** INDEX **D-SSR-10**
- **decision_ref:** backlog SSR-22 + INDEX **D-SSR-10**
- **Skill declared:** python-pro
- **Etalon структуры:** [STORY-GW-SSR-20](../STORY-GW-SSR-20-node-clustering-runtime-wire/STORY-GW-SSR-20-node-clustering-runtime-wire.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000079-20260830-gw-ssr-22-civic-geo-gate-hardening.yaml`](../../../../gateway-active-packages/pkg-000079-20260830-gw-ssr-22-civic-geo-gate-hardening.yaml)
- **Git:** только `semantic-schema-runtime` — [geo-detail Шаг 0](../../../../backlog-stories/semantic-schema-runtime/orchestrator-geo-detail-runbook.md)
- **Зависит от:** SSR-20 ([pipeline](../STORY-GW-SSR-20-node-clustering-runtime-wire/STORY-GW-SSR-20-node-clustering-runtime-wire.md)); overnight after G21
- **Scaffolded:** 2026-08-30T20:01:08Z
- **P4 audit:** 2026-08-30T20:13:31Z [`audit-gw-ssr-22-civic-geo-gate-hardening-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-22-civic-geo-gate-hardening-2026-08-30.md) · product AC yes · G1 CLOSED (T05) · G2 WAIVED

### Трассировка
| Слой | Документ | §§ |
|------|----------|-----|
| Child REQ | 35 / 51 | INDEX **D-SSR-10** |
| Decision | INDEX **D-SSR-10** | civic scope-gate: нет silent skip при активном scope |

- **Разблокирует:** G22 → SSR-23 (не этот pkg).
- **Не reopen:** SSR-01…05 / 08–21 product; T-wave G3 historical
- **Не трогаем:** GPT UI; `ClusterLens`; `GET /schema-active`; полный `geo_detail` (→23); глобальный require-geo; bullrun §«Актуальная точка»

## Nested tasks (pkg-000079)

| ID | Folder |
|----|--------|
| T00 | [`task-gw-ssr-22-t00-fail-mode-decision`](./task-gw-ssr-22-t00-fail-mode-decision/README.md) |
| T01 | [`task-gw-ssr-22-t01-handlers-no-silent-skip`](./task-gw-ssr-22-t01-handlers-no-silent-skip/README.md) |
| T02 | [`task-gw-ssr-22-t02-boot-fail-if-chosen`](./task-gw-ssr-22-t02-boot-fail-if-chosen/README.md) |
| T03 | [`task-gw-ssr-22-t03-tests`](./task-gw-ssr-22-t03-tests/README.md) |
| T04 | [`task-gw-ssr-22-t04-story-acceptance-gate`](./task-gw-ssr-22-t04-story-acceptance-gate/README.md) |
| T05 | [`task-gw-ssr-22-t05-audit-g1-as-of-done-ssot`](./task-gw-ssr-22-t05-audit-g1-as-of-done-ssot/README.md) |

## Зачем простыми словами

Scope-check сейчас **тихо пропускается**, если нет `location_query` или `geo_service is None`. При активном `geo_scope` ноды это дыра: истории вне зоны или без geo могут пройти. Закрыть silent skip; полная политика `geo_intake` / `geo_detail` — следующие стори.

## Scope / Out of scope

**In:** [`handlers.py`](../../../../../../src/core/api/handlers.py) `:254–268` — при активном `geo_scope` (из pack `node_clustering.civic` после SSR-20, не invent dual env): если `geo_service is None` → **не** silent accept (4xx «geo unavailable» **или** ConfigError на boot, если scope задан и resolve обязателен — выбрать одно в T00 и зафиксировать в AC). Согласовать с минимальным stub `geo_intake.mode` **или** harden только на «scope set ⇒ service required + query/detail required for scope check». Тесты: scope+no service → не 202; optional path (нет scope) как сейчас; адаптировать [`test_req35_geo_scope_and_filter.py`](../../../../../../tests/test_req35_geo_scope_and_filter.py).

**Out:** полный блок `geo_detail` wire (→23); SQL address columns (→24); смена `ClusterLens`; GPT UI.

## Verified current state

| Fact | Ref |
|------|-----|
| **As-of-Done (SSR-22 pkg-000079):** scope + `geo_service is None` → `IntakeValidationError("geo unavailable")` | [`handlers.py:258–260`](../../../../../../src/core/api/handlers.py) |
| **As-of-Done:** scope-check (resolve + assert) только при scope **и** location_query | [`handlers.py:261–269`](../../../../../../src/core/api/handlers.py) |
| Intake `geo_service` optional | [`services.py:100`](../../../../../../src/core/application/services.py) |
| Factory always wires `GeoService` | [`service_factory.py:64`](../../../../../../src/core/infrastructure/service_factory.py) |
| **As-of-Done:** 422 на `GeoScopeMismatchError` | [`handlers.py:324–337`](../../../../../../src/core/api/handlers.py) |
| **Historical (pre-SSR-22):** `geo_service is None` → skip check | [`handlers.py:260–268`](../../../../../../src/core/api/handlers.py) pre-P3 |
| REQ-35: без location допустимы | исторически; D-SSR-10: политика pack, не silent при scope+required |

## Стыковка

Не ломать режим «optional / нет geo_scope» (geo-agnostic stories). Не требовать geo глобально. Полный `geo_intake` modes — SSR-23; в 22 достаточно убрать silent skip при активном scope.

## Подзадачи

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **T00** | Decision | Boot ConfigError vs intake 4xx при scope+no service | Dual-source invent |
| **T01** | Handlers | Убрать silent skip; fail явно | Новый HTTP path |
| **T02** | Boot (если T00=boot) | Fail-fast когда scope и нет geo_service | Удалить GeoService |
| **T03** | Tests | req35 + `test_gw_ssr_22_*` | geo_detail parse (→23) |
| **T04** | Gate | scope+no service не accept; ClusterLens=10 | |
| **T05** | Docs | Audit G1 As-of-Done vs Historical (§Verified + T00/T01 Code Facts) | Runtime / §Актуальная точка / T-wave G3 |

## Target / AC

- [x] При активном `geo_scope` и `geo_service is None` intake **не** проходит молча. **T00:** intake 4xx (`IntakeValidationError("geo unavailable")`).
- [x] Без `geo_scope` поведение geo-agnostic сохраняется (как REQ-35 optional).
- [x] Тесты покрывают fail path и optional path.
- [x] `ClusterLens` = 10; нет `GET /schema-active`.

## Dependencies

- SSR-20 Done (geo_scope в pack). Wire `geo_detail` — SSR-23.
