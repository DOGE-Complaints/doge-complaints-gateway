# Issue Intake и SPA Projection: фактический аудит runtime

## Цель документа

Зафиксировать по коду:

1. какой входной payload реально обрабатывается для создания сущности на intake-слое;
2. есть ли в этом входе SPA-совместимый projection-объект;
3. если нет, где и как он строится в коде;
4. где есть разрыв между существующим runtime API и моделями `intake`/`projection`.

Источники: `src/core/**`, `tests/**`, `docs/runtime-docs/api-reference/openapi.yaml`.

## 1) Фактический HTTP runtime на текущий момент

В `src/core/api/asgi_app.py` реализованы только GET-роуты:

- `/health`
- `/ready`
- `/protected/status`
- `/metrics`
- `/demo/auth-page` (demo static)

`POST`-роутов в ASGI-приложении нет (в коде отсутствуют `@app.post(...)`).

Следствие:

- HTTP endpoint для `create issue` в runtime сейчас не существует;
- HTTP endpoint для story intake (`/intake/stories`) в runtime тоже не подключен, хотя его контракт описан в OpenAPI как planned.

## 2) Входная модель данных, которая реально реализована в коде

Реальный входной контракт определен в `src/core/intake/contracts.py`:

- `parse_story_intake_request(payload)` -> `StoryIntakeRequest`
- `INTAKE_SCHEMA_VERSION = "m2.story_intake_envelope.v1"`

### 2.1 Корневые поля `StoryIntakeRequest`

- `schema_version` (required, non-empty `str`, строго равно `m2.story_intake_envelope.v1`)
- `submitter` (required object)
- `narrative` (required object)
- `origin` (optional object)
- `privacy` (optional object)
- `live_story_context` (optional object)

### 2.2 Детализация полей и валидаций

#### `submitter`

- `external_user_id`: required, non-empty `str` (иначе `IntakeValidationError`)
- `identity_issuer`: optional `str`; пустая строка -> `None`; не-строка -> `None`

#### `narrative`

- `original_text`: required, non-empty `str` (иначе `IntakeValidationError`)
- `language`: optional `str`; пустая строка -> `None`; не-строка -> `None`
- `title_hint`: optional `str`; пустая строка -> `None`; не-строка -> `None`
- `location_query`: optional `str`; пустая строка -> `None`; не-строка -> `None`

#### `origin`

Если поле передано, оно обязано быть object.

- `source`: optional `str` -> trimmed or `None`
- `conversation_id`: optional `str` -> trimmed or `None`
- `tool_call_id`: optional `str` -> trimmed or `None`

#### `privacy`

Если поле передано, оно обязано быть object.

- `contains_pii`: optional, но если передано, строго `bool`; default `False`
- `redaction_requested`: optional, но если передано, строго `bool`; default `False`

Для non-bool значений бросается `IntakeValidationError`.

#### `live_story_context`

Если поле передано, оно обязано быть object.

- `consistency_notes`: optional `str` -> trimmed or `None`

### 2.3 Нормализация и поведение parser

- `str`-поля режутся через `strip()`;
- часть optional строковых полей при не-`str` значении не вызывает ошибку, а становится `None`;
- неизвестные дополнительные поля parser явно не отклоняет.

## 3) Что происходит после intake-парсинга (доменная запись)

Создание доменной сущности делает `StoryIntakeService.create_story(...)` в `src/core/application/services.py`.

Маппинг `StoryIntakeRequest` -> `StoryRecord`:

- генерируется `story_id` (`uuid4`)
- `schema_version` переносится из request
- `narrative.original_text` -> `narrative_original_text`
- `submitter.external_user_id` -> `submitter_external_user_id`
- `submitter.identity_issuer` -> `submitter_identity_issuer`
- `origin.*` -> `origin_source` / `origin_conversation_id` / `origin_tool_call_id`
- `privacy.*` -> `privacy_contains_pii` / `privacy_redaction_requested`
- `geo` вычисляется через `geo_service.resolve_for_story(location_query)` (если geo_service подключен)
- начальный статус: `accepted`, затем readiness transition в `partial_ready` или `ready_for_profile`

В `StoryRecord` (см. `src/core/domain/contracts.py`) нет SPA projection-полей вроде `title/summary/labels/type` в формате дашборда.

## 4) Аудит вопроса про SPA projection внутри входной модели

Короткий ответ: **нет**, во входной intake-модели SPA projection-объекта нет.

В `StoryIntakeRequest` отсутствуют:

- `status/type/labels` в SPA-гранулярности;
- i18n-пакеты `title/summary/description` формата `{et, ru, en}`;
- поля card-level вида `arweave_txid/image_txid/image_hash`.

То есть SPA-объект не приходит "как есть" во входном payload intake.

## 5) Где формируется SPA-совместимый объект

SPA projection строится отдельным projection-слоем:

- вход: `ProjectionInput` (`src/core/projection/input.py`)
- маппер: `project_distinct_issue(...)` (`src/core/projection/mapper.py`)
- сервис: `IssueProjectionService.project(...)` (`src/core/projection/service.py`)
- выход DTO: `SpaIssueProjection` + `to_public_dict()` (`src/core/projection/dto.py`)
- проверки контракта: `validate_governed_enums`, `validate_optional_tx_fields` (`src/core/projection/validation.py`)

### 5.1 Вход `ProjectionInput` (что нужно для SPA проекции)

- `issue_id: str`
- `status: str` (должен быть из `SpaIssueStatus`)
- `issue_type: str` (должен быть из `SpaIssueType`)
- `labels: tuple[str, ...]` (каждый label должен быть из `SpaLabel`)
- `title: I18nText`
- `summary: I18nText | None`
- `description: I18nText`
- optional: `institution`, `created_at`, `arweave_txid`, `image_txid`, `image_hash`

### 5.2 Как строится `SpaIssueProjection`

`project_distinct_issue` делает:

1. валидацию enum-значений (`status`, `issue_type`, `labels`);
2. валидацию txid полей (запрещены placeholder значения: `fake`, `placeholder`, `todo`, `0x0`, пустая строка);
3. fallback summary: если `summary` отсутствует или частично пустая по локали, берется соответствующая локаль из `title`;
4. сборку `SpaIssueProjection`.

`to_public_dict()` возвращает JSON shape для SPA:

- required keys: `id`, `status`, `type`, `labels`, `title`, `summary`, `description`
- optional keys добавляются только если не `None`.

## 6) Есть ли автоматическая связка intake -> projection в runtime API

По факту текущего кода:

- в API handlers (`src/core/api/handlers.py`) intake/projection обработчики не подключены;
- `parse_story_intake_request` и `build_story_intake_response` не вызываются из API слоя;
- `IssueProjectionService` только создается в `DefaultServiceFactory`, но не используется HTTP-роутами.

Итог:

- projection объект получается в коде отдельным процессом через `IssueProjectionService`,
- но end-to-end HTTP pipeline `POST intake/create -> построение SPA projection -> HTTP response` в текущем runtime не реализован.

## 7) Тестовые доказательства по контрактам

### Intake-контракт и story create

- `tests/test_story_intake_contract.py`
  - required поля;
  - версия схемы;
  - bool-валидация privacy;
  - формат envelope ответа intake response builder.
- `tests/test_story_repository_lifecycle.py`
  - маппинг intake -> `StoryRecord`;
  - lifecycle переходы.
- `tests/test_story_intake_idempotency.py`
  - поведение `idempotency_key`.
- `tests/test_geo_intelligence.py`
  - добавление `geo` при `location_query`.

### SPA projection

- `tests/test_spa_projection.py`
  - happy path проекции;
  - fallback summary по локалям;
  - rejection unknown labels;
  - rejection placeholder txid;
  - required keys публичного SPA payload.

### HTTP surface (подтверждение отсутствия POST intake/create в runtime)

- `tests/test_http_transport_smoke.py`
  - покрывает только `/health`, `/ready`, `/protected/status`, `/metrics`.

## 8) Практический вывод для API входа и SPA модели

1. Текущий "вход на создание" в коде существует как доменный intake parser/service (`StoryIntakeRequest` + `StoryIntakeService`), но не как активный HTTP endpoint.
2. SPA dashboard-compatible объект не является частью входного intake payload.
3. SPA объект получается отдельно в projection слое из `ProjectionInput`.
4. В текущем runtime есть функциональный разрыв между intake и projection на уровне HTTP orchestration.

## 9) Gap Register (SSOT)

| gap_id | Симптом (факт кода) | Код-источник | Impact | Target state | owner task key |
|---|---|---|---|---|---|
| GAP-IP-001 | Нет HTTP intake endpoint (`POST /intake/stories`) в runtime | `src/core/api/asgi_app.py`, `src/core/api/handlers.py` | Intake-контракт не доступен извне, демо не может показать реальный submit | Активный POST endpoint с envelope/error taxonomy | `TASK-INTAKE-HTTP-01` |
| GAP-IP-002 | Нет HTTP create issue endpoint | `src/core/api/asgi_app.py` | Ключевой use-case issue creation не экспонирован | Активный POST issue endpoint (orchestration) | `TASK-ISSUE-CREATE-HTTP-01` |
| GAP-IP-003 | Нет bridge `Story/Promotion -> ProjectionInput` | `src/core/application/services.py`, `src/core/promotion/service.py`, `src/core/projection/input.py` | Невозможно стабильно построить SPA card из текущего потока данных | Явный adapter/assembler слой до `IssueProjectionService` | `TASK-STORY-TO-PROJECTION-01` |
| GAP-IP-004 | Нет единой политики заполнения обязательных SPA полей (`status/type/labels/i18n`) из intake/story/promotion | `src/core/projection/mapper.py`, `src/core/projection/enums.py`, `src/core/intake/contracts.py` | Недетерминированный mapping и риск ad-hoc логики | Версионированная policy + правила derivation/fallback + валидации | `TASK-SPA-PROJECTION-DATA-01` |
| GAP-IP-005 | Нет e2e pipeline-контрактов от HTTP intake/create до SPA payload | `tests/test_http_transport_smoke.py`, `tests/test_spa_projection.py` | Нет доказательства сквозной совместимости API->SPA | E2E/contract suite для полного потока + регресс-гейты | `TASK-E2E-CONTRACT-01` |

## 10) Rule: gap ownership and closure

Каждый `gap_id` должен существовать в одном из состояний:

- `Planned` — есть `owner task key` в backlog;
- `In Progress` — owner task выполняется;
- `Closed` — owner task в `Done (Committed)` и есть run-report ссылка;
- `Deferred` — есть явное обоснование в матрице трассировки.
