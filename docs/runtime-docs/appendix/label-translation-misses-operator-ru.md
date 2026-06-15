# Оператор: просмотр непереведённых меток (GW-L10N-03)

**Story:** STORY-GW-L10N-03 · **Таблица:** `label_translation_misses` · **View (Supabase):** `label_translation_misses_ranked`

Анонимная телеметрия с фронта: когда humanize не находит перевод метки, SPA шлёт `POST /telemetry/label-misses` с `{label_key, locale}`. PII не собирается.

## Топ ключей по локали (Supabase / psql)

```sql
SELECT locale, label_key, miss_count, last_seen_at
FROM public.label_translation_misses_ranked
WHERE locale = 'et'
ORDER BY miss_count DESC, last_seen_at DESC
LIMIT 50;
```

## Прямой запрос к таблице

```sql
SELECT label_key, locale, miss_count, last_seen_at
FROM public.label_translation_misses
ORDER BY last_seen_at DESC
LIMIT 100;
```

## SQLite (локальные тесты / dev)

```sql
SELECT label_key, locale, miss_count, last_seen_at
FROM label_translation_misses
WHERE locale = 'ru'
ORDER BY miss_count DESC, last_seen_at DESC;
```

## Связанные артефакты

- Endpoint: `POST /telemetry/label-misses` — [`openapi.yaml`](../api-reference/openapi.yaml)
- Миграции: `supabase/migrations/20260615_1200_gw_l10n_03_label_translation_misses.sql`, `20260615_1210_gw_l10n_03_label_translation_misses_ranked_view.sql`
- Тесты: `tests/test_gw_l10n_03_label_miss_telemetry.py`
