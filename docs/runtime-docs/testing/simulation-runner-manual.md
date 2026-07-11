# Simulation Runner — Руководство

Скрипт `tests/simulation_runner.py` загружает тестовые истории из canvas-файла в задеплоенное приложение через реальные HTTP-запросы: **stash** (service) → **submit** (user).

> Это **SSOT по загрузке** (детали скрипта, env, группы). Нужна **вся цепочка** «загрузка → кластеризация (cron) → карточки на доске»? — см. сквозной e2e-runbook: [`seed-demo-data-runbook-ru.md`](../manuals/seed-demo-data-runbook-ru.md). Загрузка историй сама по себе доску **не** наполняет — карточки создаёт кластеризация (≥8 на группу).

---

## Быстрый старт

```bash
# 1. Создай файл настроек (один раз)
cp .env.test.example .env.test

# 2. Отредактируй .env.test — заполни обязательные поля:
#    GATEWAY_URL, GATEWAY_API_TOKEN, GATEWAY_USER_EMAIL, GATEWAY_USER_PASSWORD,
#    SUPABASE_URL, SUPABASE_ANON_KEY

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
| `GATEWAY_API_TOKEN` | **ДА** | **Сервисный** токен (`SERVICE_API_TOKEN` на сервере) → `POST /story-drafts` stash — **201** + `draft_id` |
| `GATEWAY_USER_EMAIL` | **ДА** | Email **вашего** демо-пользователя Supabase Auth (уже `phone_verified`) |
| `GATEWAY_USER_PASSWORD` | **ДА** | Пароль этого пользователя; runner обменивает на Supabase `access_token` на старте (in-memory) |
| `SUPABASE_URL` | **ДА** | URL Supabase-проекта (из SPA `VITE_SUPABASE_URL`) — для `POST …/auth/v1/token?grant_type=password` |
| `SUPABASE_ANON_KEY` | **ДА** | Публичный anon-ключ (из SPA `VITE_SUPABASE_ANON_KEY`) — заголовок `apikey` при логине |
| `SIMULATION_CANVAS_PATH` | нет | Путь к JSON-файлу со сценариями. По умолчанию: `tests/sandbox/dogestonia_simulation_canvas_v0_1.json`. Для наполнения доски (≥2 карточки): `tests/sandbox/dogestonia_simulation_canvas_v0_2.json` |
| `SIMULATION_GROUPS` | нет | Фильтр групп через запятую. Пусто = все группы |
| `SIMULATION_MAX_STORIES` | нет | Максимум историй за прогон. Пусто = все |

### Пример `.env.test`

```dotenv
GATEWAY_URL=https://dogestonia-tallinn.up.railway.app
GATEWAY_API_TOKEN=111.444.555.888.555.444.111-Tallinn-demo-token
GATEWAY_USER_EMAIL=demo-user@example.com
GATEWAY_USER_PASSWORD=your-demo-password
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key

SIMULATION_CANVAS_PATH=tests/sandbox/dogestonia_simulation_canvas_v0_2.json

# Опционально — оставь пустым чтобы взять все
SIMULATION_GROUPS=
SIMULATION_MAX_STORIES=
```

---

## Вызов с аргументами

CLI-аргументы перекрывают переменные окружения.

```bash
# Все сценарии из canvas
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
Canvas: tests/sandbox/dogestonia_simulation_canvas_v0_2.json (18 scenarios selected)
Target: https://dogestonia-tallinn.up.railway.app
Flow: POST /story-drafts (stash) -> POST /story-drafts/{id}/submit

[  1/18] DOGE-EST-SC-V02-001 -> 201 stash draft_id=abc... -> 202 submit story_id=def...
[  2/18] DOGE-EST-SC-V02-002 -> 201 stash draft_id=ghi... -> 202 submit story_id=jkl...
[ 15/18] DOGE-EST-SC-V02-015 -> 403 ERROR detail=...

Summary:
  Total:   18
  Success: 17
  Failed:  1
  Failed IDs: DOGE-EST-SC-V02-015
```

Exit code 0 — все истории приняты (stash **201** + submit **202**).  
Exit code 1 — есть ошибки (список в `Failed IDs`).

### Что означают HTTP-коды

| Код | Фаза | Что случилось |
|---|---|---|
| 201 | stash | Draft создан, получен `draft_id` |
| 202 | submit | Story материализована, получен `story_id` |
| 400 | обе | Невалидный payload (проблема в данных) |
| 401 | stash | Неверный или отсутствующий `GATEWAY_API_TOKEN` |
| 401 | submit | Supabase-токен невалиден/просрочен (fail-closed) |
| 403 | submit | User не verified (`phone_verified=false`) — верифицируй телефон в SPA один раз |
| 503 | stash | Сервер не готов (БД/конфиг) — см. `/ready` |
| 500 | обе | Ошибка на стороне сервера |

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

**Где взять email+password?**  
**Свой** демо-аккаунт Supabase Auth с `phone_verified=true`. Зарегистрируйся в SPA, пройди верификацию телефона один раз — затем положи те же email+password в `.env.test`. Runner **не** создаёт и **не** верифицирует аккаунты (fail-closed).

**Где взять `SUPABASE_URL` / `SUPABASE_ANON_KEY`?**  
Из конфига SPA (`VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`) или dashboard Supabase-проекта identity/SPA.

**Можно запускать локально против dev-сервера?**  
Да: `GATEWAY_URL=http://localhost:8000`, service token из локального `.env`, user creds из своего verified аккаунта.

**Как убедиться что истории попали в базу?**  
Зависит от **`DB_BACKEND` на стороне сервера**, на который указывает `GATEWAY_URL`. Если сервер в режиме Supabase, после прогона в таблице `stories` появятся строки с `origin_source = 'simulation'`. Если сервер в in-memory/sqlite без облака — это **не** hosted Supabase; см. разбор: [`docs/analysis/simulation-runner-local-run-validation-2026-05-11.md`](../../analysis/simulation-runner-local-run-validation-2026-05-11.md).

**Скрипт требует зависимостей?**  
Для HTTP достаточно стандартной библиотеки. Сборка payload импортирует `INTAKE_SCHEMA_VERSION` из пакета `core` (каталог `src/` добавляется в `sys.path` при старте скрипта), поэтому запускай из корня `doge-complaints-gateway` как в примерах выше.
