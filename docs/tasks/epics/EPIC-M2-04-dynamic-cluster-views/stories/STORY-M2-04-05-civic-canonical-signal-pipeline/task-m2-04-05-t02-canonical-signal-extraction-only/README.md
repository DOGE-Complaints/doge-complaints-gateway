## Task workspace — `task-m2-04-05-t02-canonical-signal-extraction-only`

- Story: [`../STORY-M2-04-05-civic-canonical-signal-pipeline.md`](../STORY-M2-04-05-civic-canonical-signal-pipeline.md)
- Decision Ref: REQ-34 §2.3; gap-interview G-04.3–4

## Task: refactor — canonical-only signal extraction

### Цель
Удалить `infer_signals_from_narrative()` и режимы `keyword`/`hybrid`; оставить единый путь `infer_signals_from_canonical()`; включить `canonical_type` в возвращаемый signal dict.

### Факты из кода
1. [`src/core/profile/enrichment.py`](../../../../../../../src/core/profile/enrichment.py) L16–44 — `infer_signals_from_narrative` (EN keywords).
2. Там же L52 — `_ = canonical_type` (данные отбрасываются).
3. Там же L91–116 — `get_signals_for_story(story, signal_source)` с ветками `canonical` | `keyword` | `hybrid`.
4. [`src/core/application/services.py`](../../../../../../../src/core/application/services.py) — импорт и вызов `infer_signals_from_narrative` для profile enrichment.

### Gap / Проблема
Многоязычные stories не получают корректных civic signals при keyword/hybrid fallback (G-04).

### AC/DoD
- [x] (P0) `infer_signals_from_narrative` удалена; нет экспорта в `profile/__init__.py`.
- [x] (P0) `get_signals_for_story(story: StoryRecord) -> dict[str, str]` без параметра `signal_source`.
- [x] (P0) Signal dict включает ключ для `canonical_type` (например `SignalDimension` или согласованное имя — зафиксировать в коде и тесте).
- [x] (P0) `services.py` profile path использует canonical extraction, не narrative keywords.
- [x] (P1) `cluster_orchestrator` вызовы обновлены под новую сигнатуру (или в T06, если только orchestrator).

### Где менять код
- [`src/core/profile/enrichment.py`](../../../../../../../src/core/profile/enrichment.py)
- [`src/core/profile/__init__.py`](../../../../../../../src/core/profile/__init__.py)
- [`src/core/application/services.py`](../../../../../../../src/core/application/services.py)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_signal_extraction_canonical.py -q --tb=short
rg -n infer_signals_from_narrative src/ tests/ && test $? -eq 1
```
