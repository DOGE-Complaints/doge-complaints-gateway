# GAP-28-02 status check: lifespan test for `CLUSTER_CRON_ENABLED=false`

## Контекст проверки

Проверка выполнена по запросу после внешнего аудита, который сообщил:

- `TASK-CRON-LIFESPAN-TEST-01` не закрыта;
- нового теста на lifespan-ветку с отключенным cron не найдено.

## Что проверено в коде (факты)

1. В проекте есть отдельный тестовый файл:
   - `tests/test_asgi_lifespan_cron.py`
2. В этом файле есть тест:
   - `test_lifespan_does_not_start_cron_when_disabled`
3. Тест патчит `core.api.asgi_app.ClusterCronJob` и `get_api_dependencies`, запускает `TestClient(asgi_app.app)` и проверяет, что `start()` не вызывался при `cluster_cron_enabled=False` (`events == []`).
4. Lifespan-ветка в runtime действительно условная:
   - `src/core/api/asgi_app.py` создаёт и стартует `ClusterCronJob` только внутри `if deps.config.cluster_cron_enabled:`.

## Локальная верификация

Выполнена команда:

```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_asgi_lifespan_cron.py --tb=short
```

Результат:

- `1 passed in 0.27s`

## Почему внешний аудитор мог увидеть GAP как открытый

Текущий активный YAML-пакет (`pkg-000004-20260505-m2-16.yaml`) в очереди `--list` содержит только `primary + T01..T06`.

`T07/T08/T09` в этот snapshot не входят, поэтому аудит, ориентированный только на активный пакет/его выполненные артефакты, мог считать `TASK-CRON-LIFESPAN-TEST-01` не закрытой, даже при наличии уже добавленного кода и теста в рабочем дереве.

## Вывод

- По факту в кодовой базе тест для `GAP-28-02` присутствует и исполняется успешно.
- Статус «открыто» у внешнего аудитора вероятнее связан с рассинхронизацией между active package snapshot и фактическими изменениями по `T08`.

