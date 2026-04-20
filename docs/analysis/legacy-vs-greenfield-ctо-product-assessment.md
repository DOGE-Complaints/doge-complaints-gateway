# DOGE Complaints Gateway: критический анализ "оставлять legacy vs делать с нуля"

## Контекст решения

Цель: объективно оценить, что рациональнее для Module 2 (Story Intelligence + подготовка к токенизации):
- эволюционировать текущий `doge-complaints-gateway` (Python/Flask legacy),
- переписать с нуля,
- или выбрать гибридную стратегию.

В анализе использован референсный проект `node` в workspace как эталон архитектурных паттернов и операционных конфигов (DI, validation system, API middleware/security, test orchestration, upload/sign/callback flow).

---

## Executive Verdict

**Рекомендация: hybrid greenfield core (архитектурный rewrite ядра) + selective reuse артефактов legacy.**

Почему:
- текущий код gateway слишком хрупок как основа Module 2 и токенизационного контура;
- “дешёвая доработка” legacy даст быстрый short-term результат, но закрепит системный техдолг;
- полный rewrite “в вакууме” рискован по срокам и доменному дрейфу;
- оптимум: новый каркас по паттернам `node`, с точечным переносом только того, что действительно ценно (доменная семантика, часть SQL/словарей, часть интеграционных идей).

---

## Фактическая база: что есть сейчас

## Текущее состояние `doge-complaints-gateway`

### Сильные стороны (что реально можно сохранить)
- уже есть базовая доменная модель жалоб (complaints/categories/events/time/embeddings);
- есть рабочая цепочка внешних интеграций (Supabase, geocoding, Pinata, Dogeparty);
- есть зачатки story-like данных (narrative + metadata + relation tables);
- есть Supabase Edge Functions scaffold (`vectorize`, `summary`).

### Критические слабости (блокеры для масштабируемого Module 2)
- монолитный sync endpoint-оркестратор (`submit_complaint`) с side effects в request path;
- отсутствие тестовой системы (фактически нет `tests`);
- отсутствует архитектурная декомпозиция слоёв/ролей;
- service-role доступ к Supabase в пользовательском потоке;
- слабая security hygiene (debug mode, секреты/токены в логах, неструктурированный error handling);
- несоответствия между `db.sql`, runtime-кодом и контрактами payload.

---

## Что даёт референсный `node` проект (как архитектурный донор)

## Подтверждённые паттерны, которые стоит заимствовать

1. **Чёткая многослойная архитектура**
- Presentation/API -> Application -> Domain orchestration -> Infrastructure.

2. **DI-first дизайн**
- отдельные dependency providers (`dependencies.py`, `api/dependencies.py`);
- `ServiceFactory` как единая точка сборки графа зависимостей;
- заменяемость зависимостей для тестов и режимов запуска.

3. **Orchestration services + state transitions**
- registry/orchestrator паттерн (пример `ActivityRegistryService`);
- явные lifecycle transitions и проверка допустимости переходов.

4. **Разделение доменной и инфраструктурной логики в upload/tokenization flow**
- `PrepareResolveService` (доменный фасад);
- `UploadService` (инфраструктурная state machine таблицы uploads);
- callback-driven подтверждение и последующий контрактный шаг.

5. **Системный validation layer**
- унифицированные `ValidationResult`/validators/factory;
- валидация согласована между API, converter и service слоями.

6. **Security & operations baseline**
- middleware chain (HMAC/Bearer, trusted host, CORS);
- централизованная `APIConfig`/env governance;
- health endpoints, логирование, явные режимы запуска.

7. **Зрелая тестовая культура**
- unit/integration/e2e stratification;
- централизованные fixtures/mocks;
- orchestrated full-flow e2e (подписной/публикационный цикл).

---

## Критерии оценки (Product + CTO)

Оценка 1-10, где 10 = максимально благоприятно.  
Рассмотрены 3 стратегии:
- **A**: Continue legacy (минимальная эволюция текущего кода),
- **B**: Full rewrite now,
- **C**: Hybrid greenfield core + selective reuse.

| Критерий | Вес | A Legacy | B Full Rewrite | C Hybrid |
|---|---:|---:|---:|---:|
| Скорость time-to-first-MVP | 15% | 8 | 4 | 7 |
| Долгосрочная maintainability | 20% | 3 | 9 | 9 |
| Security posture | 15% | 3 | 8 | 8 |
| Тестопригодность/качество | 15% | 2 | 9 | 8 |
| Совместимость с Module 2 требованиями | 15% | 4 | 9 | 9 |
| Готовность к tokenization flow | 10% | 4 | 9 | 9 |
| Риск delivery и миграции | 10% | 6 | 4 | 7 |
| **Итог (взвешенно)** | **100%** | **4.3** | **7.5** | **8.2** |

**Вывод:** Hybrid стратегия доминирует по суммарной ценности и контролю рисков.

---

## Что оставить из legacy, а что не переносить

## Keep (сохранить/переиспользовать)
- доменную семантику сущностей и связей (complaint/story categories/events/time/evidence lineage);
- часть SQL-модели как input в новую migration-first схему;
- интеграционные знания по Supabase/Pinata/Dogeparty;
- часть утилитных идей (геокодинг, словари признаков, embedding-концепт).

## Rewrite (переписать обязательно)
- API слой и orchestration (новый lifecycle-driven дизайн);
- security слой (auth/authz, secret handling, logging policy);
- data access слой (repository + transaction boundaries + idempotency);
- validation и contract layer (единая схема запросов/ответов);
- state machine для cluster -> issue-candidate -> issue projection;
- тестовая пирамида (unit/integration/e2e + contract tests).

## Drop (не переносить)
- текущий sync “all-in-one” endpoint-паттерн;
- неструктурированное print-логирование;
- ad-hoc JWT генерацию без нормального trust boundary;
- несогласованные payload/sql enum практики;
- helper-скрипты, печатающие секреты.

---

## Риски двух крайностей

## Если “оставить почти всё”
- высокая вероятность повторных архитектурных переломов через 1-2 спринта;
- затяжной security remediation вместо feature delivery;
- рост стоимости каждой новой функции (кластеры, reviewability, tokenization readiness).

## Если “переписать всё сразу”
- риск потери доменных нюансов и контекстной экспертизы;
- задержка value delivery для текущего продукта;
- риск scope explosion и architecture gold-plating.

---

## Рекомендуемая стратегия реализации (без кодинга, как decision blueprint)

## Phase 0: Architectural baseline (короткая)
- зафиксировать target architecture по паттернам `node`:
  - API layer
  - application orchestrators
  - domain models/state machine
  - infra adapters
- зафиксировать ADR по ключевым решениям.

## Phase 1: New core skeleton
- поднять новый каркас модулей и DI/ServiceFactory;
- внедрить unified validation + error model;
- внедрить config governance и security middleware.

## Phase 2: Data & workflow migration
- мигрировать legacy данные в новую schema/migrations дисциплину;
- перенести story intake и profile enrichment в новый pipeline;
- реализовать dynamic cluster views и issue promotion gates.

## Phase 3: Tokenization-ready bridge
- внедрить prepare/sign/callback state flow по шаблону upload orchestration;
- разделить публичную issue projection и внутренний evidence layer.

## Phase 4: Decommission legacy path
- dual-run период и сравнение результатов;
- выключение legacy endpoints после acceptance.

---

## Критерии “go/no-go” для окончательного решения

Перейти на hybrid greenfield окончательно, если одновременно верно:
- подтверждён roadmap Module 2 с кластеризацией и issue promotion;
- требуется evidence lineage и tokenization preparation в MVP+;
- команда готова инвестировать в тестовую и security дисциплину.

Оставаться на legacy только как временный мост имеет смысл, если:
- горизонт продукта <= 1-2 месяца;
- нет планов на динамические кластеры/evidence governance;
- нет регуляторных/репутационных требований к security и traceability.

Для вашего сценария (Module 2 + дальнейшая токенизация) эти условия **не выполняются**.

---

## Финальное решение

**Не стоит продолжать текущий gateway как главную архитектурную базу.**  
Рационально:
1. строить новый core по проверенным паттернам из `node`,
2. переносить только действительно ценные доменные артефакты из legacy,
3. использовать staged migration вместо big-bang cutover.

Это даёт лучший баланс: скорость выхода, качество, безопасность и устойчивость под будущую токенизацию.
