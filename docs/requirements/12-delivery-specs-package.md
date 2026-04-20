# 12. Набор продуктовых спецификаций для реализации

Из canvas должны родиться 6 производственных спецификаций:

## A. Story Intake Spec
- что считается принятой историей;
- минимальный валидный package;
- статусы полноты и readiness;
- правила PII-min.

## B. Story Intelligence Spec
- какие сигналы извлекаются;
- как различаются user/system поля;
- как обновляется профиль без потери оригинала.

## C. Cluster View Spec
- обязательные линзы MVP;
- правила multi-membership;
- метод определения доминирующего смыслового ядра.

## D. Distinct Issue Promotion Spec
- пороговые критерии issue-candidate;
- split/merge/reframe процессы;
- human review checkpoints.

## E. SPA Projection Spec
- mapping в Issue shape;
- словари enum и i18n;
- fallback и contract-tests.

## F. Evidence Pack Spec
- структура evidence;
- правила публичности/внутреннего слоя;
- tokenization-readiness markers.

## Delivery governance
- единый backlog по спецификациям с owner per spec;
- трассировка FR -> Spec -> AC -> test plan;
- change management через ADR и versioning.
