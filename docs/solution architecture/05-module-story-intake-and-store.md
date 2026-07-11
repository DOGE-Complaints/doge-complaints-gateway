# 05. Module: Story Intake & Story Store

## Responsibilities
- Сохранить story как immutable первичное свидетельство.
- Принять optional structured signals без потери original narrative.
- Поддержать readiness-состояния (partial, cluster-ready, projection-ready).
- Сохранить origin linkage (GPT intake reference, timestamps, version).
- Сохранить **авторство**: `submitter.external_user_id` (opaque, формат не фиксируется) и при необходимости `identity_issuer` из OAuth на стороне GPT/IdP — в `story_origin` или связанной сущности без потери на intake.

## Data model (logical)
- `stories` (immutable narrative core).
- `story_versions` (normalization/enrichment revisions).
- `story_origin` (source metadata + **внешний субъект/автор** при логине через GPT).
- `story_status` (readiness lifecycle).

## StoryRecord — целевые поля (v2, решения интервью 2026-05-13)

| Поле | Тип | Новое? | Описание |
|------|-----|--------|----------|
| `narrative_title` | `dict[str,str]` | ✅ Новое | `{et,ru,en}`, обязательное; заменяет `narrative_title_hint` и `narrative_title_hint_et/ru/en` |
| `narrative_description` | `dict[str,str]` | ✅ Новое | `{et,ru,en}`, обязательное |
| `narrative_summary` | `dict[str,str] \| None` | ✅ Новое | `{et,ru,en}`, опциональное; заменяет `summary_languages: tuple[tuple[str,str],...]` |
| `narrative_session_language` | `str \| None` | ✅ Новое | `"et"\|"ru"\|"en"` — primary язык сессии GPT |
| `narrative_title_hint` | — | ❌ Удалить | Заменено на `narrative_title` |
| `narrative_title_hint_et/ru/en` | — | ❌ Удалить | Заменено на `narrative_title` dict |
| `submitter_identity_issuer` | `str` (not None) | ♻️ Изменить | Из `str \| None` → обязательное (eID gate) |

## Lifecycle states
`ACCEPTED` → `PARTIAL_READY` → `READY_FOR_PROFILE` → `CLUSTERED`

(В demo: `PARTIAL_READY` не допустим как конечный — HTTP 400 при отсутствии обязательных полей)

## Storage rules
- Original narrative never overwritten.
- Interpretation fields versioned.
- PII fields optional and isolated by classification tier.
- `narrative_original_text` никогда не логируется целиком — применяется `redact_pii()` если `privacy.contains_pii=True` (G-06).

## Migration strategy from legacy
- Legacy `complaints` -> `stories` seed migration.
- Mapping table for old IDs to new story IDs.
- Dual-read period for validation.
- v1 → v2 schema migration: новые колонки `narrative_title`, `narrative_description`, `narrative_summary`, `narrative_session_language`; `identity_issuer` NOT NULL constraint.

## Решения интервью (2026-05-13)
Подробно: REQ-33, `docs/analysis/gap-interview-decisions-2026-05-13.md` G-01/G-07
