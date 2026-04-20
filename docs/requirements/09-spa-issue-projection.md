# 09. Проекция в SPA-домен Issue

## Контракт совместимости (MVP hard constraint)
Обязательные поля: `id`, `status`, `type`, `labels`, `title`, `summary`, `description`.

Опциональные: `institution`, `created_at`, `arweave_txid`, `image_txid`, `image_hash`.

## Projection rules
- status по умолчанию: `NEW` (если не утверждено иначе);
- type только из текущего словаря;
- labels только согласованные с UI-фильтрами;
- `title/summary/description` в i18n формате `{ et, ru, en }`;
- если summary пустой -> fallback на title;
- фиктивные txid запрещены.

## Product acceptance
- BoardPage/IssuePage не требуют изменений;
- issueService потребляет новый поток как текущий;
- расширения остаются optional и backward-compatible.

## CTO implementation notes
- выделить projection-layer как отдельный модуль;
- версионировать projection policy;
- внедрить contract tests на shape/enum/i18n.
