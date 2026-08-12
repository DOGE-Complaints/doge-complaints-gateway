## Task workspace — `task-m2-18-05-t21-ac41-8-testing-architecture-doc`

- Story: [`../STORY-M2-18-05-live-integration-ci-req41.md`](../STORY-M2-18-05-live-integration-ci-req41.md)
- Decision Ref: [`../../../../../../requirements/41-testing-production-coverage-target-state.md`](../../../../../../requirements/41-testing-production-coverage-target-state.md) §5 AC-41-8; PS-01..PS-25 matrix

---
**Приоритет:** P2  
**Сложность:** S  
**Оценка времени:** ~1–2 ч  
**Статус:** Done  
**Wave:** `pkg-000021`  
---

## Task: docs — testing architecture PS matrix + REQ-41 index

### Цель
Update [`13-testing-and-quality-architecture.md`](../../../../../../solution%20architecture/13-testing-and-quality-architecture.md) §6 with PS-01..PS-25 coverage matrix; add REQ-41 README-index entry.

### Почему это важно (риск)
AC-41-8 requires traceable closure of all 25 production scenarios in architecture doc.

### Факты из кода
1. REQ-39 wave closed PS-02, 05–10, 12, 15–17, 20–24 in contract tests.
2. REQ-41 gaps close PS-01, 03–04, 11, 13–14, 18–19 + layers 6–7.
3. [`requirements/README.md`](../../../../../../requirements/README.md) or gateway docs index — add REQ-41 execution pointer.

### Gap / Проблема
**AC-41-8:** architecture doc lacks full PS matrix with test file mapping.

### AC/DoD
- [x] (P0) §6 table: each PS-* → layer, test file(s), status (covered/partial/TBD).
- [x] (P0) Cross-link REQ-41, EPIC-M2-18 stories 03–05, `pkg-000021`.
- [x] (P1) Note `LOCAL_SERVER_URL` operator workflow for Layer 6.
- [x] (P1) Requirements index lists REQ-41 with link to epic wave.

### Где менять код
- [`docs/solution architecture/13-testing-and-quality-architecture.md`](../../../../../../solution%20architecture/13-testing-and-quality-architecture.md)
- [`docs/requirements/README.md`](../../../../../../requirements/README.md) (if index exists)

### Out of scope
- Implementing tests (other tasks); `pkg-000020` edits.

### Команды проверки
```bash
# Manual: review §6 matrix against REQ-41 §2 PS list
grep -n 'PS-' "doge-complaints-gateway/docs/solution architecture/13-testing-and-quality-architecture.md"
```
