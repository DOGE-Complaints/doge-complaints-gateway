## Task: refactor — demo auth page delivery boundary

### Цель
Привести delivery модель mock auth страницы к устойчивому best-practice baseline: четко отделить runtime API boundary от demo static boundary и зафиксировать эксплуатационный контракт.

### Почему это важно (риск)
Если статическая demo-страница обслуживается ad-hoc вместе с API без формализованного контракта, со временем растет риск смешивания responsibilities и неявных regressions в gateway boundary.

### Scope
Входит:
- формализация способа публикации `demo/auth-page` (что обслуживает и в каком режиме);
- фиксация boundary-контракта в runtime docs;
- устранение неявных связей между API route-map и static demo delivery.

Не входит:
- полный UI редизайн страницы;
- миграция demo auth на отдельный frontend repo.

### Факты из кода (Code Facts / SSOT)
1) `demo/auth-page/index.html` + `styles.css`
- mock auth flow существует как отдельный static набор.

2) `src/core/api/asgi_app.py`
- API и static demo page отдаются одним ASGI процессом через FastAPI routes (`FileResponse` для `/demo/auth-page`).

3) `docs/runtime-docs/server-env-quickstart.md`
- содержит инструкции по запуску локального сервера и URL mock auth страницы.

### Gap / Проблема
- Нет явно задокументированного decision record: это временная dev-only схема или целевая delivery модель.
- Статический и API boundary связаны в одном техническом механизме без формального separation policy.

### AC/DoD
- [x] (P0) Задокументирован формальный boundary contract: API routes vs demo static routes.
- [x] (P0) Зафиксирован target operating mode (dev-only combined delivery или split delivery).
- [x] (P1) Runtime quickstart и operations playbook синхронизированы с выбранной моделью.
- [x] (P1) Добавлены smoke-check критерии для demo page delivery.

### Где менять код
- `docs/runtime-docs/server-env-quickstart.md`
- `docs/runtime-docs/operations-playbook.md`
- `src/core/api/asgi_app.py` (при изменении delivery routes или split-стратегии)
- `demo/auth-page/README.md`

### План выполнения (Execution Plan)
1) Зафиксировать decision по boundary модели (combined vs split).
2) Обновить runtime docs и runbook под выбранную модель.
3) При необходимости минимально рефакторить delivery слой.
4) Добавить smoke-check шаги в документацию.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m core.api.asgi_app
# проверить /health и /demo/auth-page
```
