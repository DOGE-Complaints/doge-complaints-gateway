# STORY-GW-L10N-01 — Сохранение реального мультиязычного контента в проекции

## Meta
- **Key:** `STORY-GW-L10N-01`
- **Status:** 🔵 Done (Awaiting Commits) — исполнено через pipeline ([pkg-000027](../../gateway-active-packages/pkg-000027-20260603-gw-l10n-01-projection-content-i18n-preservation.yaml), T01–T06, gate PASS 2026-06-15); код-аудит [`audit-gw-l10n-01-...-2026-06-15.md`](../../../analysis/audit-gw-l10n-01-projection-content-i18n-2026-06-15.md) (verified; open: G1 backfill-test, G2 cluster-E2E-test). Этот backlog-файл — исходная проработка; SSOT исполнения — pipeline-копия в `epics/EPIC-M2-06-.../stories/STORY-GW-L10N-01-.../`.
- **Закрывает:** основу REQ-BE-1 (без неё MT-маркер фронта бессмысленен)
- **Источник:** [REQUIREMENTS-BACKEND-L10N §REQ-BE-1](../../../../../spa-app/docs/tasks/backlog-stories/localization/REQUIREMENTS-BACKEND-L10N.md); решение D-L10N-1
- **Зависит от:** —
- **Разблокирует:** [GW-L10N-02](./STORY-GW-L10N-02-original-locale-in-public-projection.md) (original_locale)

## Зачем простыми словами
Пользователь читает issue на своём языке. Сейчас бэк показывает один и тот же текст во всех трёх языках (et=ru=en — буквальные копии), хотя на приёме (intake) от GPT приходил настоящий перевод на 3 языка. Фронт хочет отличать «оригинал автора» от «машинного перевода», но пока отличать нечего — все локали одинаковы. Эта стори чинит корень: проекция должна сохранять реальный мультиязычный контент, а не схлопывать его в одну строку.

## Что наблюдаю сейчас (verified по коду)
- На intake `narrative.title` и `narrative.description` — обязательные i18n-объекты во всех языках (`parse_required_i18n_dict`), [contracts.py:248-258](../../../../src/core/intake/contracts.py#L248-L258). То есть реальный 3-язычный контент в системе есть.
- Он сохраняется в `StoryRecord.narrative_title` / `narrative_description` / `narrative_summary` (i18n dict).
- **Разрыв:** при сборке проекции контент схлопывается. `build_draft` принимает один `promoted_title: str` и `aggregate_text: str`, а `_to_i18n(text)` кладёт одну строку во все три слота: [extraction_policy.py:108-145](../../../../src/core/projection/extraction_policy.py#L108-L145), [:171-175](../../../../src/core/projection/extraction_policy.py#L171-L175).
- При этом доминантная история (выбрана по `alpha_score`) с её полным i18n-контентом **доступна** в точке сборки: [issue_create.py:140-160](../../../../src/core/application/issue_create.py#L140-L160) (`dominant_story` — это `StoryRecord`).
- Проекция хранится как `payload_json` (JSON), [db_supabase.py:638-712](../../../../src/core/infrastructure/db_supabase.py#L638-L712) → **схема БД не меняется**, новый контент идёт внутрь JSON.

## Требование / целевое состояние
- Публичная проекция issue должна нести **реальный** мультиязычный `title` / `description` / `summary` (i18n `{et,ru,en}`), а не идентичные копии.
- Источник контента: **i18n-контент доминантной истории кластера** (`dominant_story.narrative_title/description/summary`) — согласуется с тем, что доминантная история уже определяет заглавный контент issue.
- Манульный путь оператора (`POST /tallinn/issues`) тоже должен сохранять i18n-контент, если он передан (сейчас флэттенит через `_promoted_title_from_i18n`, [issue_create.py:376-405](../../../../src/core/application/issue_create.py#L376-L405)).

## Граница и контракт
- Меняется только наполнение i18n-полей проекции. Имена полей `title/summary/description` и форма `{et,ru,en}` — **без изменений** (фронт уже читает эту форму).
- Поведение фильтров/поиска не затрагивается (поиск client-side по тексту — см. [STORY-SPA-G3](../../../../../spa-app/docs/tasks/backlog-stories/STORY-SPA-G3-search-input-toolbar.md)).

## Подзадачи (черновик)
- **T01** — В `build_draft` / `build_projection_input_from_draft` прокинуть i18n-контент доминантной истории вместо `_to_i18n(promoted_title)`; сохранить fallback на текущее поведение, если у истории нет валидного i18n.
- **T02** — Манульный `POST /tallinn/issues`: сохранять переданный i18n-`title` без флэттена.
- **T03** — Бэкфилл: ре-проджектинг существующих issue, чтобы старые `payload_json` получили реальный контент (либо явно зафиксировать, что старые остаются копиями).
- **T04** — Acceptance-тесты: проекция кластера, где истории имеют разный текст по локалям → `title.et != title.en` при реально разном контенте; fallback при отсутствии i18n.
- **T05** — Обновить `API_REFERENCE §7` / `openapi.yaml`: пояснить, что локали могут различаться и какая считается оригиналом (cross-ref на GW-L10N-02).

## Acceptance Criteria
- [ ] Для issue, чьи истории имеют разный контент по локалям, проекция отдаёт **различающиеся** `title/description/summary` по `{et,ru,en}` (не копии).
- [ ] Источник — доминантная история кластера; при отсутствии валидного i18n используется текущий безопасный fallback (без падений).
- [ ] Манульный `POST /tallinn/issues` сохраняет i18n-`title`.
- [ ] Решён вопрос бэкфилла существующих issue (ре-проджектинг или зафиксированное исключение).
- [ ] Тест-суит без регрессий; добавлены тесты на различимость локалей и fallback.

## Открытые вопросы к аналитике
- Контент берём из **доминантной** истории — подтвердить (альтернатива: мердж по локалям, но title мерджить нельзя осмысленно).
- Если у доминантной истории заполнен не весь i18n — добиваем из других историй кластера или оставляем как есть?
