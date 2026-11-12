# REQ-44: API_REFERENCE — field provenance clarity notes

**Статус:** requirements — ready for tasking  
**Источник:** `GPT UI/docs/audit-field-provenance-2026-05-24.md` (FINDING-01, FINDING-02)  
**Приоритет:** P3 (documentation-only; no runtime-breakage, no HTTP change)  
**Тип:** documentation update — `API_REFERENCE.md §6.3` only; no code changes  
**Серверная сторона:** docs-only; `contracts.py`, `services.py`, DB layer не затрагиваются  
**Парные задачи:** REQ-22 §2 (GPT UI, intentional design decision for `original_text`)

---

## 1. Контекст

Аудит провенанса полей (`audit-field-provenance-2026-05-24.md`) выявил два места в `API_REFERENCE.md §6.3`, где документация корректна для сервера, но вводит в заблуждение операторов и интеграторов:

1. **`narrative.original_text`** — поле называется "original text", но содержит GPT-переформулированное описание (`canonical_payload.description[session_language]`), а не дословный ввод пользователя. Это намеренный дизайн (REQ-22 §2), но в API_REFERENCE нет никакого предупреждения — таблица §6.3 говорит лишь "stored as-is (stripped)".

2. **`gpt_signals.*`** — три поля (`severity`, `impact_estimation`, `problem_status`) полностью выводятся GPT-классификатором; пользователь их не называл. Источник на уровне данных помечен как `"gpt_intake_v1"`, но раздел §6.3 не объясняет, что это GPT-only inference, а не user-stated значения.

Оба — информационные зазоры, существенные для:
- Операторов и аналитиков, читающих БД или API-ответы
- Downstream ML/аналитики на `story_signals`
- Правовых/надзорных контекстов (civic complaint traceability)

---

## 2. Текущее состояние

### 2.1 `original_text` — строка 276

```markdown
| `original_text` | string | **yes** | Non-empty after `.strip()` | stored as-is (stripped) |
```

Ниже таблицы (строка 287):
```markdown
**`language` vs `session_language`**: `language` is the language of `original_text`; 
`session_language` is the language the user is interacting in ...
```

Нет ни слова о том, что `original_text` = GPT-reframed civic description, не verbatim.

### 2.2 `gpt_signals` раздел — строки 348–362

```markdown
#### `gpt_signals` — object, optional (REQ-42)
...
Persisted `signals_json` always includes `"source": "gpt_intake_v1"`.
```

Нет явного указания, что все три поля block являются GPT classifier outputs (не пользовательскими заявлениями).

---

## 3. Целевое состояние

### 3.1 Изменение к `original_text` (строка 276)

В таблице narrative §6.3, колонка Normalization для `original_text`:

**Было:**
```
stored as-is (stripped)
```

**Стало:**
```
stored as-is (stripped). **Not verbatim user input** — contains GPT-reframed description in `session_language` (REQ-22 §2 intentional design; verbatim capture is out of scope).
```

### 3.2 Изменение к `language` vs `session_language` примечанию (строка 287)

Добавить второй абзац:

**Было:**
```markdown
**`language` vs `session_language`**: `language` is the language of `original_text`; 
`session_language` is the language the user is interacting in (may differ if GPT 
translated the story). Both validated against `I18N_LANGS = ("et", "ru", "en")`.
```

**Стало:**
```markdown
**`language` vs `session_language`**: `language` is the language of `original_text`; 
`session_language` is the language the user is interacting in (may differ if GPT 
translated the story). Both validated against `I18N_LANGS = ("et", "ru", "en")`.

**`original_text` provenance**: this field contains the GPT-reframed civic description 
in `session_language` (the `canonical_payload.description[session_language]` produced 
by the GPT normalizer), not the verbatim words the user spoke. This is intentional per 
REQ-22 §2. Operators reading this field from the database should treat it as a 
structured civic restatement, not a literal quote.
```

### 3.3 Изменение к `gpt_signals` разделу (после строки 360)

Добавить примечание после строки про `signals_json source`:

**Было:**
```markdown
Persisted `signals_json` always includes `"source": "gpt_intake_v1"`. A failure to 
persist signals is logged and does **not** change HTTP `202` for the intake.
```

**Стало:**
```markdown
Persisted `signals_json` always includes `"source": "gpt_intake_v1"`. A failure to 
persist signals is logged and does **not** change HTTP `202` for the intake.

**Provenance note**: all three `gpt_signals` fields are GPT classifier outputs — they 
represent the GPT's inference from interview context, not values explicitly stated by 
the user. `severity` and `impact_estimation` are fully inferred; `problem_status` may 
reflect a direct user statement or GPT inference — the distinction is not preserved at 
the wire level. Downstream analytics on `story_signals` should treat these as 
`gpt_intake_v1` machine labels, not user-declared attributes.
```

---

## 4. Файлы для изменения

| Файл | Секция | Что изменяется |
|------|--------|----------------|
| `docs/runtime-docs/api-reference/API_REFERENCE.md` | §6.3 `narrative` table | `original_text` normalization column → добавить "Not verbatim user input" |
| `docs/runtime-docs/api-reference/API_REFERENCE.md` | §6.3 после narrative table | Добавить `original_text` provenance paragraph |
| `docs/runtime-docs/api-reference/API_REFERENCE.md` | §6.3 `gpt_signals` section | Добавить provenance note после строки про `gpt_intake_v1` |

Код не изменяется.

---

## 5. Acceptance Criteria

- [ ] `API_REFERENCE.md §6.3` строка `original_text` в таблице содержит предупреждение "Not verbatim user input" с ссылкой на REQ-22 §2
- [ ] `API_REFERENCE.md §6.3` содержит абзац, объясняющий что `original_text` = GPT-reframed `description[session_language]`
- [ ] `API_REFERENCE.md §6.3` раздел `gpt_signals` содержит provenance note: "all three fields are GPT classifier outputs, not user-declared attributes"
- [ ] Остальные разделы API_REFERENCE.md не затронуты (нет регрессий в других секциях)

---

## 6. Не в scope этого REQ

- Изменения в `contracts.py`, `services.py`, или любых Python-файлах
- Добавление нового поля `verbatim_text` или raw capture — это product backlog (R-03 из аудита)
- Изменения в GPT-инструктажных файлах (scope REQ-28, REQ-29)
- Изменения в OpenAPI schema
- Изменения в других разделах API_REFERENCE (§1–5, §7+)
