# Story acceptance gate — STORY-GW-SSR-11

- **Story:** Pack-declared fields on Issue projection
- **Package:** `pkg-000070-20260829-gw-ssr-11-pack-declared-issue-projection.yaml`
- **Result:** PASS
- **Date:** 2026-08-29T19:13:51Z

## G11 (runbook §6.5)

Allowlist fields on pack Issue card. Public read = `GET /node/issues`. Overlay UI spa — no.

| G11 check | Result | Evidence |
|-----------|--------|----------|
| public dict **не** содержит целиком `structured_payload` | PASS | `rg structured_payload` `dto.py` empty; `test_dto_source_has_no_structured_payload_token`; `test_named_sidecar_is_not_payload_dump` |
| civic Issues без новых required keys | PASS | `DOGEIssue` fields unchanged; `to_public_dict()` without `schema_card` omits sidecar; `test_civic_to_public_dict_unchanged_without_sidecar` |
| path канон `/node/issues` (не `/tallinn/issues`) | PASS | `asgi_app.py:462` `@app.get("/node/issues")`; `test_public_read_path_is_node_issues` |
| factory civic default на месте | PASS | `gates.py:14` `require_actionable_canonical_type: bool = True`; `service_factory.py:108–111` no False override; `test_civic_gate_factory_default_stays_true` |
| spa overlay UI не в diff | PASS | no `spa-app/` product files in this story |

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Pack MAY объявить card fields; absent = текущая civic-форма карточки. | PASS | `card_fields` in `schema-packs/README.md`; `_parse_card_fields`; `legal_process`/`tallinn_civic` without key → `()`; `test_legal_process_absent_card_fields_is_civic_form` |
| Public Issue **не** содержит целиком `structured_payload`. | PASS | `dto.py` has no `structured_payload` token; sidecar `schema_card` only named leaves; `test_gw_ssr_11_public_dict_no_dump.py` |
| `forbidden` / `node_private` не утекают. | PASS | `project_card_fields` filters blocked states + prefixes; `test_forbidden_and_node_private_filtered_even_if_listed` |
| Public read path = `GET /node/issues` (D-SSR-7 / SSR-13), не `/tallinn/issues`. | PASS | `asgi_app.py:462`; G11 rg `/node/issues` |
| Overlay UI spa-app в этой стори не менять. | PASS | spa-app not touched |

## Commands (live verification 2026-08-29T19:13:51Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now
cd doge-complaints-gateway
.venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_11_card_fields_loader.py tests/test_gw_ssr_11_public_dict_no_dump.py \
  tests/test_gw_ssr_05_public_card_no_payload.py tests/test_doge_issue_projection.py \
  tests/test_gw_ssr_10_dual_pack_flag.py
# → 29 passed
rg -n "structured_payload" src/core/projection/dto.py
# → empty
rg -n "/node/issues" src/core/api/asgi_app.py
rg -n "require_actionable_canonical_type: bool = True" src/core/promotion/gates.py
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)

## Residual (not story AC)

SSR-06/07/12/14/15 not started. SSR-01…05 / 08–10 / 13 not reopened. Pie T-wave unchanged. bullrun §«Актуальная точка» unchanged. `gateway-mvp-dashboard.md` unchanged. pkg-000070 immutable. `SchemaRuntime.project` stub stays.
