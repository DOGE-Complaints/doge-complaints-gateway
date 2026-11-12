# 31. Права гражданина: удаление истории и обращение с персональными данными

> **Назначение документа.** Спецификация требований к двум отсутствующим возможностям, блокирующим честный гражданский запуск: (1) право гражданина удалить свою историю, (2) базовая обработка персональных данных. Документ написан по методологии analysis.mdc — каждое утверждение верифицировано по фактическому состоянию кода.
>
> **Связь с другими документами:**
> - req22 §D-10: "privacy.contains_pii по умолчанию false в demo; детекция PII — позже" — настоящий документ закрывает это "позже"
> - MVP-аудит (`docs/mvp-readiness-tallinn-audit.md`) P0-T3, P0-T4 — этот документ их специфицирует

---

## 1. Текущее состояние кода (аудит 2026-05-07)

### 1.1 Что хранится о гражданине

`StoryRecord` (`src/core/domain/contracts.py:43-58`):

```python
@dataclass(frozen=True)
class StoryRecord:
    story_id: str
    narrative_original_text: str           # свободный текст жалобы — может содержать имя, адрес
    submitter_external_user_id: str        # wallet address или GPT user_id — связывает текст с идентификатором
    lifecycle_status: StoryLifecycleStatus
    privacy_contains_pii: bool = False     # флаг: по умолчанию False
    privacy_redaction_requested: bool = False
    ...
```

`narrative_original_text` хранится **бессрочно** в Supabase и SQLite без автоматической проверки на PII.

### 1.2 Что отсутствует в `StoryRepository`

Методы, объявленные в `src/core/domain/contracts.py:62-78`:

```python
def save_story(self, record: StoryRecord) -> StoryRecord: ...
def get_story(self, story_id: str) -> StoryRecord | None: ...
def list_stories(self) -> list[StoryRecord]: ...
def list_stories_ready_for_clustering(self) -> list[StoryRecord]: ...
def update_lifecycle_status(self, story_id: str, status: StoryLifecycleStatus) -> None: ...
```

Метода `delete_story` нет ни в интерфейсе, ни в реализациях (`db_sqlite.py`, `db_supabase.py`, `in_memory`).

### 1.3 Что отсутствует в API

Зарегистрированные маршруты (`src/core/api/asgi_app.py`):
- `GET /health`
- `GET /ready`
- `GET /protected/status`
- `GET /metrics`
- `GET /demo/auth-page`
- `POST /intake/stories`

Маршрутов для удаления или проверки статуса нет.

### 1.4 Существующая PII-инфраструктура

`src/core/evidence/redaction.py` — реализована функция `redact_evidence_pack()`, которая скрывает story_ids из публичного ответа, если `privacy_classification in {"restricted", "pii", "pii_high", "internal_only"}`. Но это работает с `EvidencePackRecord`, не с `StoryRecord`, и срабатывает только если GPT явно выставил privacy флаг.

Никакой автоматической детекции PII в `narrative_original_text` нет.

### 1.5 Текущий lifecycle — необратимый

```
ACCEPTED → READY_FOR_PROFILE → CLUSTERED
```

`update_lifecycle_status` только движется вперёд. Нет `DELETED` статуса, нет rollback. Как только story в `CLUSTERED` — она выбыла из clustering но текст остался в БД.

---

## 2. Требования

### 2.1 Право на удаление истории (P0)

**Мотивация:** гражданин подаёт свободный текст, который может содержать имя, адрес, личные обстоятельства. Без права удалить — система не имеет права хранить эти данные в контексте публичного civic инструмента.

#### 2.1.1 Новый lifecycle статус

Добавить в `StoryLifecycleStatus` (`src/core/domain/contracts.py:21`):

```python
class StoryLifecycleStatus(str, Enum):
    ACCEPTED = "accepted"
    READY_FOR_PROFILE = "ready_for_profile"
    CLUSTERED = "clustered"
    WITHDRAWN = "withdrawn"          # ← новый: история отозвана гражданином
```

`WITHDRAWN` — терминальный статус. Story исключается из `list_stories_ready_for_clustering()`.

#### 2.1.2 Метод удаления в `StoryRepository`

Добавить в интерфейс `src/core/domain/contracts.py:62-78`:

```python
def delete_story(self, story_id: str, submitter_id: str) -> bool:
    """
    Удалить narrative_original_text; перевести статус в WITHDRAWN.
    Возвращает True если история найдена и принадлежит submitter_id,
    False если не найдена, raises ValueError если submitter_id не совпадает.
    """
```

**Семантика:** `narrative_original_text` заменяется на `"[withdrawn]"`. `submitter_external_user_id` зануляется или заменяется на хеш. Остальные поля (story_id, canonical_labels, lifecycle_status=WITHDRAWN) — сохраняются для целостности кластерных ссылок.

**Почему не full DELETE из БД:** issue_story_links может содержать ссылку на этот story_id. Удаление строки сломает FK. `WITHDRAWN` + redacted text — корректный компромисс между GDPR-совместимостью и целостностью данных.

#### 2.1.3 Новый API endpoint

```
DELETE /intake/stories/{story_id}
Authorization: Bearer {user_token}   # то же GPT/user-issued token что и при POST
```

**Запрос:**
```
DELETE /intake/stories/story-abc123
Authorization: Bearer {submitter_token}
```

**Ответ 200:**
```json
{"story_id": "story-abc123", "status": "withdrawn"}
```

**Ответ 404:** история не найдена.  
**Ответ 403:** submitter_id не совпадает.  
**Ответ 409:** история уже в статусе CLUSTERED — требуется подтверждение (см. §2.1.4).

#### 2.1.4 Удаление уже кластеризованной истории

Если story в `CLUSTERED` — она уже могла стать частью DOGEIssue. Возможны два подхода:

| Подход | Описание | Рекомендация |
|--------|----------|-------------|
| Запрет | 409 Conflict: история стала публичной проблемой, отзыв невозможен | Нарушает право на забвение |
| Мягкое удаление | Текст redacted, но story_id остаётся в issue_story_links | **Рекомендуется для MVP** |
| Каскадное удаление | Удаление story → пересчёт issue, удаление если cluster<min_size | Сложно, пост-MVP |

**MVP решение:** мягкое удаление — `narrative_original_text = "[withdrawn]"`, статус = `WITHDRAWN`. Issue остаётся публичным, но конкретный текст недоступен.

### 2.2 Базовое уведомление о сборе данных (P0)

**Мотивация:** принцип информированного согласия. Гражданин должен знать, что именно хранится, до отправки.

#### 2.2.1 Что добавить в intake response

`StoryIntakeResponse` (`src/core/intake/contracts.py`) сейчас возвращает `story_id` и `status`. Добавить поле `data_notice`:

```python
@dataclass(frozen=True)
class StoryIntakeResponse:
    story_id: str
    status: str
    data_notice: str  # ← новое: человекочитаемое уведомление
```

Значение:

```
"Your complaint text, civic labels assigned by AI, and a pseudonymous identifier 
are stored and may contribute to a public civic issue. 
You may withdraw your submission at DELETE /intake/stories/{story_id}."
```

Это не замена полноценному privacy notice, но **минимально достаточный disclosure** для demo-запуска.

#### 2.2.2 Опционально: поле consent в intake request

Для будущего (пост-MVP) добавить в `StoryIntakeRequest`:

```python
privacy_consent_given: bool = False  # если False — вернуть 422 с объяснением
```

В MVP: не блокирует приём, только disclosure в ответе.

### 2.3 PII detection: минимальный tier (P1)

**Мотивация:** `privacy_contains_pii = False` по умолчанию означает, что система не пытается обнаружить PII. Для публичного инструмента это создаёт риск: текст "Меня зовут Иван, я живу по адресу..." хранится и передаётся как обычный.

#### 2.3.1 Tier 1 — Heuristic PII flag (MVP-viable)

Добавить в `StoryRecord` processing (при `save_story`) простую эвристику:

```python
_PII_PATTERNS = [
    r"\b\d{5,6}\b",            # почтовые индексы / ID
    r"\b\+?\d[\d\s\-]{8,}\d\b",  # телефоны
    r"\b[\w.+-]+@[\w-]+\.[a-z]{2,}\b",  # email
]

def detect_pii_heuristic(text: str) -> bool:
    return any(re.search(p, text) for p in _PII_PATTERNS)
```

Если `detect_pii_heuristic(narrative_original_text)` → True: `privacy_contains_pii = True`. Эффект: story попадает в `restricted` visibility tier в `redaction.py`.

#### 2.3.2 Tier 2 — GPT-driven PII flag (пост-MVP)

GPT (preprocessing layer) выставляет `contains_pii=true` в canonical_labels при обнаружении имён, адресов, личных данных. Сейчас это не стандартизировано в словаре (`vocabulary.py`). Требует отдельного решения в GPT preprocessing контракте.

---

## 3. Acceptance Criteria

**AC-31-1 — Удаление:**
Вызов `DELETE /intake/stories/{story_id}` с валидным submitter_id:
- возвращает `{"status": "withdrawn"}`
- в БД `narrative_original_text = "[withdrawn]"`
- `lifecycle_status = WITHDRAWN`
- story не появляется в `list_stories_ready_for_clustering()`

**AC-31-2 — Ownership check:**
Вызов `DELETE` с неверным submitter_id возвращает 403.

**AC-31-3 — Soft delete для clustered:**
Вызов `DELETE` на story в CLUSTERED статусе:
- возвращает 200 с `{"status": "withdrawn", "note": "story was part of a public issue"}`
- текст redacted, story_id остаётся в issue_story_links

**AC-31-4 — Data notice:**
`POST /intake/stories` response содержит поле `data_notice` с непустой строкой.

**AC-31-5 — PII heuristic:**
Story с текстом, содержащим email или телефон, сохраняется с `privacy_contains_pii = True`.

---

## 4. Файлы, требующие изменений

| Файл | Изменение |
|------|-----------|
| `src/core/domain/contracts.py` | Добавить `WITHDRAWN` в `StoryLifecycleStatus`; добавить `delete_story` в `StoryRepository` |
| `src/core/infrastructure/db_sqlite.py` | Реализовать `delete_story` (soft delete) |
| `src/core/infrastructure/db_supabase.py` | Реализовать `delete_story` (soft delete) |
| `src/core/infrastructure/in_memory.py` | Реализовать `delete_story` |
| `src/core/intake/contracts.py` | Добавить `data_notice` в `StoryIntakeResponse` |
| `src/core/api/handlers.py` | Добавить handler для `DELETE /intake/stories/{story_id}` |
| `src/core/api/asgi_app.py` | Зарегистрировать `DELETE /intake/stories/{story_id}` |
| `src/core/profile/enrichment.py` | Добавить `detect_pii_heuristic` (или отдельный `src/core/intake/pii.py`) |

---

## 5. Что остаётся за рамками этого документа

- Полный GDPR compliance (Data Processing Agreement, DPA) — это legal, не engineering
- GPT-side PII detection в canonical_labels — требует изменения GPT preprocessing контракта
- Уведомление в UI о том, что история была использована в публичном issue — req21 (post-demo notifications)
- Каскадное удаление issue при удалении всех stories кластера — post-MVP

*Методология: analysis.mdc — все утверждения верифицированы по файлам кода.*
