# STORY-GW-L10N-01 — Сохранение реального мультиязычного контента в проекции

## Meta
- **Key:** `STORY-GW-L10N-01`
- **Parent Epic:** [`../../../EPIC-M2-06-spa-projection-and-i18n.md`](../../../EPIC-M2-06-spa-projection-and-i18n.md)
- **Type:** Technical Story
- **Status:** ⚪ Todo
- **source:** [`../../../../backlog-stories/localization-l10n/STORY-GW-L10N-01-projection-content-i18n-preservation.md`](../../../../backlog-stories/localization-l10n/STORY-GW-L10N-01-projection-content-i18n-preservation.md)
- **Закрывает:** основу REQ-BE-1 (без неё MT-маркер фронта бессмысленен)
- **Источник:** [REQUIREMENTS-BACKEND-L10N §REQ-BE-1](../../../../../../../spa-app/docs/tasks/backlog-stories/localization/REQUIREMENTS-BACKEND-L10N.md); решение D-L10N-1
- **Decision Ref:** backlog file above; [`localization-l10n/INDEX.md`](../../../../backlog-stories/localization-l10n/INDEX.md) D-L10N-1
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000027-20260603-gw-l10n-01-projection-content-i18n-preservation.yaml`](../../../../gateway-active-packages/pkg-000027-20260603-gw-l10n-01-projection-content-i18n-preservation.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **6** тасков T01–T06
- **Зависит от:** —
- **Разблокирует:** [GW-L10N-02](../../../../backlog-stories/localization-l10n/STORY-GW-L10N-02-original-locale-in-public-projection.md) (original_locale)

## Зачем простыми словами
Пользователь читает issue на своём языке. Сейчас бэк показывает один и тот же текст во всех трёх языках (et=ru=en — буквальные копии), хотя на приёме (intake) от GPT приходил настоящий перевод на 3 языка. Фронт хочет отличать «оригинал автора» от «машинного перевода», но пока отличать нечего — все локали одинаковы. Эта стори чинит корень: проекция должна сохранять реальный мультиязычный контент, а не схлопывать его в одну строку.

## Что наблюдаю сейчас (verified по коду)
- На intake `narrative.title` и `narrative.description` — обязательные i18n-объекты во всех языках (`parse_required_i18n_dict`), [contracts.py:248-258](../../../../../../../src/core/intake/contracts.py#L248-L258). То есть реальный 3-язычный контент в системе есть.
- Он сохраняется в `StoryRecord.narrative_title` / `narrative_description` / `narrative_summary` (i18n dict).
- **Разрыв:** при сборке проекции контент схлопывается. `build_draft` принимает один `promoted_title: str` и `aggregate_text: str`, а `_to_i18n(text)` кладёт одну строку во все три слота: [extraction_policy.py:108-145](../../../../../../../src/core/projection/extraction_policy.py#L108-L145), [:171-175](../../../../../../../src/core/projection/extraction_policy.py#L171-L175).
- При этом доминантная история (выбрана по `alpha_score`) с её полным i18n-контентом **доступна** в точке сборки: [issue_create.py:140-160](../../../../../../../src/core/application/issue_create.py#L140-L160) (`dominant_story` — это `StoryRecord`).
- Проекция хранится как `payload_json` (JSON), [db_supabase.py:638-712](../../../../../../../src/core/infrastructure/db_supabase.py#L638-L712) → **схема БД не меняется**, новый контент идёт внутрь JSON.

## Требование / целевое состояние
- Публичная проекция issue должна нести **реальный** мультиязычный `title` / `description` / `summary` (i18n `{et,ru,en}`), а не идентичные копии.
- Источник контента: **i18n-контент доминантной истории кластера** (`dominant_story.narrative_title/description/summary`) — согласуется с тем, что доминантная история уже определяет заглавный контент issue.
- Манульный путь оператора (`POST /tallinn/issues`) тоже должен сохранять i18n-контент, если он передан (сейчас флэттенит через `_promoted_title_from_i18n`, [issue_create.py:376-405](../../../../../../../src/core/application/issue_create.py#L376-L405)).

## Граница и контракт
- Меняется только наполнение i18n-полей проекции. Имена полей `title/summary/description` и форма `{et,ru,en}` — **без изменений** (фронт уже читает эту форму).
- Поведение фильтров/поиска не затрагивается (поиск client-side по тексту — см. [STORY-SPA-G3](../../../../../../../spa-app/docs/tasks/backlog-stories/STORY-SPA-G3-search-input-toolbar.md)).

## Product decisions (fixed, P1 materialization)
- **Partial i18n:** только `dominant_story`; пустые слоты → текущий безопасный fallback (`_to_i18n` на `promoted_title` / `aggregate_text`), **без** merge из других stories кластера.
- **Backfill:** one-off re-project script пересобирает `payload_json` существующих issue из `issue_story_links` + stories.

## Out of scope
- `original_locale` (GW-L10N-02)
- GW-L10N-03/04 (телеметрия, реестр меток)
- Изменения SPA
- DDL / schema migration
- Фильтры/поиск на бэке

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-l10n-01-t01-extraction-policy-dominant-i18n`](./task-gw-l10n-01-t01-extraction-policy-dominant-i18n/README.md) | pkg-000027 |
| 2 | [`task-gw-l10n-01-t02-manual-post-preserve-i18n-title`](./task-gw-l10n-01-t02-manual-post-preserve-i18n-title/README.md) | pkg-000027 |
| 3 | [`task-gw-l10n-01-t03-backfill-reproject-existing-issues`](./task-gw-l10n-01-t03-backfill-reproject-existing-issues/README.md) | pkg-000027 |
| 4 | [`task-gw-l10n-01-t04-projection-i18n-acceptance-tests`](./task-gw-l10n-01-t04-projection-i18n-acceptance-tests/README.md) | pkg-000027 |
| 5 | [`task-gw-l10n-01-t05-api-reference-openapi-i18n-locales`](./task-gw-l10n-01-t05-api-reference-openapi-i18n-locales/README.md) | pkg-000027 |
| 6 | [`task-gw-l10n-01-t06-story-acceptance-gate`](./task-gw-l10n-01-t06-story-acceptance-gate/README.md) | pkg-000027 |
| 7 | [`task-gw-l10n-01-t07-reproject-script-autotests`](./task-gw-l10n-01-t07-reproject-script-autotests/README.md) | audit override (`run_mode=gw_l10n_01_audit_followup`) |
| 8 | [`task-gw-l10n-01-t08-cluster-bridge-projection-i18n-e2e`](./task-gw-l10n-01-t08-cluster-bridge-projection-i18n-e2e/README.md) | audit override (`run_mode=gw_l10n_01_audit_followup`) |

## Post-audit gaps (P5 scaffold 2026-06-15)

Источник: [`audit-gw-l10n-01-projection-content-i18n-2026-06-15.md`](../../../../analysis/audit-gw-l10n-01-projection-content-i18n-2026-06-15.md) §3.

| Gap | Task | Status |
|-----|------|--------|
| G1 backfill script без автотеста | T07 | Done (audit follow-up) |
| G2 cluster bridge E2E не verified | T08 | Done (audit follow-up) |
| G3 `original_locale` | — | scope GW-L10N-02 |

Исполнение T07–T08: `run_mode=gw_l10n_01_audit_followup` в [Gateway_builder.plan.md](../../../../../../../.cursor/plans/Gateway_builder.plan.md); YAML default остаётся `pkg-000027`.
- [ ] Для issue, чьи истории имеют разный контент по локалям, проекция отдаёт **различающиеся** `title/description/summary` по `{et,ru,en}` (не копии).
- [ ] Источник — доминантная история кластера; при отсутствии валидного i18n используется текущий безопасный fallback (без падений).
- [ ] Манульный `POST /tallinn/issues` сохраняет i18n-`title`.
- [ ] Решён вопрос бэкфилла существующих issue (ре-проджектинг или зафиксированное исключение).
- [ ] Тест-суит без регрессий; добавлены тесты на различимость локалей и fallback.

## Открытые вопросы к аналитике
- Контент берём из **доминантной** истории — подтвердить (альтернатива: мердж по локалям, но title мерджить нельзя осмысленно).
- Если у доминантной истории заполнен не весь i18n — добиваем из других историй кластера или оставляем как есть?

**Gate:** [`story-acceptance-gate-STORY-GW-L10N-01.md`](./story-acceptance-gate-STORY-GW-L10N-01.md) — Todo

## Traceability: parent AC → tasks

| Parent AC | Tasks |
|-----------|-------|
| Различающиеся title/description/summary | T01, T04, T06 |
| Dominant + fallback | T01, T04, T06 |
| Manual POST i18n-title | T02, T04, T06 |
| Бэкфилл | T03, T06 |
| Тесты без регрессий | T04, T06 |
