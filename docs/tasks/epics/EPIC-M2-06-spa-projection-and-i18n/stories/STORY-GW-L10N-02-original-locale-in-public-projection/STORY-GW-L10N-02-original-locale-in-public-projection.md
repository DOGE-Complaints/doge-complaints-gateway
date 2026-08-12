# STORY-GW-L10N-02 — `original_locale` в публичной проекции issue

## Meta
- **Key:** `STORY-GW-L10N-02`
- **Parent Epic:** [`../../../EPIC-M2-06-spa-projection-and-i18n.md`](../../../EPIC-M2-06-spa-projection-and-i18n.md)
- **Type:** Technical Story
- **Status:** 🔵 Done (Awaiting Commits)
- **source:** [`../../../../backlog-stories/localization-l10n/STORY-GW-L10N-02-original-locale-in-public-projection.md`](../../../../backlog-stories/localization-l10n/STORY-GW-L10N-02-original-locale-in-public-projection.md)
- **Закрывает:** REQ-BE-1 (поле для MT-маркера фронта)
- **Источник:** [REQUIREMENTS-BACKEND-L10N §REQ-BE-1](../../../../../../../spa-app/docs/tasks/backlog-stories/localization/REQUIREMENTS-BACKEND-L10N.md); решения D-L10N-1, D-L10N-2
- **Decision Ref:** backlog file above; [`localization-l10n/INDEX.md`](../../../../backlog-stories/localization-l10n/INDEX.md) D-L10N-2
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000028-20260603-gw-l10n-02-original-locale-in-public-projection.yaml`](../../../../gateway-active-packages/pkg-000028-20260603-gw-l10n-02-original-locale-in-public-projection.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **7** тасков T01–T07; audit follow-up **T08** вне pkg (`run_mode=gw_l10n_02_audit_followup`)
- **Зависит от:** [GW-L10N-01](../STORY-GW-L10N-01-projection-content-i18n-preservation/STORY-GW-L10N-01-projection-content-i18n-preservation.md) (иначе помечать нечего — локали идентичны)

## Зачем простыми словами
Фронт хочет показывать значок «машинный перевод» на тех языках, которые писал не человек, а автоперевод. Для этого ему нужно знать, **на каких языках issue реально был подан людьми**. Бэк это знает (язык каждой истории), но в публичный ответ это не отдаёт.

## Что наблюдаю сейчас (verified по коду)
- Язык-оригинал истории = `StoryRecord.narrative_language` ∈ `{et, ru, en}` (валидируется на intake, [contracts.py:198-245](../../../../../../../src/core/intake/contracts.py#L198-L245)).
- В точке сборки проекции доступны все истории кластера и их языки: [issue_create.py:140-160](../../../../../../../src/core/application/issue_create.py#L140-L160) (`cluster_stories: tuple[StoryRecord, ...]`).
- **Разрыв:** ни `ProjectionInput` ([input.py:8-30](../../../../../../../src/core/projection/input.py#L8-L30)), ни `DOGEIssue.to_public_dict()` ([dto.py:25-48](../../../../../../../src/core/projection/dto.py#L25-L48)) не несут язык-оригинал. `grep original|locale|lang` по `dto.py` = 0.
- Проекция — `payload_json` (JSON) → **миграция схемы не нужна**, поле идёт в JSON.

## Требование / целевое состояние (решение D-L10N-2)
- Добавить в публичную проекцию issue поле **`original_locale`** = **список** различных языков-оригиналов всех историй кластера (например `["et", "ru"]`).
- Семантика для фронта: локали из списка — «есть человеческий оригинал»; локали **вне** списка фронт помечает как MT.
- Поле приходит и в списке (`GET /tallinn/issues`), и в одиночном (`GET /tallinn/issues/{id}`).
- Значения — из согласованного набора локалей `{et, ru, en}`, дедуп, стабильный порядок (напр. по появлению или алфавиту).

## Контракт со стороны фронта (приёмка FE-POV)
- Фронт читает `original_locale: string[]`; локали из списка показывает без MT-маркера, остальные — с маркером (L10N-03 на фронте).
- Если поле отсутствует/пустой массив — фронт деградирует мягко (не показывает маркер, не падает). Поле желательно, но не критично для рендера.

## Product decisions (fixed, P1 materialization)
- **Пустое / неизвестно:** опускать поле в public dict (не `[]`); FE soft-degrade.
- **Порядок элементов:** канонический `et`, `ru`, `en` — в список попадают только присутствующие уникальные `narrative_language` из кластера.
- **Дедуп:** уникальные значения из `{et, ru, en}`.
- **Источник языков:** все `cluster_stories`, не только dominant (D-L10N-2).

## Out of scope
- GW-L10N-03/04 (телеметрия, реестр меток)
- SPA L10N-03 (MT UI на фронте)
- DDL / schema migration
- Изменение семантики `title` / `summary` / `description` (GW-L10N-01)

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-l10n-02-t01-compute-original-locale-projection-input`](./task-gw-l10n-02-t01-compute-original-locale-projection-input/README.md) | pkg-000028 |
| 2 | [`task-gw-l10n-02-t02-doge-issue-public-dict-original-locale`](./task-gw-l10n-02-t02-doge-issue-public-dict-original-locale/README.md) | pkg-000028 |
| 3 | [`task-gw-l10n-02-t03-manual-post-original-locale`](./task-gw-l10n-02-t03-manual-post-original-locale/README.md) | pkg-000028 |
| 4 | [`task-gw-l10n-02-t04-reproject-backfill-original-locale`](./task-gw-l10n-02-t04-reproject-backfill-original-locale/README.md) | pkg-000028 |
| 5 | [`task-gw-l10n-02-t05-openapi-api-reference-original-locale`](./task-gw-l10n-02-t05-openapi-api-reference-original-locale/README.md) | pkg-000028 |
| 6 | [`task-gw-l10n-02-t06-original-locale-acceptance-tests`](./task-gw-l10n-02-t06-original-locale-acceptance-tests/README.md) | pkg-000028 |
| 7 | [`task-gw-l10n-02-t07-story-acceptance-gate`](./task-gw-l10n-02-t07-story-acceptance-gate/README.md) | pkg-000028 |
| 8 | [`task-gw-l10n-02-t08-reproject-backfill-original-locale-assertion`](./task-gw-l10n-02-t08-reproject-backfill-original-locale-assertion/README.md) | audit override (`run_mode=gw_l10n_02_audit_followup`) |

## Acceptance Criteria
- [x] `GET /tallinn/issues` и `/{id}` возвращают `original_locale: string[]` из `{et,ru,en}`.
- [x] Для смешанного кластера список содержит все различные языки историй; дедуп; стабильный порядок.
- [x] Поле опускается (или пустой массив по согласованию) когда язык неизвестен — фронт не падает.
- [x] openapi/API_REFERENCE описывают поле и семантику.
- [x] Тест-суит без регрессий.

## Открытые вопросы к аналитике
- Пустое значение: опускать поле или отдавать `[]`? (фронт обрабатывает оба — выбрать одно для консистентности). → **Закрыто P1:** опускать поле.
- Порядок элементов списка: по появлению в кластере или алфавитный? → **Закрыто P1:** канонический `et`, `ru`, `en`.

**Gate:** [`story-acceptance-gate-STORY-GW-L10N-02.md`](./story-acceptance-gate-STORY-GW-L10N-02.md) — PASS 2026-06-15 (remediated; prior 2026-05-29 invalid)
