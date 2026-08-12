# Interview Report: Domain Story Contract
## task-domain-story-contract-interview-01

**Дата:** 2026-05-17  
**Метод:** Структурированное интервью (4 раунда, AskUserQuestion)  
**Оператор:** zeya.metsapuu@gmail.com  
**Цель:** Зафиксировать целевой story intake-контракт для story-first pipeline; заблокировать downstream задачи по extraction/cluster/projection на актуальных полях.

---

## 1. Контекст интервью

Перед интервью был проведён code audit текущего intake-контракта (`src/core/intake/contracts.py`), domain-модели (`src/core/domain/contracts.py`) и lifecycle-логики (`src/core/application/services.py`, `narrative_v2_complete()`).

**Факты из кода (baseline до интервью):**

| Поле | Обязательное | Персистируется в StoryRecord |
|------|-------------|-------------------------------|
| `schema_version` | ДА (exact `"m2.story_intake_envelope.v2"`) | ДА |
| `submitter.external_user_id` | ДА | ДА |
| `submitter.identity_issuer` | ДА | ДА |
| `narrative.original_text` | ДА | ДА |
| `narrative.language` | ДА (et/ru/en) | ДА (`narrative_language`) |
| `narrative.session_language` | ДА (et/ru/en) | ДА (`narrative_session_language`) |
| `narrative.title` | ДА (dict et+ru+en, все 3) | ДА (`narrative_title`) |
| `narrative.description` | ДА (dict et+ru+en, все 3) | ДА (`narrative_description`) |
| `narrative.summary` | нет | ДА (`narrative_summary`) |
| `narrative.location_query` | нет | через GeoService → `geo` |
| `narrative.canonical_type` | нет | ДА (`narrative_canonical_type`) |
| `narrative.canonical_labels` | нет | ДА (`narrative_canonical_labels`) |
| `origin.*` | нет | ДА (3 поля) |
| `privacy.*` | нет | ДА (2 поля) |
| `live_story_context.consistency_notes` | нет | ДА (`narrative_consistency_notes`) |

**`narrative_v2_complete()` condition:**
```python
bool(original_text.strip() and language.strip() and session_language.strip()
     and all(title[lang].strip() for lang in ["et","ru","en"])
     and all(description[lang].strip() for lang in ["et","ru","en"]))
```
Только полный набор → `READY_FOR_PROFILE`, иначе `PARTIAL_READY`.

**Единственный entry point:** `POST /intake/stories` (`POST /issues` в коде отсутствует).

---

## 2. Вопросы

| ID | Раунд | Вопрос | Зачем нужен |
|----|-------|--------|-------------|
| Q1 | 1 | Как GPT-агент подаёт историю в систему? Какой transport/формат используется при demo-запуске? | Определить нет ли промежуточного слоя (очереди, MCP-сервера) который меняет контракт |
| Q2 | 1 | Когда происходит кластеризация и создание issue — синхронно внутри intake или асинхронно после? | Понять scope ответа POST /intake/stories и trigger для StoryClusterOrchestrator |
| Q3 | 2 | Что такое `external_user_id` в demo и кто его формирует? | Определить тип идентификатора, обязательность, и как GPT его получает |
| Q4 | 2 | Кто заполняет multilingual поля title/description (et+ru+en — все 3 языка обязательны)? | narrative_v2_complete требует все 3 — без понимания кто генерирует остаётся PARTIAL_READY |
| Q5 | 2 | Какие canonical_type значения предполагаются в demo? Кто его проставляет? | canonical_type — gate для promotion; без него история не promotable |
| Q6 | 3 | Если GPT разговаривал с гражданином на русском, что идёт в narrative.language и в original_text? | Уточнить семантику language — язык оригинала или нормализованный язык |
| Q7 | 3 | Кто проставляет privacy.contains_pii? | redact_pii() применяется только при contains_pii=True; если всегда false — PII safety неэффективна |
| Q8 | 3 | Для чего используется live_story_context.consistency_notes? Нужно ли его персистировать и показывать в UI? | Поле персистируется (narrative_consistency_notes) — нужно понять, нужно ли поверхностно в UI |
| Q9 | 4 | До готовности OAuth2.0 авторизации — что служит как external_user_id + identity_issuer для demo? | Убедиться что demo не заблокирован на validation этого поля |
| Q10 | 4 | Канонические метки canonical_labels — из какого набора GPT выбирает? | Определить нужен ли серверный vocabulary/validation для labels |
| Q11 | 4 | Есть ли поля в intake-пайлоаде, которые GPT должен заполнять, но сейчас не описаны / неClear? | Open points сбор |

---

## 3. Ответы

| ID | Ответ (дословно/нормализованно) |
|----|----------------------------------|
| Q1 | **Прямой HTTP POST.** GPT формирует JSON payload и вызывает `POST /intake/stories` напрямую, без промежуточного слоя. |
| Q2 | **Асинхронно, StoryClusterOrchestrator.** `POST /intake/stories` возвращает `story_id`; orchestrator запускается отдельно. |
| Q3 | **OAuth2.0 в разработке.** GPT будет проходить авторизацию через отдельную систему и передавать OAuth2.0-токен. Пока не готово. |
| Q4 | **GPT генерирует все 3 языка.** GPT пишет `title` и `description` сразу на et/ru/en в одном запросе. |
| Q5 | **GPT определяет из широкого списка.** canonical_type не ограничен complaint/suggestion — GPT выбирает из расширенного vocabulary. |
| Q6 | **language=«ru», original_text на русском.** `language` отражает язык оригинального текста; `original_text` не переводится перед отправкой. |
| Q7 | **GPT детектирует и проставляет.** GPT анализирует разговор и выставляет `contains_pii=true` при обнаружении персональных данных. |
| Q8 | **GPT пишет сюда отклонения от стандартного сценария.** Метаданные GPT (напр., "гражданин уточнял адрес 3 раза"). Персистировать нужно; показывать в UI — явно не указано, но возможно для оператора. |
| Q9 | **Любой строкой — не важно для demo.** Validation identity не критичен на данном этапе. |
| Q10 | **GPT генерирует свободные метки (free-form).** Фиксированного vocabulary нет; backend не валидирует labels против списка. |
| Q11 | **Нет, всё понятно.** Open points не выявлены. |

---

## 4. Решения

| decision_id | Решение | Owner | Rationale | Effect |
|-------------|---------|-------|-----------|--------|
| D-01 | GPT вызывает `POST /intake/stories` напрямую как HTTP POST без промежуточного слоя | GPT-агент | Нет очереди/MCP в demo-архитектуре | Контракт stableNo changes to API layer needed |
| D-02 | Кластеризация — асинхронная через StoryClusterOrchestrator | Backend | POST /intake/stories не блокирует на cluster/issue creation | Trigger механизм для orchestrator должен быть определён (cron или post-intake callback) |
| D-03 | external_user_id = временно любая строка; identity_issuer = любая строка | Demo | OAuth2.0 не готов; нет смысла блокировать demo на auth | Нет validation на этапе demo; после готовности OAuth2.0 — добавить validation |
| D-04 | GPT генерирует title+description сразу на 3 языках (et/ru/en) | GPT-агент | narrative_v2_complete требует все 3 языка для READY_FOR_PROFILE | GPT-промпт должен включать требование генерировать все 3 языка |
| D-05 | canonical_type — из расширенного списка, определяется GPT | GPT-агент | Не ограничен complaint/suggestion | Нет серверной валидации canonical_type против enum; backend принимает любую строку |
| D-06 | language = язык оригинального разговора; original_text = оригинал без перевода | GPT-агент | language отражает реальный язык нарратива; translate не нужен | Поля `narrative_language` корректно отражают реальный язык |
| D-07 | contains_pii = GPT-детект; GPT выставляет true при обнаружении PII | GPT-агент | REQ-37 redact_pii() применяется только при contains_pii=True | GPT-промпт должен включать инструкцию по PII детекции |
| D-08 | consistency_notes = GPT-метаданные об отклонениях от стандартного сценария; персистируются | GPT-агент | narrative_consistency_notes уже персистируется в StoryRecord | Показывать ли в UI — решается в frontend-задачах (не определено сейчас) |
| D-09 | canonical_labels = free-form строки, генерируются GPT | GPT-агент | Нет фиксированного vocabulary в demo | Backend не валидирует labels против списка (current code принимает любые строки) |

---

## 5. Open Points

На момент окончания интервью открытых точек не выявлено.

**Pending (не blocking для demo):**
- OAuth2.0 integration: когда будет готово — `external_user_id` станет OAuth2.0 subject; нужен отдельный REQ
- `origin.source` / `origin.conversation_id` — значения для GPT flow не уточнены (GPT может не передавать; не критично)
- UI отображение `consistency_notes` — решается в frontend-задачах

---

## 6. Mapping to Model/Rules

| Ответ | Поле / правило | Где в коде |
|-------|----------------|------------|
| GPT → прямой HTTP POST | `POST /intake/stories` | `api/asgi_app.py:281`, `api/handlers.py` |
| Async orchestrator | `StoryClusterOrchestrator.process_story()` | `application/cluster_orchestrator.py:72` |
| external_user_id = any string | `Submitter.external_user_id` required str | `intake/contracts.py:128–130` |
| identity_issuer = any string | `Submitter.identity_issuer` required str | `intake/contracts.py:131–133` |
| GPT генерирует et/ru/en для title+description | `narrative_v2_complete()` validates all 3 langs | `domain/narrative_i18n.py:91–105` |
| canonical_type = GPT-wide list | `narrative_canonical_type: str | None` | `domain/contracts.py:59`, `intake/contracts.py:176–181` |
| language = язык оригинала | `Narrative.language` required, `_parse_language_code()` | `intake/contracts.py:141–145` |
| contains_pii = GPT-детект | `Privacy.contains_pii` → `redact_pii()` | `core/redaction.py:6–10`, `application/services.py:82–83` |
| consistency_notes = GPT-метаданные | `narrative_consistency_notes` в StoryRecord | `domain/contracts.py:58`, `application/services.py:138–142` |
| canonical_labels = free-form | `narrative_canonical_labels: tuple[str, ...]` | `domain/contracts.py:60`, `intake/contracts.py:182–196` |

---

## 7. GPT Interview Data Reconciliation

### Что GPT собирает при разговоре с гражданином

| Данные из разговора | Intake поле | Кто заполняет | Примечание |
|---------------------|-------------|---------------|------------|
| Текст жалобы (оригинал) | `narrative.original_text` | GPT | Без перевода |
| Язык разговора | `narrative.language` + `narrative.session_language` | GPT | Оба = язык оригинала |
| Заголовок (et/ru/en) | `narrative.title` | GPT | GPT генерирует все 3 |
| Описание (et/ru/en) | `narrative.description` | GPT | GPT генерирует все 3 |
| Тип обращения | `narrative.canonical_type` | GPT | Из широкого списка |
| Тематические метки | `narrative.canonical_labels` | GPT | Free-form strings |
| Место | `narrative.location_query` | GPT (если упомянуто) | GeoService resolves |
| PII-флаг | `privacy.contains_pii` | GPT | GPT детектирует в тексте |
| Отклонения сценария | `live_story_context.consistency_notes` | GPT | Метаданные диалога |
| Идентификатор гражданина | `submitter.external_user_id` | OAuth2.0 токен (pending) | Пока — any string |
| Источник | `submitter.identity_issuer` | OAuth2.0 issuer (pending) | Пока — any string |

### Поля, которые GPT НЕ заполняет напрямую

- `narrative.summary` — поле в контракте опциональное; GPT не обязан заполнять (не упомянуто в интервью)
- `origin.*` — необязательные; GPT может не передавать
- `privacy.redaction_requested` — не упомянуто; default false

### Критический path к READY_FOR_PROFILE

Для того чтобы story после intake сразу попала в `READY_FOR_PROFILE` (а не `PARTIAL_READY`), GPT **обязан** заполнять:
1. `narrative.original_text` — непустой
2. `narrative.language` — et/ru/en
3. `narrative.session_language` — et/ru/en
4. `narrative.title` — все 3 ключа et/ru/en, каждый непустой
5. `narrative.description` — все 3 ключа et/ru/en, каждый непустой

GPT подтверждён как генератор всех этих полей (D-04).

---

## 8. Impact on Next Tasks

### TASK-INTAKE-STORY-CONTRACT-EXPANSION-02

На основании интервью — **изменений в backend-контракте не требуется** для demo. Текущий контракт (`m2.story_intake_envelope.v2`) покрывает все сценарии.

**Что нужно сделать в следующих задачах:**

| Пункт | Приоритет | Scope |
|-------|-----------|-------|
| Документировать trigger-механизм для StoryClusterOrchestrator (D-02) — cron или post-intake hook | P1 | Backend / ops |
| GPT-промпт engineering: требование генерировать title+description на et/ru/en (D-04) | P1 | GPT agent |
| GPT-промпт engineering: инструкция по PII-детекции для contains_pii (D-07) | P1 | GPT agent |
| GPT-промпт engineering: canonical_type vocabulary list | P2 | GPT agent |
| OAuth2.0 integration: заменить any-string auth на реальный токен (D-03) | P2 | Auth / backend |
| UI: решить отображение consistency_notes для оператора (D-08) | P3 | Frontend |
| Определить значения origin.source / origin.conversation_id для Telegram flow | P3 | GPT agent / backend |

### Влияние на upstream задачи (REQ-34..REQ-37)

- **REQ-34 (canonical signals):** canonical_labels = free-form (D-09) → ClusteringEngine использует `signals` dict, а не labels напрямую; изменений не требует
- **REQ-35 (geo scope):** location_query заполняется GPT → geo resolution активна; geo scope enforcement применяется корректно
- **REQ-36 (alpha score):** alpha_score учитывает canonical_type, labels, text_len, summary, consistency_notes, geo — GPT-flow должен обеспечить canonical_type + labels для хорошего score
- **REQ-37 (PII safety):** GPT детектирует PII (D-07) → redact_pii() получает корректный contains_pii флаг; pipeline safety обеспечена
