# 15. Acceptance Criteria: operationalization

## Story AC
- история сохраняется без forced collapse;
- narrative и signal profile отделимы;
- story может повторно участвовать в разных выборках.

## Cluster AC
- один corpus читается разными cluster views;
- одна история может быть в нескольких кластерах;
- analytics cluster и issue-ready cluster различаются явно.

## Distinct Issue AC
- из зрелого кластера строится distinct issue;
- для issue есть обратимая связь к первичным stories;
- issue отображается в существующем SPA контракте.

## SPA AC
- выдаются обязательные поля контракта;
- default status = NEW;
- i18n `{ et, ru, en }` на title/summary/description;
- фиктивных txid нет.

## Product AC
- модуль снижает дубликаты, не ломая evidence базу;
- distinct issues формируются как collective cases;
- есть рабочий мост “жительские истории -> управляемые кейсы”.

## CTO validation matrix
- AC покрываются contract/integration/review tests;
- для каждого AC есть owner, наблюдаемая метрика и путь эскалации.
