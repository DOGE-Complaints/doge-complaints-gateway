## Task workspace — `task-m2-04-05-t08-gap34-01-env-remove-legacy-lens-block`

- Story: [`../STORY-M2-04-05-civic-canonical-signal-pipeline.md`](../STORY-M2-04-05-civic-canonical-signal-pipeline.md)
- Decision Ref: [`../../../../../../analysis/audit-req34-civic-clustering-canonical-pipeline-2026-05-15.md`](../../../../../../analysis/audit-req34-civic-clustering-canonical-pipeline-2026-05-15.md) GAP-34-01

---
**Приоритет:** P0  
**Сложность:** S  
**Оценка времени:** < 15 мин  
**Статус:** ready  
**Supersedes / Superseded by:** complements T03 (example.env); does not reopen T01–T07 code wave  
---

## Task: fix — remove legacy CLUSTER_* block from operator `.env`

### Цель
Закрыть **AC-8 (effective)** полностью: в репозиторном/операторском `.env` остаётся только civic-блок REQ-34, без «ядовитых» дублирующих ключей `topic_micro` / `CLUSTER_TIE_BREAKER=lexical`.

### Почему это важно (риск)
`merge_dotenv_from_path()` в [`src/core/config/env_file.py`](../../../../../../../src/core/config/env_file.py) применяет **last-value-wins**. Сейчас runtime корректен (civic-блок ниже), но удаление или перестановка строк 22–30 активирует legacy значения → `ConfigError` при старте или неверные линзы.

### Факты из кода
1. [`doge-complaints-gateway/.env`](../../../../../../../.env) L22–30 — незакомментированный legacy-блок:
   - `CLUSTER_ACTIVE_LENSES=topic_micro,need_local,...`
   - `CLUSTER_PRIMARY_LENS=topic_micro`
   - `CLUSTER_TIE_BREAKER=lexical`
2. Тот же файл L32–36 — civic override (эффективные значения):
   - six civic lenses, `CLUSTER_SIGNAL_SOURCE=canonical`, `CLUSTER_TIE_BREAKER=alpha`
3. [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py) L313–317 — `_parse_cluster_lenses()` отклоняет `topic_micro` и др.
4. [`example.env`](../../../../../../../example.env) — уже civic-only (эталон для оператора).

### Gap / Проблема
**GAP-34-01 (HIGH):** operational trap — единственное место, где civic pipeline может сломаться без изменения кода.

### AC/DoD
- [x] (P0) В `.env` удалены или закомментированы строки legacy-блока (L22–30 по аудиту); оставлен один civic-блок.
- [x] (P0) Нет дублирующих ключей `CLUSTER_ACTIVE_LENSES`, `CLUSTER_PRIMARY_LENS`, `CLUSTER_TIE_BREAKER`, `CLUSTER_TYPE_RESOLUTION` с конфликтующими значениями.
- [x] (P0) `load_config_from_env()` с merged `.env` даёт `cluster_active_lenses` = six civic IDs и `cluster_tie_breaker=alpha`.
- [x] (P1) Краткий комментарий в `.env` ссылается на REQ-34 / `example.env` (без копирования секретов).

### Где менять код
- [`doge-complaints-gateway/.env`](../../../../../../../.env) — operator file (не коммитить секреты; при коммите — только cluster keys без tokens)
- Сверка: [`example.env`](../../../../../../../example.env)

### План выполнения
1. Удалить legacy block (topic_micro, lexical tie-breaker).
2. Оставить civic six-lens block + `CLUSTER_SIGNAL_SOURCE=canonical`.
3. Локально: `python3 -c "from core.config import load_config_from_env; c=load_config_from_env(None); print(c.cluster_active_lenses, c.cluster_tie_breaker)"` из `doge-complaints-gateway/`.

### Команды проверки
```bash
cd doge-complaints-gateway
rg -n "topic_micro|CLUSTER_TIE_BREAKER=lexical" .env example.env
python3 -c "from core.config import load_config_from_env; c=load_config_from_env(None); assert 'topic_micro' not in c.cluster_active_lenses; assert c.cluster_tie_breaker=='alpha'"
```
