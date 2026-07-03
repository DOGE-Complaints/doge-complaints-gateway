# Наполнение демо-данными с нуля — runbook (как наполнить базу и доску)

> Этот мануал — **сквозной процесс** «загрузить истории → получить карточки на доске». Детали самого загрузчика — в [`simulation-runner-manual.md`](../testing/simulation-runner-manual.md) (SSOT по загрузке); здесь — вся цепочка целиком. Метод: `.cursor/rules/analysis.mdc` — шаги по фактическому коду.
>
> **Статус (2026-06-22, SEED-03):** цепочка intake→cron→проекция→доска **проверена end-to-end локально** — расширенный датасет `v0_2` ([SEED-02](../../tasks/backlog-stories/demo-data-seeding/STORY-GW-SEED-02-dataset-expansion-for-clustering.md), Done) даёт **2 карточки** на `GET /tallinn/issues` (см. [«Локальный e2e»](#локальный-e2e--быстрая-сквозная-проверка-без-hosted) и [verification](../../analysis/verify-gw-seed-03-end-to-end-2026-06-22.md)).
> ⚠️ **Hosted-прогон (Railway) временно заблокирован:** публичный `GET /tallinn/issues` отдаёт `INTERNAL_ERROR` из-за рассинхрона версии задеплоенного кода → чинит [STORY-GW-RC-07](../../tasks/backlog-stories/issues-read-contract/STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md). До закрытия RC-07 hosted-наполнение не проверяемо; локальный путь работает.

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
   - **Legacy service path на `/intake/stories` (GW-DRAFT-04).** Загрузчик `simulation_runner` шлёт истории только с `Authorization: Bearer` (`GATEWAY_API_TOKEN` = `SERVICE_API_TOKEN` на сервере). **Актуальный user submit в продукте:** GPT стешит → браузер сабмитит — [`story-draft-handoff`](../../tasks/backlog-stories/story-draft-handoff/INDEX.md). Детали env — [`simulation-runner-manual.md`](../testing/simulation-runner-manual.md) (SSOT).
     - **Коды отказа intake:** `401` (нет/битый сервисный токен) · `503` (сервер/БД не готов).
2. **Готовность БД — `/ready` зелёный:**
   ```bash
   curl -sS "$GATEWAY_URL/ready" | jq '.data.db | {ready, checks}'
   # ожидается: ready: true; все checks: true
   #   (контракт ответа: handle_readiness -> data.db.ready / data.db.checks; см. handlers.py)
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
#   GATEWAY_API_TOKEN=<SERVICE_API_TOKEN сервера>   # Authorization: Bearer (service-only intake)
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

Кластеризация идёт **сама**, по таймеру. Чтобы не ждать долго на время seed — на сервере временно поставить короткий интервал и убедиться, что включено:
```
CLUSTER_CRON_ENABLED=true
CLUSTER_CRON_INTERVAL_S=20        # на время seed; вернуть к 60 после
```
**Решение по интервалу (open question закрыт):** на время seed — `20s` (быстрый тик для демо), после наполнения **вернуть дефолт `60s`** (`CLUSTER_CRON_INTERVAL_S` без override; default из [schema.py](../../../src/core/config/schema.py)). Подождите 1–2 интервала. (Ручного триггера нет — это ожидание by design; код пути — [handlers.py: intake `cron_deferred`/`not_clustered`](../../../src/core/api/handlers.py).)

## Шаг 5 — Проверить, что доска наполнилась

```bash
curl -sS "$GATEWAY_URL/tallinn/issues" | jq '.data.issues | length'
# > 0  → карточки появились
curl -sS "$GATEWAY_URL/tallinn/issues" | jq '.data.issues[0] | {id,status,type,labels}'
```
И открыть SPA-доску (`/board`) в режиме GFL-DRIVEN — должны быть карточки.

---

## Локальный e2e — быстрая сквозная проверка без hosted

Когда hosted недоступен/заблокирован (см. статус-баннер про RC-07), всю цепочку можно проверить **локально на изолированном sqlite** (не трогая прод-данные). Это реальный прогон intake→cron→проекция→доска на актуальном коде:

```bash
cd doge-complaints-gateway
# изолированный sqlite + порог 8 + расширенный датасет v0_2
APP_PROFILE=demo API_BASE_URL=https://demo.example/api REQUEST_TIMEOUT_S=15 \
CLUSTER_MIN_SIZE=8 CLUSTER_READINESS_THRESHOLD=8 \
DB_BACKEND=sqlite DATABASE_URL="sqlite:////tmp/seed_demo.sqlite" \
SUPABASE_URL= SUPABASE_SERVICE_ROLE= \
/usr/local/bin/python3.11 -m pytest tests/test_gw_seed_02_cluster_density.py -q
# 4 passed → кластеризация v0_2 формирует ≥2 issue-проекции при min_size=8
```

**Фактический результат e2e (2026-06-22, [verification](../../analysis/verify-gw-seed-03-end-to-end-2026-06-22.md)):** intake 18 (202) → `process_all_pending`=2 → `GET /tallinn/issues` HTTP 200, **2 карточки** PUBLISHED:
- `waste`/Kalamaja — «Переполненные мусорные баки во дворе Каламая»
- `roads`/Lasnamäe — «Выбоины на жилой улице в Ласнамяэ»

Совпадает с [`expected-board-fill-matrix.md`](../../tasks/epics/EPIC-M2-19-demo-data-seeding/stories/STORY-GW-SEED-02-dataset-expansion-for-clustering/task-gw-seed-02-t04-expected-board-fill-matrix/expected-board-fill-matrix.md) (2 issue: Kalamaja+Lasnamäe).

---

## Если доска пустая — диагностика

| Симптом | Причина | Что делать |
|---|---|---|
| `stories` пустая после загрузки | сервер не в `DB_BACKEND=supabase` (писалось не в hosted) | проверить конфиг сервера; см. [simulation-runner-manual §FAQ](../testing/simulation-runner-manual.md) |
| `stories` есть, `/tallinn/issues` пуст | кластеры <8 ИЛИ cron выключен ИЛИ не дождались тика | проверить `CLUSTER_CRON_ENABLED=true`; подождать интервал; расширить датасет (SEED-02) |
| `/ready` → `checks.columns: false` | columnar-миграции RC-04 не применены на hosted | применить `20260619_1200/1210/1220` к Supabase |
| `GET /tallinn/issues` = `INTERNAL_ERROR`, **но `/ready` зелёный** | **deploy drift** — на сервере крутится старая сборка кода (до RC-04/05/06), падает на новом формате строк. Данные при этом целы (тот же набор отдаётся локальным актуальным кодом). | передеплоить актуальный код на таргет (deploy version parity); разбор — [STORY-GW-RC-07](../../tasks/backlog-stories/issues-read-contract/STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md) |
| `GET /tallinn/issues` ошибка **и** `/ready` `columns:false` | отсутствуют columnar-колонки | применить миграции, перепроверить `/ready` |

---

## Связанные документы
- Загрузчик (детали, переменные, группы) — **SSOT по загрузке**: [`simulation-runner-manual.md`](../testing/simulation-runner-manual.md)
- Решения и контекст: [`interview-seed-demo-data-2026-06-20.md`](../../analysis/interview-seed-demo-data-2026-06-20.md)
- Пакет стори: [`demo-data-seeding/INDEX.md`](../../tasks/backlog-stories/demo-data-seeding/INDEX.md)
- Ожидаемое наполнение доски (SEED-02 T04): [`expected-board-fill-matrix.md`](../../tasks/epics/EPIC-M2-19-demo-data-seeding/stories/STORY-GW-SEED-02-dataset-expansion-for-clustering/task-gw-seed-02-t04-expected-board-fill-matrix/expected-board-fill-matrix.md)
- E2E verification (SEED-03): [`verify-gw-seed-03-end-to-end-2026-06-22.md`](../../analysis/verify-gw-seed-03-end-to-end-2026-06-22.md)
- RC-04 ops (columnar на hosted): [`audit-gw-rc-04-...`](../../analysis/audit-gw-rc-04-columnar-model-migration-2026-06-20.md)
- Hosted board 500 (deploy drift): [`STORY-GW-RC-07`](../../tasks/backlog-stories/issues-read-contract/STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md)

> **SSOT-разграничение (T04):** детали загрузчика (env, группы, флаги) — только в `simulation-runner-manual.md`; сквозной e2e (предусловия→cron→доска) — этот файл. Дублирования нет: runner-manual ссылается сюда за полной цепочкой, этот — туда за деталями загрузки.
