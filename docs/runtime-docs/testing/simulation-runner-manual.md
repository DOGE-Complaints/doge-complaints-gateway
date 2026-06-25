# Simulation Runner — Руководство

Скрипт `tests/simulation_runner.py` загружает тестовые истории из canvas-файла в задеплоенное приложение через реальные HTTP-запросы.

> Это **SSOT по загрузке** (детали скрипта, env, группы). Нужна **вся цепочка** «загрузка → кластеризация (cron) → карточки на доске»? — см. сквозной e2e-runbook: [`seed-demo-data-runbook-ru.md`](../manuals/seed-demo-data-runbook-ru.md). Загрузка историй сама по себе доску **не** наполняет — карточки создаёт кластеризация (≥8 на группу).

---

## Быстрый старт

```bash
# 1. Создай файл настроек (один раз)
cp .env.test.example .env.test

# 2. Отредактируй .env.test — заполни два обязательных поля:
#    GATEWAY_URL и GATEWAY_API_TOKEN

# 3. Запусти
python3 tests/simulation_runner.py
# или через Make:
make simulate
```

---

## Переменные окружения

### Где прописывать

Файл `.env.test` в корне проекта (`doge-complaints-gateway/.env.test`).  
Этот файл **не коммитится** в репозиторий — он у тебя локально.  
Шаблон лежит рядом: `.env.test.example`.

```
doge-complaints-gateway/
├── .env               ← production-конфиг (не трогай)
├── .env.test          ← твой тестовый конфиг (создай из .example)
├── .env.test.example  ← шаблон (коммитится в репо)
```

### Порядок загрузки

Скрипт читает `.env.test` **первым**, потом `.env`. Значения из `.env.test` имеют приоритет — переменные из `.env` загружаются только если они ещё не заданы. Переменные, уже установленные в shell-окружении, не перезаписываются.

### Все переменные

| Переменная | Обязательная | Описание |
|---|---|---|
| `GATEWAY_URL` | **ДА** | Адрес задеплоенного приложения, например `https://dogestonia-tallinn.up.railway.app` |
| `GATEWAY_API_TOKEN` | **ДА** | **Сервисный** токен канала (`SERVICE_API_TOKEN` из `.env` приложения) → заголовок `Authorization: Bearer`. Слой 1 «доверенный канал» (GW-GAUTH-01). |
| `GATEWAY_USER_TOKEN` | нет (но см. ⚠️) | **Пользовательский** токен → заголовок `X-User-Token`. Слой 2 «кто человек» (GW-GAUTH-01). **По умолчанию = `GATEWAY_API_TOKEN`** (`getenv("GATEWAY_USER_TOKEN", gateway_api_token)`, [`simulation_runner.py:172`](../../../tests/simulation_runner.py#L172)). ⚠️ Дефолт проходит, пока user-слой — заглушка присутствия; после реального introspection (**GW-GAUTH-02**) сюда нужен **настоящий пользовательский OAuth-токен**, иначе intake вернёт 401. |
| `SIMULATION_CANVAS_PATH` | нет | Путь к JSON-файлу со сценариями. По умолчанию: `tests/sandbox/dogestonia_simulation_canvas_v0_1.json` |
| `SIMULATION_GROUPS` | нет | Фильтр групп через запятую. Пусто = все группы |
| `SIMULATION_MAX_STORIES` | нет | Максимум историй за прогон. Пусто = все |

### Пример `.env.test`

```dotenv
GATEWAY_URL=https://dogestonia-tallinn.up.railway.app
GATEWAY_API_TOKEN=111.444.555.888.555.444.111-Tallinn-demo-token
# GATEWAY_USER_TOKEN=<пользовательский OAuth-токен>   # опц.; по умолчанию = GATEWAY_API_TOKEN (нужен реальный после GW-GAUTH-02)

SIMULATION_CANVAS_PATH=tests/sandbox/dogestonia_simulation_canvas_v0_1.json

# Опционально — оставь пустым чтобы взять все
SIMULATION_GROUPS=
SIMULATION_MAX_STORIES=
```

---

## Вызов с аргументами

CLI-аргументы перекрывают переменные окружения.

```bash
# Все 130 историй
python3 tests/simulation_runner.py

# Только 10 историй
python3 tests/simulation_runner.py --max 10

# Только группа infrastructure
python3 tests/simulation_runner.py --groups infrastructure

# Несколько групп, не более 20 историй
python3 tests/simulation_runner.py --groups infrastructure,environment --max 20
```

### Группы в canvas

| Группа | Историй | Содержание |
|---|---|---|
| `infrastructure` | 50 | Дороги, переходы, освещение, парковки |
| `environment` | 40 | Мусор, шум, озеленение, экология |
| `digital` | 25 | Цифровые сервисы, портал, e-gov |
| `conflict` | 15 | Конфликты интересов, жалобы на процесс |

---

## Как выглядит вывод

```
DOGEstonia Simulation Runner
Canvas: tests/sandbox/dogestonia_simulation_canvas_v0_1.json (130 scenarios selected)
Target: https://dogestonia-tallinn.up.railway.app

[  1/130] DOGE-EST-SC-001 -> 200 OK story_id=abc123...
[  2/130] DOGE-EST-SC-002 -> 200 OK story_id=def456...
[ 15/130] DOGE-EST-SC-015 -> 400 ERROR detail=...

Summary:
  Total:   130
  Success: 129
  Failed:  1
  Failed IDs: DOGE-EST-SC-015
```

Exit code 0 — все истории приняты.  
Exit code 1 — есть ошибки (список в `Failed IDs`).

### Что означают HTTP-коды

| Код | Что случилось |
|---|---|
| 200 | История принята, получен `story_id` |
| 400 | Невалидный payload (проблема в данных) |
| 401 | Неверный `GATEWAY_API_TOKEN` (сервисный слой), **или** отсутствует/невалиден `X-User-Token` (пользовательский слой, GW-GAUTH-01). Проверь оба токена. |
| 500 | Ошибка на стороне сервера |

---

## Smoke-проверка (10 историй из всех групп)

```bash
python3 tests/simulation_runner.py --max 10
```

Полезно убедиться что соединение работает перед полным прогоном.

---

## Часто задаваемые вопросы

**Где взять `GATEWAY_API_TOKEN`?**  
В файле `.env` проекта — значение поля `SERVICE_API_TOKEN`.

**Можно запускать локально против dev-сервера?**  
Да: `GATEWAY_URL=http://localhost:8000`, `GATEWAY_API_TOKEN=<твой локальный токен>`.

**Как убедиться что истории попали в базу?**  
Зависит от **`DB_BACKEND` на стороне сервера**, на который указывает `GATEWAY_URL`. Если сервер в режиме Supabase, после прогона в таблице `stories` появятся строки с `submitter_external_user_id`, начинающимся на `sim:`. Если сервер в in-memory/sqlite без облака — это **не** hosted Supabase; см. разбор реального прогона: [`docs/analysis/simulation-runner-local-run-validation-2026-05-11.md`](../../analysis/simulation-runner-local-run-validation-2026-05-11.md).

**Скрипт требует зависимостей?**  
Для HTTP достаточно стандартной библиотеки. Сборка payload импортирует `INTAKE_SCHEMA_VERSION` из пакета `core` (каталог `src/` добавляется в `sys.path` при старте скрипта), поэтому запускай из корня `doge-complaints-gateway` как в примерах выше.
