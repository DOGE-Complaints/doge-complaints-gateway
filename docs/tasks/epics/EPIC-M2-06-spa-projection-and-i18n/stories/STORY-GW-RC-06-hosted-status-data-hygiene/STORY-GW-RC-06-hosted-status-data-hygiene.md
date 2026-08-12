# STORY-GW-RC-06 — Гигиена hosted-данных: status-миграция + пустой контент (S1)

## Meta
- **Key:** `STORY-GW-RC-06`
- **Parent Epic:** [`../../../EPIC-M2-06-spa-projection-and-i18n.md`](../../../EPIC-M2-06-spa-projection-and-i18n.md)
- **Type:** Technical Story
- **Status:** 🔵 Done (Awaiting Commits) — gate PASS 2026-06-20; code audit [`audit-gw-rc-06-hosted-status-data-hygiene-2026-06-21.md`](../../../../../../analysis/audit-gw-rc-06-hosted-status-data-hygiene-2026-06-21.md) (P5 activation none 2026-06-21); **пакет issues-read-contract RC-01→06 закрыт**
- **Приоритет:** P3 (понижен — НЕ блокер). По аудиту RC-05 read-canon уже мапит `promoted`→PUBLISHED на чтении, поэтому доска работает на текущих live-записях **без** этой миграции. RC-06 = гигиена: привести колонку `status` в соответствие read-выводу + S1 (пустой контент). См. [`audit-gw-rc-05-...`](../../../../../../analysis/audit-gw-rc-05-status-vocabulary-canonicalization-2026-06-20.md) §G1.
- **Тип:** data / ops
- **source:** [`../../../../backlog-stories/issues-read-contract/STORY-GW-RC-06-hosted-status-data-hygiene.md`](../../../../backlog-stories/issues-read-contract/STORY-GW-RC-06-hosted-status-data-hygiene.md)
- **Закрывает:** reopened GAP-2 на уровне ДАННЫХ (5 записей с `promoted`) + S1 (пустой `title_json`/`summary_json`)
- **Основание:** [`CLOSURE`](../../../../backlog-stories/issues-read-contract/CLOSURE-empty-board-status-vocabulary-2026-06-20.md) · [`investigation`](../../../../backlog-stories/issues-read-contract/investigation-empty-board-status-vocabulary-2026-06-20.md) §Recommended fixes 3, §Secondary S1 · [`interview`](../../../../backlog-stories/issues-read-contract/interview-rc05-rc06-status-vocabulary-2026-06-20.md) (D-RC05-2/3)
- **Decision Ref:** backlog file above; [`interview-rc05-rc06-status-vocabulary-2026-06-20.md`](../../../../backlog-stories/issues-read-contract/interview-rc05-rc06-status-vocabulary-2026-06-20.md) — D-RC05-2/3
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000035-20260620-gw-rc-06-hosted-status-data-hygiene.yaml`](../../../../gateway-active-packages/pkg-000035-20260620-gw-rc-06-hosted-status-data-hygiene.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **5** тасков T01–T05
- **Зависит от:** [GW-RC-05](../STORY-GW-RC-05-status-vocabulary-canonicalization/STORY-GW-RC-05-status-vocabulary-canonicalization.md) (сначала код-фикс, чтобы новые записи были чистыми)
- **Парная:** [GW-RC-05](../STORY-GW-RC-05-status-vocabulary-canonicalization/STORY-GW-RC-05-status-vocabulary-canonicalization.md) (код)

## Зачем простыми словами
Даже после код-фикса (RC-05) **уже лежащие** на hosted 5 записей имеют `status='promoted'` и у 4 из 5 пустой текст (`title_json`/`summary_json`). Их надо привести в порядок, чтобы текущая доска показала осмысленные карточки.

## Что наблюдаю сейчас (verified, post-P3 2026-06-20)

- Hosted `doge_issues`: **1** запись `test-7ef193be-dc51-4ddb-a582-24a6977dfd51`, `status='PUBLISHED'`, title en/et/ru populated ([T04 live response](./task-gw-rc-06-t04-verify-tallinn-issues-and-board-cards/tallinn-issues-live-response.json)).
- 4 пустых test-seed удалены (T03); backup в T01 ([`hosted-doge-issues-backup-pre-status-migration.json`](./task-gw-rc-06-t01-backup-and-hosted-status-migration-promoted-to-published/hosted-doge-issues-backup-pre-status-migration.json)).
- До P3 (investigation E3): 5× `promoted`, 4/5 `title_json={}` — см. [`investigation E3`](../../../../backlog-stories/issues-read-contract/investigation-empty-board-status-vocabulary-2026-06-20.md).
- **G1 (post-audit):** доска = 1 карточка; полное наполнение → [`demo-data-seeding`](../../../../backlog-stories/demo-data-seeding/INDEX.md).

## Требование / целевое состояние (D-RC05-2/3)
- **Status-миграция (сейчас):** `UPDATE public.doge_issues SET status='PUBLISHED' WHERE status='promoted'` на hosted Supabase. (После RC-05 новые записи уже чистые; это — для существующих.)
- **S1 (пустой контент):** для записей с пустым `title_json`/`summary_json` — ре-проджектинг из связанных историй (если есть линки) либо пометить как тестовый мусор/удалить. Решить по факту наличия `issue_story_links`.
- **Проверка:** `GET /tallinn/issues` → `status` board-valid и непустой текст; SPA-доска показывает карточки.

## Out of scope
- Только данные на hosted; код — в RC-05.
- Если контент восстановить нельзя (нет линков на истории) — зафиксировать как тестовый seed (не продакшн-данные), чистый набор придёт через пакет demo-data-seeding.

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-rc-06-t01-backup-and-hosted-status-migration-promoted-to-published`](./task-gw-rc-06-t01-backup-and-hosted-status-migration-promoted-to-published/README.md) | pkg-000035 |
| 2 | [`task-gw-rc-06-t02-audit-empty-content-and-issue-story-links`](./task-gw-rc-06-t02-audit-empty-content-and-issue-story-links/README.md) | pkg-000035 |
| 3 | [`task-gw-rc-06-t03-reproject-recoverable-and-test-seed-decision`](./task-gw-rc-06-t03-reproject-recoverable-and-test-seed-decision/README.md) | pkg-000035 |
| 4 | [`task-gw-rc-06-t04-verify-tallinn-issues-and-board-cards`](./task-gw-rc-06-t04-verify-tallinn-issues-and-board-cards/README.md) | pkg-000035 |
| 5 | [`task-gw-rc-06-t05-story-acceptance-gate`](./task-gw-rc-06-t05-story-acceptance-gate/README.md) | pkg-000035 |

## Acceptance Criteria
- [x] На hosted нет `doge_issues.status='promoted'` (все board-vocab).
- [x] Записи с пустым контентом либо ре-проджектнуты, либо явно помечены как test-seed/удалены.
- [x] `GET /tallinn/issues` отдаёт валидные карточки; доска не пустая.

## Открытые вопросы (closed P3/P5 2026-06-21)
- ~~Доступ к hosted Supabase~~ — `.env` SUPABASE_SERVICE_ROLE; ops выполнены в P3.
- ~~test-* demo vs мусор~~ — 4 empty без links удалены; 1 populated row сохранена; полный демо-набор — [`demo-data-seeding`](../../../../backlog-stories/demo-data-seeding/INDEX.md).
