# Интервью CPO/CTO — доработки по reopened GAP-2 (status vocabulary) → RC-05/RC-06

**Дата:** 2026-06-20
**Метод:** `.cursor/rules/analysis.mdc` — решения поверх verified-фактов.
**Основание:** [`CLOSURE-empty-board-status-vocabulary-2026-06-20.md`](./CLOSURE-empty-board-status-vocabulary-2026-06-20.md) + [`investigation-...`](./investigation-empty-board-status-vocabulary-2026-06-20.md).
**Итог:** [`STORY-GW-RC-05`](./STORY-GW-RC-05-status-vocabulary-canonicalization.md) (код) + [`STORY-GW-RC-06`](./STORY-GW-RC-06-hosted-status-data-hygiene.md) (данные).

## Verified-факты (перед решениями)
- **Create-path корректен** ([issue_create.py:252](../../../../src/core/application/issue_create.py#L252)) — пишет projection board-status (PUBLISHED). **Extend-path баг** ([:334](../../../../src/core/application/issue_create.py#L334)) — пишет candidate `updated.status.value` (`promoted`). Также [:272](../../../../src/core/application/issue_create.py#L272)/[:300](../../../../src/core/application/issue_create.py#L300) возвращают candidate-статус (в `IssueCreateResult`, не в проекцию — но единообразие важно).
- Проекция **всегда** board-vocab (status=PUBLISHED из `build_projection_input_from_draft`). → сложного маппинга candidate→board не нужно; брать projection-status везде.
- Read-path **не** канонизирует status ([read_filters.py:234](../../../../src/core/projection/read_filters.py#L234)); `canonicalize_status` отсутствует (новое).
- Тесты, фиксирующие неверное значение: `test_spa_projection_supabase_roundtrip.py:29,53` (projection seed/assert `promoted` — **обновить**); `test_supabase_live_full_pipeline_roundtrip.py:155` (projection assert `promoted` — **обновить**). ⚠️ Строка `:133` того же файла — `candidate_rows` (issue_candidates) — `promoted` там **корректен**, НЕ трогать.

## Решения (D-RC05)
- **D-RC05-1 — Разбивка:** 2 стори. **RC-05 (код)** = write-fix + read-канонизация + контракт-тест; **RC-06 (данные)** = миграция hosted + S1.
- **D-RC05-2 — Миграция данных: сейчас.** В RC-06 — прямой `UPDATE doge_issues SET status='PUBLISHED' WHERE status='promoted'` на hosted (быстрый демо-эффект).
- **D-RC05-3 — S1 (пустой title_json 4/5):** в RC-06 (data-гигиена hosted: reproject пустого контента вместе со status-миграцией).
- **D-RC05-4 — Контракт-тест на РЕАЛЬНОМ выводе пайплайна** (create→extend/promote), не happy-seed — это AC RC-05 (закрывает корень «почему RC-03 не поймал»).

## Открытые вопросы (стори-уровень)
- RC-05: поведение read-канонизации для неизвестного status (mirror RC-02 type: default+log vs pass-through).
- RC-06: доступ к hosted Supabase для UPDATE/reproject — у кого; делать ли резервную выгрузку перед UPDATE.
