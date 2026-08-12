## Task workspace — `task-gw-l10n-01-t05-api-reference-openapi-i18n-locales`

- Story: [`../STORY-GW-L10N-01-projection-content-i18n-preservation.md`](../STORY-GW-L10N-01-projection-content-i18n-preservation.md)
- Decision Ref: backlog T05; cross-ref GW-L10N-02

---
**Priority:** P1  
**Complexity:** S  
**Estimate:** ~30 min  
**Status:** ready  
**Wave:** `pkg-000027`  
**Skill declared:** python-pro  
---

## Task: docs — API_REFERENCE §7 / openapi i18n locales

### Цель
Обновить `API_REFERENCE §7` / `openapi.yaml`: пояснить, что локали могут различаться и какая считается оригиналом (cross-ref на GW-L10N-02).

### Факты из кода
1. [`API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) L466 — `## 7. Issues API`.
2. [`openapi.yaml`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) — issue title/summary/description i18n objects.
3. Backlog: `original_locale` — **GW-L10N-02** (out of scope implementation here; только cross-ref).

### AC/DoD
- [ ] (P0) API_REFERENCE §7 документирует: `title`/`summary`/`description` locales **may differ** (not identical copies).
- [ ] (P0) Cross-reference на GW-L10N-02 для `original_locale` (planned).
- [ ] (P1) openapi.yaml description на i18n issue fields обновлён согласованно.

### Где менять код
- [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md)
- [`docs/runtime-docs/api-reference/openapi.yaml`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml)

### Out of scope
- `src/**`, `tests/**`
- Реализация `original_locale`

### Команды проверки
```bash
grep -n "may differ\|различа" doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md
```
