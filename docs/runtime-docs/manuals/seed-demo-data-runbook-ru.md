# Наполнение демо-данными с нуля — runbook (как наполнить базу и доску)

> Этот мануал — **сквозной процесс** «загрузить истории → получить карточки на доске». Детали самого загрузчика — в [`simulation-runner-manual.md`](../testing/simulation-runner-manual.md) (SSOT по загрузке); здесь — вся цепочка целиком. Метод: `.cursor/rules/analysis.mdc` — шаги по фактическому коду.
>
> Статус разделов: загрузка/проверка — **verified, работает сейчас**; раздел про объём кластеров зависит от расширенного датасета ([STORY-GW-SEED-02](../../tasks/backlog-stories/demo-data-seeding/STORY-GW-SEED-02-dataset-expansion-for-clustering.md)).

## Главное за 30 секунд

Доска показывает **issue-карточки**, а не сырые истории. Поэтому процесс **двухступенчатый**:

```
1) Вы грузите истории        2) Система сама кластеризует (cron)        3) Доска
POST /intake/stories    →    объединяет ≥8 похожих в одну issue    →    GET /tallinn/issues
```

**Если просто загрузить истории — доска останется пустой**, пока кластеризация не соберёт группу из **≥8 похожих** историй. Это by design.

---

## Термины простыми словами

- **История (story)** — сырое обращение жителя. Грузится скриптом.
- **Issue (карточка)** — то, что на доске. Создаётся не при загрузке, а **кластеризацией**.
- **Кластеризация** — фоновое объединение похожих историй (по меткам `canonical_labels`) в группы.
- **`CLUSTER_MIN_SIZE`** = 8 — минимум историй в группе, чтобы она стала карточкой.
- **cron** — встроенный таймер сервиса, который периодически запускает кластеризацию (`CLUSTER_CRON_ENABLED`, интервал `CLUSTER_CRON_INTERVAL_S`, по умолчанию 60s). **Ручной кнопки «кластеризуй сейчас» нет** — только этот таймер.
- **проекция (projection)** — готовая issue в таблице `doge_issues`, которую читает доска.

---

## Предусловия (проверить ДО загрузки)

Цель — hosted-демо (Railway + Supabase).

1. **Сервер в режиме Supabase.** Данные попадут в облако только если у gateway `DB_BACKEND=supabase`. Иначе пишется в in-memory/sqlite и в hosted-БД ничего не появится.
2. **Готовность БД — `/ready` зелёный:**
   ```bash
   curl -sS "$GATEWAY_URL/ready" | jq '{db_ready, db_checks}'
   # ожидается: db_ready: true; все db_checks: true
   ```
   ⚠️ Если `db_checks.columns: false` — на hosted **не применены columnar-миграции** (RC-04). Примените `supabase/migrations/20260619_1200/1210/1220` к проекту Supabase **до** загрузки, иначе проекции не запишутся/не прочитаются. (Подробно — [audit-gw-rc-04](../../analysis/audit-gw-rc-04-columnar-model-migration-2026-06-20.md).)
3. **Кластеризация включена:** на сервере `CLUSTER_CRON_ENABLED=true` (по умолчанию true). Без неё истории загрузятся, но карточек не будет никогда.
4. **Достаточно историй для ≥8/кластер.** Текущий `dogestonia_simulation_canvas_v0_1.json` (130 историй) разнороден по меткам — кластер ≥8 не гарантирован. Для заполненной доски используйте расширенный датасет **v0_2**: `tests/sandbox/dogestonia_simulation_canvas_v0_2.json` ([SEED-02](../../tasks/backlog-stories/demo-data-seeding/STORY-GW-SEED-02-dataset-expansion-for-clustering.md); ожидаемо **2** issue-карточки — см. [`expected-board-fill-matrix.md`](../../tasks/epics/EPIC-M2-19-demo-data-seeding/stories/STORY-GW-SEED-02-dataset-expansion-for-clustering/task-gw-seed-02-t04-expected-board-fill-matrix/expected-board-fill-matrix.md)).

---

## Шаг 1 — Настроить загрузчик

```bash
cd doge-complaints-gateway
cp .env.test.example .env.test
# заполнить в .env.test:
#   GATEWAY_URL=https://<твой-railway>.up.railway.app
#   GATEWAY_API_TOKEN=<SERVICE_API_TOKEN сервера>
#   SIMULATION_CANVAS_PATH=tests/sandbox/dogestonia_simulation_canvas_v0_1.json   (или _v0_2 из SEED-02)
```

## Шаг 2 — Smoke (10 историй) — убедиться, что доезжает

```bash
python3 tests/simulation_runner.py --max 10
# ожидается: 200/202 OK, story_id=...; Success: 10
```
Проверка записи:
```sql
-- в Supabase SQL editor
select count(*) from stories where submitter_external_user_id like 'sim:%';
```

## Шаг 3 — Полная загрузка

```bash
python3 tests/simulation_runner.py          # все истории из canvas
# или make simulate
```
Exit code 0 — все приняты; 1 — есть Failed IDs (см. вывод).

## Шаг 4 — Дождаться кластеризации (cron)

Кластеризация идёт **сама**, по таймеру. Чтобы не ждать долго на время seed — на сервере можно временно поставить короткий интервал и убедиться, что включено:
```
CLUSTER_CRON_ENABLED=true
CLUSTER_CRON_INTERVAL_S=20        # на время seed; вернуть к 60 после
```
Подождите 1–2 интервала. (Ручного триггера нет — это ожидание by design.)

## Шаг 5 — Проверить, что доска наполнилась

```bash
curl -sS "$GATEWAY_URL/tallinn/issues" | jq '.data.issues | length'
# > 0  → карточки появились
curl -sS "$GATEWAY_URL/tallinn/issues" | jq '.data.issues[0] | {id,status,type,labels}'
```
И открыть SPA-доску (`/board`) в режиме GFL-DRIVEN — должны быть карточки.

---

## Если доска пустая — диагностика

| Симптом | Причина | Что делать |
|---|---|---|
| `stories` пустая после загрузки | сервер не в `DB_BACKEND=supabase` (писалось не в hosted) | проверить конфиг сервера; см. [simulation-runner-manual §FAQ](../testing/simulation-runner-manual.md) |
| `stories` есть, `/tallinn/issues` пуст | кластеры <8 ИЛИ cron выключен ИЛИ не дождались тика | проверить `CLUSTER_CRON_ENABLED=true`; подождать интервал; расширить датасет (SEED-02) |
| `/ready` → `columns: false` | columnar-миграции RC-04 не применены на hosted | применить `20260619_1200/1210/1220` к Supabase |
| `GET /tallinn/issues` ошибка/500 | то же — отсутствуют columnar-колонки | применить миграции, перепроверить `/ready` |

---

## Связанные документы
- Загрузчик (детали, переменные, группы): [`simulation-runner-manual.md`](../testing/simulation-runner-manual.md)
- Решения и контекст: [`interview-seed-demo-data-2026-06-20.md`](../../analysis/interview-seed-demo-data-2026-06-20.md)
- Пакет стори: [`demo-data-seeding/INDEX.md`](../../tasks/backlog-stories/demo-data-seeding/INDEX.md)
- RC-04 ops (columnar на hosted): [`audit-gw-rc-04-...`](../../analysis/audit-gw-rc-04-columnar-model-migration-2026-06-20.md)
