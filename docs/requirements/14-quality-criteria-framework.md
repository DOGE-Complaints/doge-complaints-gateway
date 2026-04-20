# 14. Критерии качества модуля

## Продуктовые критерии
- история не теряется на любом этапе;
- кластеры не цементируются слишком рано;
- distinct issues ясные, честные и управляемые;
- каждая карточка имеет прозрачный путь к evidence base;
- дашборд показывает кейсы, а не сырой шум.

## Технические критерии
- contract compatibility с SPA = 100%;
- lineage completeness = 100%;
- projection errors < agreed threshold;
- false merge/split под контролем мониторинга.

## NFR критерии
- explainability для cluster inclusion и issue promotion;
- reproducibility результатов при фиксированной версии правил;
- privacy-min и separation public/internal layers.

## Операционные критерии
- наблюдаемость всех переходов lifecycle;
- деградация в safe mode при сомнительной кластерной зрелости;
- управляемый rollback projection-правил.
