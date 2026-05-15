# REQ-34: Civic Clustering Engine — Canonical Signal Pipeline

**Статус:** Требует реализации  
**Источник:** Gap-интервью 2026-05-13, G-04, G-09  
**Приоритет:** P1  
**Связанные SA:** SA-06, cluster-engine/02, cluster-engine/03  

---

## 1. Контекст

### Проблема: legacy lenses и keyword-matching

Текущий `CLUSTER_ACTIVE_LENSES` содержит только legacy линзы:
```
topic_micro, need_local, failure_systemic, failure_micro, repeatability_local, relevance_systemic
```

Эти линзы используют `infer_signals_from_narrative()` — keyword-matching по английским словам (`"road" in text`). Для эстонских и русских историй точность = 0%.

Civic линзы (`civic_domain_micro`, `failure_pattern_micro` и др.) реализованы в коде, но не активированы. Они используют `canonical_labels` из GPT — language-agnostic и единственный корректный подход для многоязычной системы.

### Проблема: canonical_type игнорируется

`profile/enrichment.py:infer_signals_from_canonical()`:
```python
_ = canonical_type   # ← данные выбрасываются
```
GPT присылает `canonical_type` (`complaint`/`observation`/`system_bug`/`absurdity`), но gateway его не использует.

### Проблема: issue_type и labels из keyword-parsing

`application/issue_create.py` определяет `issue_type` и `labels` через keyword-matching по тексту — та же проблема.

---

## 2. Требования

### 2.1 Legacy линзы — полное удаление

Удалить из кодовой базы 6 legacy линз:
- `TOPIC_MICRO`, `NEED_LOCAL`, `FAILURE_SYSTEMIC`, `FAILURE_MICRO`, `REPEATABILITY_LOCAL`, `RELEVANCE_SYSTEMIC`

**Причина:** несовместимы с многоязычностью — keyword-matching работает только на EN.

### 2.2 Civic линзы — единственный активный набор

```
CLUSTER_ACTIVE_LENSES=civic_domain_micro,failure_pattern_micro,civic_weight_systemic,desired_outcome_local,affected_group_local,geographic_district_micro
```

Обновить в `.env` и `example.env`.

### 2.3 Signal extraction — canonical only

- `infer_signals_from_narrative()` — **удалить**
- `get_signals_for_story()` — убрать параметр `signal_source`, оставить только canonical режим
- `CLUSTER_SIGNAL_SOURCE` env var — не поддерживать `keyword`/`hybrid` (только `canonical`)
- **Исправить BUG**: `_ = canonical_type` → использовать `canonical_type` как дополнительный сигнал

### 2.4 `canonical_type` как сигнал

`canonical_type` используется в двух местах:

**В `alpha_score()`** (G-03, REQ-36): наличие `canonical_type` даёт +12 pts к score доминантной истории.

**Как readiness gate** (`promotion/gates.py`): кластер без хотя бы одной истории с `canonical_type in {"complaint", "system_bug"}` → не промотируется в Issue. Предотвращает продвижение плохо классифицированных историй.

### 2.5 `issue_type` и `labels` — из canonical полей

**`issue_type`** = `canonical_type` доминантной истории (по `alpha_score`):
```python
issue_type = dominant_story.narrative_canonical_type or "observation"
```

**`labels`** = union `canonical_labels` всех историй кластера, без дублей:
```python
labels = list(dict.fromkeys(
    label
    for story in cluster_stories
    for label in story.narrative_canonical_labels
))
```

Нет ограничения top-N — все уникальные метки.

**Удалить** `_derive_issue_type()` и `_derive_labels()` из `issue_create.py`.

---

## 3. Cascade — файлы для изменения

| Файл | Изменение |
|------|-----------|
| `cluster/types.py` | Удалить 6 legacy значений из `ClusterLens` enum |
| `cluster/engine.py` | Удалить `LEGACY_LENSES` константу; `lens_dimension()` только civic |
| `profile/enrichment.py` | Удалить `infer_signals_from_narrative()`, исправить `canonical_type` bug, убрать `signal_source` параметр |
| `application/issue_create.py` | Заменить `_derive_issue_type()` и `_derive_labels()` на canonical-based логику |
| `application/cluster_orchestrator.py` | Передавать dominant story и cluster stories в `issue_create` |
| `promotion/gates.py` | Добавить `canonical_type` readiness gate |
| `cluster/vocabulary.py` | Без изменений — словари корректны |
| `.env` | Обновить `CLUSTER_ACTIVE_LENSES` |
| `example.env` | То же |
| `config/schema.py` | `CLUSTER_TIE_BREAKER` допустимые значения: только `alpha` |
| Тесты кластеризации | Обновить фикстуры под civic-only lenses |

---

## 4. Acceptance Criteria

- [ ] `ClusterLens` enum не содержит legacy значений
- [ ] `infer_signals_from_narrative()` отсутствует в codebase
- [ ] `get_signals_for_story(story)` работает без `signal_source` параметра
- [ ] `canonical_type` присутствует в signal dict (не `_`)
- [ ] Кластер из историй с `canonical_type="observation"` → не промотируется (gate reject)
- [ ] `Issue.type` = `canonical_type` dominant story
- [ ] `Issue.labels` = union canonical_labels всех историй кластера
- [ ] `CLUSTER_ACTIVE_LENSES` в `.env` содержит только civic линзы
- [ ] Тесты проходят на ET/RU историях с заполненными `canonical_labels`
