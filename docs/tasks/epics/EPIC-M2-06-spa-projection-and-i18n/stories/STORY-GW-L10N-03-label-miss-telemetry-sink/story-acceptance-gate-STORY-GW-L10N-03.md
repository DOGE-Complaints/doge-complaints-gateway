# Story acceptance gate — STORY-GW-L10N-03

- **Story:** Анонимный приём телеметрии непереведённых меток
- **Package:** `pkg-000029-20260615-gw-l10n-03-label-miss-telemetry-sink.yaml`
- **Result:** PASS
- **Date:** 2026-06-15

## AC checklist (verbatim from backlog)

| AC | Status | Evidence |
|----|--------|----------|
| Публичный `POST` принимает `{label_key, locale}` без токена и без PII | PASS | `tests/test_gw_l10n_03_label_miss_telemetry.py::test_post_label_miss_accepts_without_auth` |
| Валидное событие фиксируется в отдельной таблице; повтор агрегируется/накапливается | PASS | migration `20260615_1200_gw_l10n_03_label_translation_misses.sql`; `test_in_memory_store_aggregates_repeats`; `test_post_label_miss_accepts_without_auth` |
| Невалидный payload → мягкая ошибка без утечки деталей; недоступность хранилища не влияет на другие пути | PASS | `test_post_label_miss_invalid_payload_returns_soft_400`; `test_post_label_miss_store_failure_returns_202_degraded` |
| Есть оператор-запрос для просмотра новых непереведённых ключей | PASS | view `20260615_1210_gw_l10n_03_label_translation_misses_ranked_view.sql`; `docs/runtime-docs/appendix/label-translation-misses-operator-ru.md` |
| openapi/API_REFERENCE обновлены; зафиксирована анонимность | PASS | `openapi.yaml` `/telemetry/label-misses`; `API_REFERENCE.md` §6.5 |
| `builder_resolve_queue.py --verify` ok 7 paths | PASS | pkg-000029 (live run 2026-06-15) |
| Тест-суит без регрессий | PASS | `463 passed in 14.44s` — live run 2026-06-15 UTC |

## Commands (live verification 2026-06-15)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_l10n_03_label_miss_telemetry.py -q
cd doge-complaints-gateway && python3 -m pytest tests/ -q --ignore=tests/smoke --ignore=tests/integration
```
