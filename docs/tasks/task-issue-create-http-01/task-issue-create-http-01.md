## Task: implement — HTTP create issue endpoint(s)

### Цель
Добавить HTTP слой для создания issue из runtime pipeline, чтобы ключевой use-case был доступен на API boundary.

### Почему это важно (риск)
Без create issue endpoint демо не отражает главный сценарий продукта, а внутренние сервисы остаются недоступными снаружи.

### Scope
Входит:
- endpoint для create issue (канонический путь согласуется в decision phase);
- orchestration: intake/promotion/projection integration point;
- единый envelope/error контракт.

Не входит:
- полный workflow управления issue (list/search/history UI).

### Факты из кода (Code Facts / SSOT)
1) `src/core/api/asgi_app.py`
- отсутствует `POST` create route для issue.

2) `src/core/promotion/service.py`
- есть `IssuePromotionService` с candidate lifecycle.

3) `src/core/projection/service.py`
- есть `IssueProjectionService.project`, но нет HTTP wiring.

### Gap / Проблема
`GAP-IP-002`: ключевой create issue функционал не экспонирован через API.

### Decision Points
- **PM decision:** выбрать endpoint shape, достаточный для demo narrative.
- **CTO decision:** не смешивать transport и доменную оркестрацию в одном слое.
- **Options:**
  - A: один endpoint с минимальным payload и inline orchestration.
  - B: endpoint с явным application orchestrator/use-case сервисом и строгим response контрактом.
- **Recommendation:** вариант B (лучше для расширения после демо и без layer drift).

### AC/DoD
- [ ] (P0) Добавлен HTTP create issue endpoint.
- [ ] (P0) Endpoint вызывает application orchestration (не прямой ad-hoc маппинг в роуте).
- [ ] (P0) Возвращается стабильный envelope с issue id и статусом.
- [ ] (P1) Добавлены negative tests на invalid payload/contract errors.
- [ ] (P1) Документация runtime API обновлена.

### Где менять код
- `src/core/api/asgi_app.py`
- `src/core/api/handlers.py`
- `src/core/application/` (новый orchestrator при необходимости)
- `tests/` (HTTP create issue tests)
- `docs/runtime-docs/api-reference/openapi.yaml`

### План выполнения (Execution Plan)
1) Согласовать endpoint contract.
2) Реализовать orchestration слой.
3) Подключить endpoint в API.
4) Добавить tests.
5) Синхронизировать runtime docs.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/test_http_transport_smoke.py -q
python3 -m pytest tests/test_http_issue_create_endpoint.py -q
python3 -m pytest tests/test_e2e_intake_create_spa_contract.py -q
```
