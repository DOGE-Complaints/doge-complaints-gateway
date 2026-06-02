# REQ-46: Demo backend — geo expansion, intake_notes, logging transparency

**Статус:** requirements — ready for tasking  
**Источник:** `GPT UI/docs/analysis/1.06.26-testing-gap-report.md` + code audit 2026-05-28 + PM/CTO interview 2026-05-28  
**Дата:** 2026-05-28 (обновлён от 2026-06-01)  
**Приоритет:** P2  
**Тип:** backend code patch — services.py, geo/providers.py, intake/contracts.py, handlers.py, openapi.yaml, API_REFERENCE.md, db_supabase.py, db_sqlite.py  
**Парный REQ:** REQ-47 (операционные задачи: Railway + GPT-скрипты)  
**Зависит от:** REQ-37 (logging), REQ-42 (gpt_signals), REQ-33 (v2 narrative schema)

---

## 1. Контекст

Код-аудит тест-прогона `2026-06-01` (story_id `d295ed9f`) выявил три класса проблем на стороне backend:

### 1.1 Geo: stub-провайдер слишком узкий

`geo/providers.py` содержит только **2 города** (Tallinn, Narva) и проверяет только **английское написание**:
```python
if "tallinn" in canonical_key  # не поймает "таллин", "таллинн"
if "narva" in canonical_key    # не поймает "нарва"
```

`normalize_location_query()` только lowercases и collapses whitespace — русские буквы остаются как есть. Поэтому `"Таллин"` → `"таллин"` → **не совпадает** с `"tallinn"`.

Geo-сервис в deployment ВСЕГДА подключён (`providers.py:235`). Пустые `geo_*` — следствие узкого stub, не отсутствия сервиса.

### 1.2 gpt_signals: тихое падение невидимо в ответе

`services.py:93-112`: при `story_signal_store is None` — silent return без логирования. При exception — `logger.warning("intake.gpt_signals_persist_failed")`. Но в обоих случаях API возвращает 202 без каких-либо hint что сигналы **не были сохранены**.

`story_signal_store` в production с Supabase backend никогда не None (`providers.py:187`). Тихое падение сигналов означает exception при Supabase-записи — warning уходит в Railway stderr, но GPT-оркестратор об этом не знает.

### 1.3 Ответ API непрозрачен

`build_story_intake_response()` (`intake/contracts.py:358-369`) возвращает только `story_id` и `status`. Нет никакого сигнала:
- был ли определён geo (или пропущен)
- были ли сохранены gpt_signals

### 1.4 narrative_title_hint* — legacy write nulls

`db_supabase.py:464-467` явно пишет `None` для 4 legacy-колонок при каждом save. Код читает их как fallback при десериализации, но поскольку все текущие записи содержат null, они мертвы на практике. Требуется cleanup.

---

## 2. Решения (после PM/CTO interview)

### 2.1 Расширение geo stub-провайдера

**Файл:** `src/core/geo/providers.py`

Новый паттерн: словарь alias → snapshot вместо двух отдельных классов.

**Покрытие: топ-10 городов Эстонии + 9 районов Таллинна, 3 языка (EN/ET/RU):**

| Город/район | EN ключ | RU ключ | ET ключ |
|-------------|---------|---------|---------|
| Tallinn | `tallinn` | `таллин`, `таллинн` | `tallinn` |
| Tartu | `tartu` | `тарту` | `tartu` |
| Narva | `narva` | `нарва` | `narva` |
| Pärnu | `pärnu`, `parnu` | `пярну` | `pärnu` |
| Kohtla-Järve | `kohtla-järve`, `kohtla-jarve` | `кохтла-ярве` | `kohtla-järve` |
| Viljandi | `viljandi` | `вильянди` | `viljandi` |
| Rakvere | `rakvere` | `раквере` | `rakvere` |
| Maardu | `maardu` | `маарду` | `maardu` |
| Sillamäe | `sillamäe`, `sillamae` | `силламяэ` | `sillamäe` |
| Võru | `võru`, `voru` | `выру` | `võru` |
| Kalamaja (р-н) | `kalamaja` | `каламая` | `kalamaja` |
| Mustamäe (р-н) | `mustamäe`, `mustamae` | `мустамяэ` | `mustamäe` |
| Lasnamäe (р-н) | `lasnamäe`, `lasnamae` | `ласнамяэ` | `lasnamäe` |
| Kristiine (р-н) | `kristiine` | `кристийне` | `kristiine` |
| Põhja-Tallinn (р-н) | `põhja-tallinn`, `pohja-tallinn` | `пыхья-таллин` | `põhja-tallinn` |
| Haabersti (р-н) | `haabersti` | `хааберсти` | `haabersti` |
| Pirita (р-н) | `pirita` | `пирита` | `pirita` |
| Nõmme (р-н) | `nõmme`, `nomme` | `нымме` | `nõmme` |
| Kesklinn (р-н) | `kesklinn` | `кесклинн` | `kesklinn` |

**Архитектура реализации:**

```python
# Единый lookup dict: keyword → StoryGeoSnapshot
_GEO_LOOKUP: dict[str, StoryGeoSnapshot] = {
    "tallinn": StoryGeoSnapshot(normalized_label="Tallinn, EE", ..., admin_settlement="tallinn", admin_country="EE"),
    "таллин": StoryGeoSnapshot(normalized_label="Tallinn, EE", ..., admin_settlement="tallinn", admin_country="EE"),
    "таллинн": StoryGeoSnapshot(normalized_label="Tallinn, EE", ..., admin_settlement="tallinn", admin_country="EE"),
    "kalamaja": StoryGeoSnapshot(normalized_label="Kalamaja, Tallinn, EE", admin_district="kalamaja", admin_settlement="tallinn", ...),
    # ...
}

class _EstoniaGeoLookup:
    provider_id: str = "estonia_lookup_stub"

    def resolve(self, original_query: str, *, canonical_key: str) -> StoryGeoSnapshot | None:
        for keyword, snapshot in _GEO_LOOKUP.items():
            if keyword in canonical_key:
                return snapshot
        return None

def default_provider_chain() -> tuple[GeoProvider, ...]:
    return (_EstoniaGeoLookup(),)
```

### 2.2 Логирование — два уровня

**Файл:** `src/core/application/services.py`

**A. Geo miss → INFO вместо DEBUG** (когда location_query был передан, но geo не резолвился):

```python
# Было (только DEBUG):
if geo is None:
    logger.debug("intake.geo_skip", extra={"reason": "no_geo_or_not_resolved"})

# Стало:
if geo is None:
    if (request.narrative.location_query or "").strip():
        # location_query был, но не резолвился — это info-worthy
        logger.info(
            "intake.geo_not_resolved location_query=%s",
            (request.narrative.location_query or "")[:60],
            extra={"reason": "provider_miss", "location_query_len": len(request.narrative.location_query or "")},
        )
    else:
        logger.debug("intake.geo_skip", extra={"reason": "no_location_query"})
```

**B. gpt_signals drop → WARNING** (когда `store is None`):

```python
def _persist_gpt_classifier_signals(self, *, story_id: str, gpt_signals: GptSignalsBlock) -> None:
    if self.story_signal_store is None:
        logger.warning(
            "intake.gpt_signals_drop story_id=%s reason=signal_store_not_configured",
            story_id,
            extra={"story_id": story_id, "reason": "signal_store_not_configured", "outcome": "dropped"},
        )
        return
    # ... остальной код без изменений
```

### 2.3 `intake_notes` в ответе API

**Решение (после PM/CTO interview):** добавить в ответ 202 поле `intake_notes` с двумя boolean-флагами.

**Lockstep изменения (4 файла):**

#### A. `src/core/intake/contracts.py` — расширить `StoryIntakeResponse`

```python
# Добавить dataclass:
@dataclass(frozen=True)
class IntakeNotes:
    geo_resolved: bool
    gpt_signals_persisted: bool

    def as_dict(self) -> dict[str, Any]:
        return {"geo_resolved": self.geo_resolved, "gpt_signals_persisted": self.gpt_signals_persisted}

# Обновить StoryIntakeResponse:
@dataclass(frozen=True)
class StoryIntakeResponse:
    schema_version: str
    story_id: str
    status: str
    intake_notes: IntakeNotes | None = None  # опциональный

    def as_dict(self) -> dict[str, Any]:
        d = {"schema_version": self.schema_version, "story_id": self.story_id, "status": self.status}
        if self.intake_notes is not None:
            d["intake_notes"] = self.intake_notes.as_dict()
        return d

# Обновить build_story_intake_response():
def build_story_intake_response(
    *, story_id: str, status: str, trace_id: str,
    geo_resolved: bool = False,
    gpt_signals_persisted: bool | None = None,
) -> dict[str, Any]:
    notes = IntakeNotes(
        geo_resolved=geo_resolved,
        gpt_signals_persisted=gpt_signals_persisted if gpt_signals_persisted is not None else True,
    )
    contract = StoryIntakeResponse(
        schema_version=INTAKE_RESPONSE_SCHEMA_VERSION,
        story_id=story_id,
        status=status,
        intake_notes=notes,
    )
    return build_success_envelope(data=contract.as_dict(), trace_id=trace_id).as_dict()
```

#### B. `src/core/application/services.py` — вернуть флаги из create_story()

`create_story()` должен вернуть не только `StoryRecord`, но и `(StoryRecord, bool geo_resolved, bool gpt_signals_ok)` — или передавать флаги через `_persist_gpt_classifier_signals()`.

Альтернатива (менее инвазивная): добавить `geo_resolved` как поле `StoryRecord` (не персистируется) — но это загрязняет domain.

**Рекомендуемый подход:** добавить dataclass `StoryIntakeResult` в `services.py`:
```python
@dataclass(frozen=True)
class StoryIntakeResult:
    story: StoryRecord
    geo_resolved: bool
    gpt_signals_persisted: bool
```
`create_story()` → возвращает `StoryIntakeResult`.

#### C. `src/core/api/handlers.py` — передать флаги в build_story_intake_response()

```python
result = dependencies.story_intake_service.create_story(request, idempotency_key=idempotency_key)
return (
    build_story_intake_response(
        story_id=result.story.story_id,
        status=result.story.lifecycle_status.value,
        trace_id=resolved_trace_id,
        geo_resolved=result.geo_resolved,
        gpt_signals_persisted=result.gpt_signals_persisted,
    ),
    202,
)
```

#### D. `docs/runtime-docs/api-reference/openapi.yaml` и `API_REFERENCE.md`

В schema `SuccessEnvelope_StoryIntake.data` добавить:
```yaml
intake_notes:
  type: object
  properties:
    geo_resolved:
      type: boolean
      description: "True if location_query was resolved to geo coordinates"
    gpt_signals_persisted:
      type: boolean
      description: "True if gpt_signals block was successfully saved to story_signals"
```

### 2.4 narrative_title_hint* cleanup

**Условие:** выполнять только после верификации что все строки в таблице `stories` имеют null в этих колонках:
```sql
SELECT COUNT(*) FROM stories
WHERE narrative_title_hint IS NOT NULL
   OR narrative_title_hint_et IS NOT NULL
   OR narrative_title_hint_ru IS NOT NULL
   OR narrative_title_hint_en IS NOT NULL;
-- Ожидается: 0
```

Если 0 → выполнить:

**A. Migration SQL** (`supabase/migrations/YYYYMMDD_narrative_title_hint_cleanup.sql`):
```sql
ALTER TABLE stories
  DROP COLUMN IF EXISTS narrative_title_hint,
  DROP COLUMN IF EXISTS narrative_title_hint_et,
  DROP COLUMN IF EXISTS narrative_title_hint_ru,
  DROP COLUMN IF EXISTS narrative_title_hint_en;
```

**B. `src/core/infrastructure/db_supabase.py`:** удалить из `_STORY_SELECT_FIELDS`, удалить из `save_story()` row dict, удалить из `_i18n_dict_from_supabase_row()` fallback logic.

**C. `src/core/infrastructure/db_sqlite.py`:** удалить из CREATE TABLE, ALTER TABLE schema, INSERT, UPDATE, SELECT.

---

## 3. Файлы для изменения

| Файл | Изменение | Scope |
|------|-----------|-------|
| `src/core/geo/providers.py` | Заменить 2 stub-класса на `_EstoniaGeoLookup` с dict из 19+ записей | §2.1 |
| `src/core/application/services.py` | Промоут geo miss лога; WARNING при gpt_signals drop; вернуть `StoryIntakeResult` | §2.2, §2.3 |
| `src/core/intake/contracts.py` | Добавить `IntakeNotes`, `StoryIntakeResult`; обновить `build_story_intake_response()` | §2.3 |
| `src/core/api/handlers.py` | Передать флаги из `StoryIntakeResult` в response builder | §2.3 |
| `docs/runtime-docs/api-reference/openapi.yaml` | Добавить `intake_notes` schema | §2.3 |
| `docs/runtime-docs/api-reference/API_REFERENCE.md` | Обновить §6.6, добавить `intake_notes` | §2.3 |
| `src/core/infrastructure/db_supabase.py` | Удалить title_hint (условно) | §2.4 |
| `src/core/infrastructure/db_sqlite.py` | Удалить title_hint (условно) | §2.4 |
| `supabase/migrations/...` | DROP COLUMN migration (условно) | §2.4 |

---

## 4. Acceptance Criteria

### Geo expansion (§2.1)
- [ ] `location_query = "Таллин"` → `geo_admin_settlement = "tallinn"`, `geo_admin_country = "EE"`
- [ ] `location_query = "Kalamaja"` → `geo_admin_district = "kalamaja"`, `geo_admin_settlement = "tallinn"`
- [ ] `location_query = "Tartu"` → `geo_admin_settlement = "tartu"`, `geo_admin_country = "EE"`
- [ ] `location_query = "Тарту"` → то же (RU-написание)
- [ ] `location_query = "Нарва"` → `geo_admin_settlement = "narva"`
- [ ] `location_query = ""` или отсутствует → `geo_*` = null, нет ошибок

### Logging (§2.2)
- [ ] История с непустым `location_query` но нераспознанным городом → в Railway logs появляется `intake.geo_not_resolved` на уровне INFO
- [ ] История без `location_query` → лог остаётся DEBUG `intake.geo_skip`
- [ ] `story_signal_store is None` при наличии gpt_signals → в Railway logs появляется WARNING `intake.gpt_signals_drop reason=signal_store_not_configured`

### intake_notes (§2.3)
- [ ] Ответ 202 содержит поле `data.intake_notes.geo_resolved: boolean`
- [ ] Ответ 202 содержит поле `data.intake_notes.gpt_signals_persisted: boolean`
- [ ] История без `location_query` → `geo_resolved: false`
- [ ] История с распознанным `location_query` → `geo_resolved: true`
- [ ] История без `gpt_signals` в запросе → `gpt_signals_persisted: true` (нечего сохранять = ok)
- [ ] История с `gpt_signals`, запись упала → `gpt_signals_persisted: false`
- [ ] openapi.yaml содержит `intake_notes` schema
- [ ] Тест-суит без регрессий

### Title hint cleanup (§2.4, условно)
- [ ] SQL-проверка вернула 0 строк с ненулевыми title_hint значениями
- [ ] Migration выполнена на Supabase
- [ ] `db_supabase.py` и `db_sqlite.py` не содержат упоминаний `title_hint`
- [ ] `required_columns_ready()` не проверяет `narrative_title_hint` (обновить список)

---

## 5. Не в scope этого REQ

- GPT-скрипты (location_query, origin_source) — scope REQ-47
- Railway deployment переменные — scope REQ-47
- Реальный geocoding API (OpenCage, Nominatim) — product backlog
- narrative_summary_json генерация (GPT-side) — scope REQ-47
- Изменение `status` lifecycle — не затрагивается
