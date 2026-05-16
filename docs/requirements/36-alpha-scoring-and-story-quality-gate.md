# REQ-36: Alpha Scoring and Story Quality Gate

**Статус:** Реализовано (STORY-M2-04-06, 2026-05-16)  
**Источник:** Gap-интервью 2026-05-13, G-03  
**Приоритет:** P1  
**Связанные SA:** cluster-engine/03, SA-04 (eID gate)  

---

## 1. Контекст

`CLUSTER_TIE_BREAKER` объявлен в `config/schema.py` и читается в `AppConfig`, но `cluster/engine.py` не использует его. Текущий выбор доминантной истории — примитивный (первая по алфавиту или наибольшая по размеру данных).

Доминантная история — это story, чьи поля (`canonical_type`, `title`, сигналы) используются при формировании Issue. Без правильного выбора SPA видит некачественные данные.

---

## 2. Требования

### 2.1 `identity_issuer` как eID gate на intake (не scoring)

- `submitter.identity_issuer` → обязательное поле (HTTP 400 без него)
- Все истории в системе имеют eID верификацию → поле не дифференцирует качество
- В `alpha_score()` **не участвует** — у всех историй оно заполнено

(Изменение контракта описано в REQ-33; здесь фиксируется что eID — gate, не scoring.)

### 2.2 Алгоритм `alpha_score()` — максимум 100 баллов

```python
def alpha_score(story: StoryRecord) -> float:
    score = 0.0

    # Измерение 1: Классификационная покрытость (0–30)
    # Насколько хорошо история "понята" GPT
    if story.narrative_canonical_type:
        score += 12   # тип определён
    label_count = len(story.narrative_canonical_labels)
    score += min(label_count * 6, 18)  # до 3 меток × 6 pts; cap 18

    # Измерение 2: Богатство нарратива (0–40)
    # Насколько детально описана проблема
    text_len = len(story.narrative_original_text.strip())
    score += min(text_len / 15, 20)    # cap: 300 символов → 20 pts
    if story.narrative_summary_json:
        score += 10   # GPT создал структурированное резюме
    if story.narrative_consistency_notes:
        score += 10   # GPT делал follow-up уточнения

    # Измерение 3: Гео-точность (0–30)
    # Применимо только для гео-релевантных историй
    if story.geo is not None:
        score += 10                          # базовый бонус за наличие гео
        score += story.geo.confidence * 20   # точность: 0.88 → +17.6 pts

    return score  # max: 100
```

**Гео-агностичные кластеры:** для цифровых сервисов, политических жалоб и т.д. `geo = None` → измерение 3 = 0 для всех историй кластера → соревнуются только по [1]+[2]. Это корректно.

### 2.3 Tiebreaker при равных баллах

```python
winner = min(story_a, story_b, key=lambda s: s.created_at)  # старейшая история
```

### 2.4 `CLUSTER_TIE_BREAKER` env var

- Единственное поддерживаемое значение: `alpha`
- `oldest_first` и `systemic_priority` — roadmap, не реализованы
- Дефолт: `alpha`

### 2.5 Canonical type readiness gate

В `promotion/gates.py` добавить gate: кластер должен содержать хотя бы одну историю с `canonical_type in {"complaint", "system_bug"}`, иначе promotion → skip.

**Логика:** кластер из одних `observation` — наблюдения без явной проблемы; нет смысла создавать Issue.

---

## 3. Размещение в коде

Варианты:
- Новый модуль `cluster/alpha.py` с `alpha_score(story: StoryRecord) -> float`
- Или встроить в `cluster/engine.py`

Рекомендация: отдельный `cluster/alpha.py` — testability + single responsibility.

---

## 4. Cascade — файлы для изменения

| Файл | Изменение |
|------|-----------|
| `cluster/alpha.py` | ✅ Новый — `alpha_score()` функция |
| `cluster/engine.py` | Использовать `alpha_score()` при выборе dominant story |
| `promotion/gates.py` | Добавить `canonical_type` gate |
| `intake/contracts.py` | `identity_issuer` обязательное (см. REQ-33) |
| `domain/contracts.py` | `Submitter.identity_issuer: str` (без None) |
| `config/schema.py` | `CLUSTER_TIE_BREAKER` только `alpha` как валидное значение |
| Тесты | `tests/test_alpha_score.py` — unit тесты формулы |

---

## 5. Acceptance Criteria

- [x] `alpha_score(story)` возвращает float 0–100
- [x] История с `canonical_type` + 3 labels + длинный текст + summary → score > 60
- [x] История без canonical fields → score < 20
- [x] `alpha_score` = 0 для geo-агностичной истории (geo=None) по измерению 3
- [x] Dominant story в кластере = история с наибольшим `alpha_score`
- [x] Кластер без `complaint`/`system_bug` в canonical_type → не промотируется
- [x] `CLUSTER_TIE_BREAKER=alpha` в конфиге → используется formула, не примитивный sort
