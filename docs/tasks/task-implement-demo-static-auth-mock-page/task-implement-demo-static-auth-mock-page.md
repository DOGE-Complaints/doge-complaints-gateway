## Task: implement — demo static auth mock page for fixed user

### Цель
Подготовить отдельную static `html/css` страницу для demo-сценария «внешняя авторизация в экосистеме DOGEstonia» с фиксированным пользователем, чтобы запуск демо выглядел цельным и понятным для non-technical аудитории.

### Почему это важно (риск)
Сейчас runtime не содержит выделенной визуальной точки входа для демонстрации auth-шага. Без отдельного экрана продуктовый narrative «как пользователь входит в экосистему» теряется, и демо воспринимается как набор технических операций без user journey.

### Scope
Входит в задачу:
- статическая страница (`html/css`) без backend-auth интеграции;
- фиксированный demo-профиль пользователя;
- продуктово оформленный flow: welcome -> action -> loading -> success -> continue;
- визуальные элементы для качественной подачи (DOGE-персонаж, copy, лоадер «гав-гав»);
- стилистическая совместимость с `spa-app` как UI baseline.

Не входит:
- production SSO/OAuth/OIDC;
- хранение реальных токенов/сессий;
- финальная дизайн-система и пиксель-перфект.

### Факты из кода (Code Facts / SSOT)
1) В `doge-complaints-gateway` отсутствуют статические веб-страницы:
- Поиск `*.html` и `*.css` в репозитории возвращает 0 файлов.

2) Текущий runtime API — handler-driven backend слой:
- `src/core/api/handlers.py` содержит только API handlers (`health/readiness/protected/metrics`), UI-view слой в этом модуле не реализован.

3) В `spa-app` уже есть готовый визуальный baseline:
- `spa-app/src/index.css` задаёт цветовую схему, типографику, CTA-паттерны, skeleton-анимации.

4) В `spa-app/public/assets` уже есть бренд-ресурсы:
- например `DOGEstonia-logo-fallback.svg`, которые можно использовать как отправную точку для demo-экрана.

### Gap / Проблема
- Нет выделенного demo auth-entry экрана.
- Нет визуального контракта «пользователь авторизуется в DOGEstonia» перед основным сценарным потоком демо.
- Нет даже минимальной static-реализации, которую можно показать продукту/стейкхолдерам для быстрого первого прогона.

### AC/DoD
- [x] (P0) Добавлена отдельная static страница demo auth (`.html` + `.css`) с фиксированным пользователем.
- [x] (P0) Экран содержит:
  - [x] заголовок и copy про вход в экосистему DOGEstonia;
  - [x] CTA «Авторизоваться в экосистеме DOGEstonia»;
  - [x] визуальный блок DOGE-персонажа/брендинга;
  - [x] loading-state с сообщением «гав-гав»;
  - [x] success-state и кнопку перехода в следующий demo flow.
- [x] (P1) Стиль страницы согласован с базовыми токенами/паттернами из `spa-app`.
- [x] (P1) Добавлен короткий runbook как открыть страницу локально и проверить сценарий вручную.

### Где менять код
В `doge-complaints-gateway`:
- добавить новую директорию для static demo auth page;
  - выбранный путь реализации: `demo/auth-page/`.
- создать:
  - `index.html`
  - `styles.css`

Дополнительно:
- при необходимости добавить readme/runbook в ту же директорию;
- использовать как ориентир визуальные паттерны из:
  - `/Users/eslinko/Development/DOGEstonia/spa-app/src/index.css`
  - `/Users/eslinko/Development/DOGEstonia/spa-app/public/assets/*`

### План выполнения (Execution Plan)
1) Зафиксировать структуру static-страницы и текстовый сценарий demo flow.
2) Собрать high-level layout (hero, profile block, CTA, loading, success).
3) Добавить стили с опорой на `spa-app` visual baseline.
4) Проверить локально сценарий от первого экрана до success-state.
5) Описать smoke-проверку и ограничения demo-уровня в кратком runbook.

### Команды проверки (Verification Commands)
```bash
# Вариант 1: открыть html напрямую в браузере
open /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/demo/auth-page/index.html

# Вариант 2: через локальный static server
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/demo/auth-page
python3 -m http.server 8080
# затем открыть http://localhost:8080
```
