## Task workspace — `task-m2-02-06-t03-gap-04-origin-gpt-orchestrator-payload`

- Story: [`../STORY-M2-02-06-data-model-registry-section-16-followup.md`](../STORY-M2-02-06-data-model-registry-section-16-followup.md)
- Decision Ref: [`../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md`](../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md) — §16 слой 1, **GAP-04** (закрыт: оркестратор + существующий intake `origin`)

## Task: implement — заполнение `origin.*` из GPT-оркестратора

### Цель
Чтобы `origin_source`, `origin_conversation_id`, `origin_tool_call_id` в `public.stories` не оставались NULL при штатном GPT-потоке (сейчас поля есть в домене, оркестратор их не шлёт).

### Факты из кода (§16)
1) `StoryRecord` содержит три поля origin — [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py).
2) `StoryIntakeService.create_story` маппит `request.origin` — [`src/core/application/services.py`](../../../../../../../src/core/application/services.py).
3) В `api-orchestrator.md §5.2.1` блок payload без `origin` — см. анализ §16.

### Gap / Проблема
Gateway уже парсит `origin`; закрытие — документированный минимальный JSON в `api-orchestrator.md §5.2.1`.

### AC/DoD
- [x] (P0) В GPT-инструкциях добавлен блок `origin` в пример и таблицу маппинга (`GPT UI/instructions/api-orchestrator.md`).
- [x] (P0) Gateway intake и `create_story` без изменений контракта (уже поддерживаются).
- [x] (P1) Contract-тест: `tests/test_story_intake_contract.py` (фикстура с `origin`).

### Где менять код
- GPT UI (корень воркспейса `DOGEstonia/`): [`GPT UI/instructions/api-orchestrator.md`](../../../../../../../../GPT%20UI/instructions/api-orchestrator.md)
- [`src/core/intake/contracts.py`](../../../../../../../src/core/intake/contracts.py) при расширении shape
- Тесты: [`tests/`](../../../../../../../tests/)

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_story_intake_contract.py tests/test_e2e_intake_create_doge_issue_contract.py
```

### Артефакты процесса (`task-execution-process.md`)
- [`BULLRUN-PHASE-LOG.md`](./BULLRUN-PHASE-LOG.md)
- [`implementation-plan-m2-02-06-t03.md`](./implementation-plan-m2-02-06-t03.md)
- [`acceptance-verification-m2-02-06-t03.md`](./acceptance-verification-m2-02-06-t03.md)
- [`retrospective-m2-02-06-t03-full.md`](./retrospective-m2-02-06-t03-full.md)
