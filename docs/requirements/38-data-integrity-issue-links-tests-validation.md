# REQ-38: Data Integrity — Issue Story Links, Tests, Validation

**Статус:** Реализовано (STORY-M2-17-02, 2026-05-17)  
**Источник:** Gap-интервью 2026-05-13, G-10, G-11, G-12  
**Приоритет:** P2 (G-10, G-11), P3 (G-12)  
**Связанные SA:** SA-10, SA-05  

---

## 1. G-10: Тесты living issues extend flow

### Контекст

`extend_candidate()` и `extend_issue()` реализованы в `promotion/service.py` и `application/issue_create.py`. Функция `find_promoted_by_cluster_id()` есть во всех трёх backends (in_memory, sqlite, supabase). Но e2e теста для полного flow **не существует** — `tests/test_living_issues_extend_existing.py` не найден.

### Требование

Написать e2e тест `tests/test_living_issues_extend_existing.py` для flow:

1. Создать кластер с 2 stories → promote → Issue создан (`story_count=2`)
2. Добавить третью story в тот же кластер
3. Запустить `process_story()` для новой story
4. Проверить: `extend_candidate()` вызван → Issue обновлён (`story_count=3`, `labels` обновлены)

Тест должен запускаться на всех трёх backends:
- `in_memory` (fast, unit-level)
- `sqlite` (integration)
- `supabase` (mock/stub)

---

## 2. G-11: `issue_story_links` N:M таблица

### Контекст

`ClusterMembershipStore` Protocol допускает N кластеров на story. В `domain/contracts.py` архитектурно предусмотрена множественная принадлежность. Однако таблица `issue_story_links` в Supabase bootstrap SQL **не найдена** — связь story ↔ issue не персистируется в Supabase backend.

### Требование

#### Миграция

```sql
CREATE TABLE IF NOT EXISTS issue_story_links (
    issue_id TEXT NOT NULL REFERENCES issues(id) ON DELETE CASCADE,
    story_id TEXT NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    cluster_id TEXT NOT NULL,
    linked_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (issue_id, story_id)
);

CREATE INDEX idx_issue_story_links_story ON issue_story_links(story_id);
CREATE INDEX idx_issue_story_links_issue ON issue_story_links(issue_id);
```

#### Обновление persistence / lookup (Variant A, 2026-05-17)

N:M связь story↔issue пишется через `IssueStoryLinkStore.save_issue_story_links()` (вызывается из `IssueCreateService`). `ClusterMembershipStore.save_membership()` остаётся на `cluster_memberships`.

`find_promoted_by_cluster_id()` должен учитывать `issue_story_links` при поиске promoted issue по `cluster_id`.

---

## 3. G-12: Arweave txid валидация

### Контекст

`projection/validation.py` принимает любую строку как txid без проверки формата. Arweave txid — всегда 43 символа base64url (`[A-Za-z0-9_-]{43}`).

### Требование

```python
# projection/validation.py
import re

ARWEAVE_TXID_RE = re.compile(r'^[A-Za-z0-9_-]{43}$')

def validate_arweave_txid(txid: str) -> bool:
    """Validate Arweave transaction ID format (43 chars base64url)."""
    return bool(ARWEAVE_TXID_RE.match(txid))
```

Применять при приёме `txid` в evidence/projection слоях. При невалидном txid → `ValidationError`.

---

## 4. Cascade — файлы для изменения

| Файл | Изменение |
|------|-----------|
| `tests/test_living_issues_extend_existing.py` | ✅ Новый файл — e2e тесты extend flow |
| Supabase bootstrap SQL | Добавить `issue_story_links` миграцию |
| `infrastructure/db_supabase.py` | Реализовать `save_membership()` через `issue_story_links` |
| `projection/validation.py` | Добавить `validate_arweave_txid()` |

---

## 5. Acceptance Criteria

**G-10:**
- [x] `tests/test_living_issues_extend_existing.py` существует и проходит на in_memory backend
- [x] Тест проверяет что после добавления 3-й story `Issue.story_count = 3`
- [x] Тест проверяет что `labels` пересчитаны (union canonical_labels)

**G-11:**
- [x] Таблица `issue_story_links` присутствует в bootstrap SQL
- [x] N:M persistence через `save_issue_story_links()` (Variant A; не `save_membership()`)
- [x] `find_promoted_by_cluster_id()` корректно работает через таблицу

**G-12:**
- [x] `validate_arweave_txid("valid43chars_base64url_string_here_xxxx")` → `True`
- [x] `validate_arweave_txid("short")` → `False`
- [x] `validate_arweave_txid("invalid!chars!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")` → `False`
