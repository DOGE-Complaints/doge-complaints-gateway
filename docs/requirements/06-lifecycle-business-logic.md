# 06. Бизнес-логика жизненного цикла

## Этапы lifecycle
1. **Story Intake** — приём narrative package без forced collapse в issue.
2. **Normalization** — приведение смысла к операционной читаемости.
3. **Profile Enrichment** — наполнение сигналами для многомерного чтения.
4. **Cluster Inclusion** — участие истории в разных cluster views.
5. **Cluster Maturation** — оценка зрелости до issue-candidate.
6. **Issue Projection** — формирование SPA-совместимого shape.
7. **Evidence Pack Build** — выделенная доказательная сборка.

## State machine (продуктовая)
`draft_story -> accepted_story -> cluster_eligible -> issue_candidate -> projected_issue`

## Контрольные точки переходов
- определены пороги полноты narrative и profile;
- определены пороги cluster cohesion;
- определены условия перехода в issue_candidate;
- есть контроль ложных merge/split.

## SLA/операционный контур
- intake и сохранение: near-real-time;
- кластеризация: периодическая + on-demand;
- projection: триггер от зрелости или операторского review.

## Риски
- преждевременная промоция в issue;
- чрезмерная задержка (кластер “вечно зрелый”);
- дрейф критериев зрелости между командами.
