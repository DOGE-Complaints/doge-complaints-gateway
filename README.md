# DOGEComplaints — Demo Architecture Branch

Эта ветка (`demo-ready-april-26`) является **docs-only baseline** для Demo/Pilot архитектуры Module 2:
- Web2 Core / Story Intelligence Layer;
- solution architecture;
- requirements pack;
- audit и аналитические материалы.

Код рантайма legacy-репозитория в этой ветке намеренно удалён, чтобы зафиксировать чистый архитектурный контур без смешивания со старой реализацией.

## Точка входа

- `docs/solution architecture/00-index.md`

## Состав документации

- `docs/requirements/` — детализированные продуктовые и технические требования;
- `docs/solution architecture/` — модульная целевая архитектура demo (pilot-ready adapters);
- `docs/analysis/` — стратегический анализ, включая выбор legacy vs greenfield;
- `docs/01-04-*.md` — технический, data, supabase и security audits.

## Важно

- Ветка предназначена для архитектурного согласования и планирования реализации.
- Реализация нового кода ожидается в последующих ветках/этапах.

## Конфигурация (greenfield runtime)

- Шаблон переменных окружения для Supabase и связанных настроек: `example.env` (копировать в `.env` локально; не коммитить секреты).

## License

MIT License, см. `LICENSE`.
