## Task workspace — `task-m2-17-02-t04-arweave-txid-validation`

- Story: [`../STORY-M2-17-02-data-integrity-issue-links-tests-validation-req38.md`](../STORY-M2-17-02-data-integrity-issue-links-tests-validation-req38.md)
- Decision Ref: [`../../../../../../requirements/38-data-integrity-issue-links-tests-validation.md`](../../../../../../requirements/38-data-integrity-issue-links-tests-validation.md) §3; G-12; audit GAP-38-04

---
**Приоритет:** P3  
**Сложность:** S  
**Оценка времени:** ~30–60 min  
**Статус:** ready  
**Wave:** `pkg-000017`  
---

## Task: implement — `validate_arweave_txid()` in projection validation

### Цель
Добавить regex-валидацию Arweave txid (43 chars base64url) и применять при приёме txid в evidence/projection; невалидный → `ValidationError`.

### Факты из кода
1. [`projection/validation.py`](../../../../../../../src/core/projection/validation.py) — `validate_governed_enums()`, `validate_optional_tx_fields()` only; **нет** `validate_arweave_txid` / `ARWEAVE_TXID_RE` (audit).
2. REQ-38 §3 — `^[A-Za-z0-9_-]{43}$`.
3. M2-06-04 — placeholder tx rejection exists separately; G-12 adds format gate.

### Gap / Проблема
**GAP-38-04:** все 3 AC G-12 открыты.

### AC/DoD
- [ ] (P0) `ARWEAVE_TXID_RE` + `validate_arweave_txid(txid: str) -> bool` per REQ-38.
- [ ] (P0) Wire into txid acceptance path (`validate_optional_tx_fields` or call sites in evidence/projection).
- [ ] (P0) Invalid txid raises `ValidationError` (or documented equivalent).
- [ ] (P1) Unit tests: valid 43-char → True; `"short"` / invalid chars → False.

### Где менять код
- [`src/core/projection/validation.py`](../../../../../../../src/core/projection/validation.py)
- Evidence/projection call sites as needed (grep `arweave` / `txid`)

### Out of scope
- Living issues tests (T01)
- Supabase linkage (T03)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -c "from core.projection.validation import validate_arweave_txid; assert validate_arweave_txid('a'*43)"
cd doge-complaints-gateway && python3 -m pytest -q -k arweave 2>/dev/null || true
```
