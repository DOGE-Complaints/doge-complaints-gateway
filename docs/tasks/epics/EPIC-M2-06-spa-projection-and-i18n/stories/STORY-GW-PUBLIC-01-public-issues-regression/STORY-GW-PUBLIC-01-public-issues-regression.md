# STORY-GW-PUBLIC-01 — Регресс-гарантия публичности issues (gateway)

## Meta
- **Key:** `STORY-GW-PUBLIC-01`
- **Parent Epic:** [`../../../EPIC-M2-06-spa-projection-and-i18n.md`](../../../EPIC-M2-06-spa-projection-and-i18n.md)
- **Type:** Technical Story
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** P2 gate
- **Тип:** test (regression gate)
- **source:** [`../../../../backlog-stories/issues-read-contract/STORY-GW-PUBLIC-01-public-issues-regression.md`](../../../../backlog-stories/issues-read-contract/STORY-GW-PUBLIC-01-public-issues-regression.md)
- **Закрывает:** M-5 — зафиксировать подтверждённое: read без auth; не дать случайно закрыть при добавлении auth на write
- **Источник:** [`mvp-integration-plan-2026-07-02.md` M-5](../../../../../../../doge-identity-service/docs/analysis/mvp-integration-plan-2026-07-02.md)
- **Decision Ref:** backlog file above; M-5 from mvp-integration-plan
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000048-20260710-gw-public-01-public-issues-regression.yaml`](../../../../gateway-active-packages/pkg-000048-20260710-gw-public-01-public-issues-regression.yaml) — **5** тасков T01–T05
- **Зависит от:** —
- **Разблокирует:** безопасные изменения auth на story-drafts / tallinn write paths

## Зачем простыми словами
Просмотр жалоб без логина — ключевое требование, и сейчас оно выполнено. Пока мы навешиваем auth на сабмит-роуты (M-3), легко случайно закрыть и read-роуты. Нужен тест, который **падает**, если на публичные issue-роуты вдруг повесили авторизацию.

## Что наблюдаю сейчас (verified по коду)

| Route | Auth | Ref |
|-------|------|-----|
| `GET /tallinn/issues` | **нет** deps | [`asgi_app.py:429`](../../../../../../../src/core/api/asgi_app.py) |
| `GET /tallinn/issues/{issue_id}` | **нет** deps | [`asgi_app.py:471`](../../../../../../../src/core/api/asgi_app.py) |
| `POST /tallinn/issues` | service auth | [`asgi_app.py:485`](../../../../../../../src/core/api/asgi_app.py) |
| `POST /story-drafts` | service deps | [`asgi_app.py:521`](../../../../../../../src/core/api/asgi_app.py) |
| `POST /story-drafts/{id}/submit` | browser auth | [`asgi_app.py:552`](../../../../../../../src/core/api/asgi_app.py) |

- Partial coverage: [`test_http_transport_smoke.py`](../../../../../../../tests/test_http_transport_smoke.py) проверяет `/health`, `/ready` — **не** `/tallinn/issues`.
- Legacy `POST /intake/stories` ([`:501`](../../../../../../../src/core/api/asgi_app.py)) — к удалению [GW-DRAFT-06](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md); contrast-тесты на **story-drafts**, не intake.

## Требование / целевое состояние

- Offline contract test: публичные GET issue routes без заголовков → 200 (не 401/403).
- Contrast: write routes без сервис-токена → 401 (не «всё открыто»).
- Тест устойчив к story-draft handoff (не ломается при M-3).

## Граница

- In scope: `GET /tallinn/issues`, `GET /tallinn/issues/{id}`.
- Out of scope: hosted E2E; auth на write paths (уже покрыто другими contract tests).

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-public-01-t01-get-tallinn-issues-list-without-auth-200`](./task-gw-public-01-t01-get-tallinn-issues-list-without-auth-200/README.md) | pkg-000048 |
| 2 | [`task-gw-public-01-t02-get-tallinn-issue-by-id-without-auth-not-401`](./task-gw-public-01-t02-get-tallinn-issue-by-id-without-auth-not-401/README.md) | pkg-000048 |
| 3 | [`task-gw-public-01-t03-post-story-drafts-without-service-token-401`](./task-gw-public-01-t03-post-story-drafts-without-service-token-401/README.md) | pkg-000048 |
| 4 | [`task-gw-public-01-t04-post-tallinn-issues-without-service-token-offline-green`](./task-gw-public-01-t04-post-tallinn-issues-without-service-token-offline-green/README.md) | pkg-000048 |
| 5 | [`task-gw-public-01-t05-story-acceptance-gate`](./task-gw-public-01-t05-story-acceptance-gate/README.md) | pkg-000048 |
| 6 | [`task-gw-public-01-t06-restore-testclient-request-after-gauth-auto-headers`](./task-gw-public-01-t06-restore-testclient-request-after-gauth-auto-headers/README.md) | audit override (`run_mode=gw_public_01_audit_followup`) |

## Audit follow-up (2026-07-10)

- **Audit:** [`audit-gw-public-01-public-issues-regression-2026-07-10.md`](../../../../../../analysis/audit-gw-public-01-public-issues-regression-2026-07-10.md)
- **G1** → T06 **Done** 2026-07-11 (conftest `TestClient.request` session restore)
- **R1/R2/R3** doc drift → `activation: none` (вне P5/P6 по команде оператора)
- **Не менять** [`pkg-000048`](../../../../gateway-active-packages/pkg-000048-20260710-gw-public-01-public-issues-regression.yaml)

## Подзадачи

| ID | Задача |
|----|--------|
| **T01** | Тест: `GET /tallinn/issues` без auth → 200 |
| **T02** | Тест: `GET /tallinn/issues/{id}` без auth → 200/404, не 401/403 |
| **T03** | Contrast: `POST /story-drafts` без `SERVICE_API_TOKEN` → 401 |
| **T04** | Contrast: `POST /tallinn/issues` без service token → 401; offline suite green |

## Acceptance Criteria

- [x] T01–T02: read routes публичны
- [x] T03–T04: write routes закрыты без service auth
- [x] Тесты в offline-сюите (без сети), зелёные

## Открытые вопросы

- Нужен ли отдельный тест на `GET /story-drafts/{id}` (требует browser auth)? → **нет**, вне M-5 scope.

## Швы

- [`asgi_app.py:429,471,485,521`](../../../../../../../src/core/api/asgi_app.py)
- Тесты — рядом с [`test_http_transport_smoke.py`](../../../../../../../tests/test_http_transport_smoke.py) или dedicated `test_gw_public_01_*.py`
