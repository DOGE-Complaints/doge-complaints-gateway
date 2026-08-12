# STORY-GW-L10N-02 — `original_locale` в публичной проекции issue

## Meta
- **Key:** `STORY-GW-L10N-02`
- **Status:** 🔵 Done (Awaiting Commits) — pipeline [`STORY-GW-L10N-02`](../../epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-L10N-02-original-locale-in-public-projection/STORY-GW-L10N-02-original-locale-in-public-projection.md) · [`pkg-000028`](../../gateway-active-packages/pkg-000028-20260603-gw-l10n-02-original-locale-in-public-projection.yaml) T01–T08; gate PASS 2026-06-15 (remediated); [`audit-gw-l10n-02-acceptance-date-remediation-2026-06-15.md`](../../../analysis/audit-gw-l10n-02-acceptance-date-remediation-2026-06-15.md).
- **Закрывает:** REQ-BE-1 (поле для MT-маркера фронта)
- **Источник:** [REQUIREMENTS-BACKEND-L10N §REQ-BE-1](../../../../../spa-app/docs/tasks/backlog-stories/localization/REQUIREMENTS-BACKEND-L10N.md); решения D-L10N-1, D-L10N-2
- **Зависит от:** [GW-L10N-01](./STORY-GW-L10N-01-projection-content-i18n-preservation.md) (иначе помечать нечего — локали идентичны)

## Зачем простыми словами
Фронт хочет показывать значок «машинный перевод» на тех языках, которые писал не человек, а автоперевод. Для этого ему нужно знать, **на каких языках issue реально был подан людьми**. Бэк это знает (язык каждой истории), но в публичный ответ это не отдаёт.

## Что наблюдаю сейчас (verified по коду)
- Язык-оригинал истории = `StoryRecord.narrative_language` ∈ `{et, ru, en}` (валидируется на intake, [contracts.py:198-245](../../../../src/core/intake/contracts.py#L198-L245)).
- В точке сборки проекции доступны все истории кластера и их языки: [issue_create.py:140-160](../../../../src/core/application/issue_create.py#L140-L160) (`cluster_stories: tuple[StoryRecord, ...]`).
- **Разрыв:** ни `ProjectionInput` ([input.py:8-30](../../../../src/core/projection/input.py#L8-L30)), ни `DOGEIssue.to_public_dict()` ([dto.py:25-48](../../../../src/core/projection/dto.py#L25-L48)) не несут язык-оригинал. `grep original|locale|lang` по `dto.py` = 0.
- Проекция — `payload_json` (JSON) → **миграция схемы не нужна**, поле идёт в JSON.

## Требование / целевое состояние (решение D-L10N-2)
- Добавить в публичную проекцию issue поле **`original_locale`** = **список** различных языков-оригиналов всех историй кластера (например `["et", "ru"]`).
- Семантика для фронта: локали из списка — «есть человеческий оригинал»; локали **вне** списка фронт помечает как MT.
- Поле приходит и в списке (`GET /tallinn/issues`), и в одиночном (`GET /tallinn/issues/{id}`).
- Значения — из согласованного набора локалей `{et, ru, en}`, дедуп, стабильный порядок (напр. по появлению или алфавиту).

## Контракт со стороны фронта (приёмка FE-POV)
- Фронт читает `original_locale: string[]`; локали из списка показывает без MT-маркера, остальные — с маркером (L10N-03 на фронте).
- Если поле отсутствует/пустой массив — фронт деградирует мягко (не показывает маркер, не падает). Поле желательно, но не критично для рендера.

## Подзадачи (черновик)
- **T01** — Вычислять `original_locale` = уникальные `narrative_language` по `cluster_stories`; прокинуть в `ProjectionInput`.
- **T02** — Добавить поле в `DOGEIssue` + `to_public_dict()` (опускать при пустом, как остальные опциональные поля).
- **T03** — Манульный `POST /tallinn/issues`: вычислять из `story_ids` (языки указанных историй).
- **T04** — Бэкфилл существующих issue (ре-проджектинг; общий с GW-L10N-01).
- **T05** — `openapi.yaml` + `API_REFERENCE §6/§7`: описать `original_locale` (тип `string[]`, enum значений, семантика «человеческий оригинал»).
- **T06** — Acceptance-тесты: моно-язычный кластер → `["et"]`; смешанный → `["et","ru"]`; форма в обоих endpoint.

## Acceptance Criteria
- [ ] `GET /tallinn/issues` и `/{id}` возвращают `original_locale: string[]` из `{et,ru,en}`.
- [ ] Для смешанного кластера список содержит все различные языки историй; дедуп; стабильный порядок.
- [ ] Поле опускается (или пустой массив по согласованию) когда язык неизвестен — фронт не падает.
- [ ] openapi/API_REFERENCE описывают поле и семантику.
- [ ] Тест-суит без регрессий.

## Открытые вопросы к аналитике
- Пустое значение: опускать поле или отдавать `[]`? (фронт обрабатывает оба — выбрать одно для консистентности).
- Порядок элементов списка: по появлению в кластере или алфавитный? (для предсказуемости снапшот-тестов).
