## Task workspace — `task-m2-02-06-t07-gap-02-03-simulation-runner-intake-payload-parity`

- Story: [`../STORY-M2-02-06-data-model-registry-section-16-followup.md`](../STORY-M2-02-06-data-model-registry-section-16-followup.md)
- Decision Ref: [`../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md`](../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md) — раздел **«Незакрытые хвосты — финальный прогон»**, таблица хвостов (GAP-02/03: `simulation_runner`)

## Task: fix — паритет `_scenario_to_payload()` с контрактом intake (title et/ru/en + summary)

### Цель
Remote-раннер [`tests/simulation_runner.py`](../../../../../../../tests/simulation_runner.py) должен отправлять тот же набор полей `narrative`, что ожидает gateway после STORY-M2-02-06 T01/T02; иначе прогон против live API **не верифицирует** мультиязычный title и summary, хотя данные в [`tests/sandbox/dogestonia_simulation_canvas_v0_1.json`](../../../../../../../tests/sandbox/dogestonia_simulation_canvas_v0_1.json) есть.

### Факты из кода
1. `_scenario_to_payload` (примерно L47–76 в `simulation_runner.py`) заполняет только `title_hint` для одного языка и не передаёт `title_hint_et` / `title_hint_ru` / `title_hint_en` и не передаёт объект `narrative.summary`.
2. Canvas-сценарии содержат `canonical_payload.title.{et,ru,en}` и `canonical_payload.summary.{et,ru,en}` — см. sandbox JSON.

### Gap / Проблема
Инструмент отстаёт от контракта; расхождение задокументировано в Decision Ref (таблица хвостов).

### AC/DoD
- [x] (P0) В `payload["narrative"]` добавлены опциональные строки `title_hint_et`, `title_hint_ru`, `title_hint_en` из `title_map` (как в анализе).
- [x] (P0) В `payload["narrative"]` добавлен объект `summary` с непустыми значениями из `summary_map` (ключи `et`/`ru`/`en` при наличии строк).
- [x] (P1) `schema_version` в payload по возможности выровнен с `INTAKE_SCHEMA_VERSION` из gateway (или явно задокументировано, почему остаётся литерал), без ломки remote-скрипта.
- [x] (P1) Короткая проверка: unit-импорт или ручной вызов функции с одним сценарием из canvas (по желанию — минимальный тест в T08).

### Где менять код
- [`tests/simulation_runner.py`](../../../../../../../tests/simulation_runner.py) — функция `_scenario_to_payload`.

### Команды проверки
После правки `_scenario_to_payload`: вручную или одноразовым скриптом убедиться, что для первого сценария canvas в `p["narrative"]` присутствуют ключи `title_hint_et`, `title_hint_ru`, `title_hint_en` и объект `summary` (если в canvas есть строки). Регресс перекрывается [`tests/test_e2e_simulation_canvas_intake.py`](../../../../../../../tests/test_e2e_simulation_canvas_intake.py) (T08) при согласованном построении payload.
