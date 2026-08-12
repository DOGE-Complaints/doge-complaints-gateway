# STORY-GW-RC-06 — Гигиена hosted-данных: status-миграция + пустой контент (S1)

## Meta
- **Key:** `STORY-GW-RC-06`
- **Status:** 🔵 Done (Awaiting Commits) — pipeline ([pkg-000035](../../gateway-active-packages/pkg-000035-20260620-gw-rc-06-hosted-status-data-hygiene.yaml), T01–T05, gate PASS 2026-06-20): hosted `promoted`→`PUBLISHED` (5→0), 4 пустых test-seed удалены (backup в T01), 1 валидная карточка подтверждена `GET /tallinn/issues`. Код-аудит [`audit-gw-rc-06-...`](../../../analysis/audit-gw-rc-06-hosted-status-data-hygiene-2026-06-21.md) (artifact-based, evidence совпадает с investigation E3; прод-код не тронут). **Наблюдение:** доска=1 карточка → полное наполнение через [`demo-data-seeding`](../demo-data-seeding/INDEX.md). SSOT исполнения — pipeline-копия.
- **Приоритет:** P3 (понижен — НЕ блокер). По аудиту RC-05 read-canon уже мапит `promoted`→PUBLISHED на чтении, поэтому доска работает на текущих live-записях **без** этой миграции. RC-06 = гигиена: привести колонку `status` в соответствие read-выводу + S1 (пустой контент). См. [`audit-gw-rc-05-...`](../../../analysis/audit-gw-rc-05-status-vocabulary-canonicalization-2026-06-20.md) §G1.
- **Тип:** data / ops
- **Закрывает:** reopened GAP-2 на уровне ДАННЫХ (5 записей с `promoted`) + S1 (пустой `title_json`/`summary_json`)
- **Основание:** [`CLOSURE`](./CLOSURE-empty-board-status-vocabulary-2026-06-20.md) · [`investigation`](./investigation-empty-board-status-vocabulary-2026-06-20.md) §Recommended fixes 3, §Secondary S1 · [`interview`](./interview-rc05-rc06-status-vocabulary-2026-06-20.md) (D-RC05-2/3)
- **Зависит от:** [GW-RC-05](./STORY-GW-RC-05-status-vocabulary-canonicalization.md) (сначала код-фикс, чтобы новые записи были чистыми)

## Зачем простыми словами
Даже после код-фикса (RC-05) **уже лежащие** на hosted 5 записей имеют `status='promoted'` и у 4 из 5 пустой текст (`title_json`/`summary_json`). Их надо привести в порядок, чтобы текущая доска показала осмысленные карточки.

## Что наблюдаю сейчас (verified, post-P3 2026-06-20)

- Hosted `doge_issues`: **1** запись `test-7ef193be-dc51-4ddb-a582-24a6977dfd51`, `status='PUBLISHED'`, title en/et/ru populated ([T04 live response](../../epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-06-hosted-status-data-hygiene/task-gw-rc-06-t04-verify-tallinn-issues-and-board-cards/tallinn-issues-live-response.json)).
- 4 пустых test-seed (`test-*`, empty content, 0 `issue_story_links`) **удалены**; backup в T01 ([`hosted-doge-issues-backup-pre-status-migration.json`](../../epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-06-hosted-status-data-hygiene/task-gw-rc-06-t01-backup-and-hosted-status-migration-promoted-to-published/hosted-doge-issues-backup-pre-status-migration.json)).
- До P3 (investigation E3): 5× `promoted`, 4/5 `title_json={}` — см. [`investigation E3`](./investigation-empty-board-status-vocabulary-2026-06-20.md).

## Требование / целевое состояние (D-RC05-2/3)
- **Status-миграция (сейчас):** `UPDATE public.doge_issues SET status='PUBLISHED' WHERE status='promoted'` на hosted Supabase. (После RC-05 новые записи уже чистые; это — для существующих.)
- **S1 (пустой контент):** для записей с пустым `title_json`/`summary_json` — ре-проджектинг из связанных историй (если есть линки) либо пометить как тестовый мусор/удалить. Решить по факту наличия `issue_story_links`.
- **Проверка:** `GET /tallinn/issues` → `status` board-valid и непустой текст; SPA-доска показывает карточки.

## Граница
- Только данные на hosted; код — в RC-05.
- Если контент восстановить нельзя (нет линков на истории) — зафиксировать как тестовый seed (не продакшн-данные), чистый набор придёт через пакет demo-data-seeding.

## Подзадачи (черновик)
- **T01** — Резервная выгрузка текущих 5 записей (на всякий) → SQL `UPDATE promoted→PUBLISHED` на hosted.
- **T02** — Аудит пустого контента: у каких записей есть `issue_story_links` для ре-проджектинга.
- **T03** — Ре-проджектинг восстановимых; для невосстановимых — решение (оставить/удалить как test-seed).
- **T04** — Верификация: `curl /tallinn/issues` → board-status + непустой текст; скрин доски.

## Acceptance Criteria
- [x] На hosted нет `doge_issues.status='promoted'` (все board-vocab). — T01 post-check 0 promoted; gate PASS 2026-06-20.
- [x] Записи с пустым контентом либо ре-проджектнуты, либо явно помечены как test-seed/удалены. — 0 recoverable; 4 empty test-* deleted (T03); backup T01.
- [x] `GET /tallinn/issues` отдаёт валидные карточки; доска не пустая. — 1 issue `PUBLISHED`, title populated (T04).

## Открытые вопросы (closed P3/P5 2026-06-21)
- ~~Доступ к hosted Supabase~~ — `doge-complaints-gateway/.env` (`SUPABASE_URL`, `SUPABASE_SERVICE_ROLE`); ops выполнены в P3.
- ~~test-* demo vs мусор~~ — 4 empty без links удалены как integration garbage; 1 populated row сохранена; полный демо-набор — [`demo-data-seeding`](../demo-data-seeding/INDEX.md).
