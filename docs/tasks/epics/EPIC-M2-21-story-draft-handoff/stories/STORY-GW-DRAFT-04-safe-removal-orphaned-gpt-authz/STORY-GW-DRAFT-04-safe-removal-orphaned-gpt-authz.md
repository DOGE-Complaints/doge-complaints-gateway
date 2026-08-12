# STORY-GW-DRAFT-04 — Безопасное удаление осиротевшего кода gpt-submit-authz

## Meta
- **Key:** `STORY-GW-DRAFT-04`
- **Parent Epic:** [`../../../EPIC-M2-21-story-draft-handoff.md`](../../../EPIC-M2-21-story-draft-handoff.md)
- **Type:** implement (refactor/removal, change-propagation)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED (гигиена кода: против анти-паттерна «Legacy Accumulation»)
- **source:** [`../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md`](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md)
- **Decision Ref:** backlog file above; [`interview-story-draft-handoff-2026-07-03`](../../../../backlog-stories/story-draft-handoff/interview-story-draft-handoff-2026-07-03.md) (**D-DRAFT-4, D-DRAFT-6** + §Инвентарь)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000046-20260703-gw-draft-04-safe-removal-orphaned-gpt-authz.yaml`](../../../../gateway-active-packages/pkg-000046-20260703-gw-draft-04-safe-removal-orphaned-gpt-authz.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **7** тасков T01–T07
- **Зависит от:** [GW-DRAFT-01](../STORY-GW-DRAFT-01-story-draft-stash/STORY-GW-DRAFT-01-story-draft-stash.md), [GW-DRAFT-02](../STORY-GW-DRAFT-02-browser-submit-verification-gate/STORY-GW-DRAFT-02-browser-submit-verification-gate.md) (новая модель уже стоит и зелёная), [GW-DRAFT-03](../STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon/STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon.md) (канон помечен)
- **Парная:** [GW-DRAFT-03](../STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon/STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon.md) (та — docs, эта — код)

## Зачем простыми словами
После разворота на «браузер сабмитит» часть кода `gpt-submit-authz` (OAuth-introspection именно **токена GPT** на `/intake/stories`) больше не используется. Оставлять мёртвый код — плодить хвосты старых решений. Нужно **аккуратно удалить только осиротевшее**, не задев переиспользуемое (гейт, verify, авторство) и не сломав тесты/деплой. **Историю (аудиты/pkg) не трогаем** (D-DRAFT-6).

## Что наблюдаю сейчас (verified по коду — инвентарь 2026-07-03)
| Компонент | Путь | Действие |
|-----------|------|----------|
| `authoritative_submitter.py` | [src/core/identity/](../../../../../../src/core/identity/authoritative_submitter.py) | ✅ **KEEP** (реюз GW-DRAFT-02) |
| `verification_gate.py`, `verify_url.py`, `VerificationRequiredError` | src/core/identity/, api/envelope.py | ✅ **KEEP** (реюз браузер-гейт) |
| `IntrospectionResult` (value-object) | [introspection_client.py:16-19](../../../../../../src/core/identity/introspection_client.py#L16) | ⚠️ **REFACTOR** — импортируется `verification_gate.py:5` + `authoritative_submitter.py:7`; вынести в нейтральный модуль (напр. `identity/introspection_result.py`), НЕ удалять |
| `IdentityIntrospectionClient` + `build_identity_introspection_from_config` | introspection_client.py, [dependencies.py:16,90](../../../../../../src/core/api/dependencies.py#L16) | ❌ **REMOVE** (OAuth-introspection токена GPT не нужна; браузер → `/me`) |
| env `IDENTITY_INTROSPECT_URL` / `IDENTITY_SERVICE_TOKEN` | [schema.py:130,139](../../../../../../src/core/config/schema.py#L130) | ❌ **REMOVE** (замена `IDENTITY_BASE_URL` для `/me`, GW-DRAFT-02) |
| `require_user_token` (OAuth-introspect на входящем) | [asgi_app.py:298](../../../../../../src/core/api/asgi_app.py#L298) | ❌ **REMOVE**/переработать |
| `_PUBLIC_CONTENT_WRITE_DEPS` на `/intake/stories` **и** `/tallinn/issues` | [asgi_app.py:459,475](../../../../../../src/core/api/asgi_app.py#L459) | ⚠️ **DECIDE** (change-propagation): чем заменяется user-слой на обоих роутах |

**Change-propagation (analysis.mdc §2) — ВСЕ затронутые:**
- `conftest.py` авто-инъект GAUTH-заголовков + монипатч `IdentityIntrospectionClient.introspect` (для intake-тестов) — **обновить/убрать** вместе с клиентом.
- Тесты `test_gw_gauth_02_*`, `test_gw_gauth_03_*` (introspection-контракт) — пересмотреть (что осталось валидным: gate/author — сохранить; OAuth-introspect-специфику — удалить).
- Загрузчик `simulation_runner.py` / seed-доки (`X-User-Token`/`GATEWAY_USER_TOKEN`) — привести к новой модели.
- `/tallinn/issues` (ручное создание issue) — решить, остаётся ли под user-слоем или только сервисный.

**P1 operator default (T01):** `/intake/stories` + `/tallinn/issues` → `[Depends(require_public_content_service_auth)]` only; OAuth `require_user_token` снимается полностью.

## Требование / целевое состояние (D-DRAFT-4/6)
- Удалить **только осиротевший живой код** (таблица «REMOVE» выше) так, что:
  - переиспользуемое (`verification_gate`, `verify_url`, `authoritative_submitter`, `IntrospectionResult`) продолжает работать (GW-DRAFT-02 зелёный);
  - тест-суит зелёный **после** удаления (не «сломали и удалили тесты»);
  - деплой-конфиг/env консистентны (нет висящих `IDENTITY_INTROSPECT_URL` без потребителя).
- **История НЕ трогается** (D-DRAFT-6): аудиты `docs/analysis/audit-gw-gauth-*`, `pkg-000039..042`, run-summary — **сохранить**; backlog `gpt-submit-authz/*` — только пометки superseded (в GW-DRAFT-03).

## Out of scope
- **НЕ удалять историю** (аудиты/pkg/run-summary) — D-DRAFT-6.
- **НЕ трогать** переиспользуемое (KEEP-таблица).
- Кросс-репо канон (04-security) — не здесь (GW-DRAFT-03 / identity-задача).

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-gw-draft-04-t01-change-propagation-audit`](./task-gw-draft-04-t01-change-propagation-audit/README.md) | pkg-000046 |
| 2 | [`task-gw-draft-04-t02-introspection-result-module-extract`](./task-gw-draft-04-t02-introspection-result-module-extract/README.md) | pkg-000046 |
| 3 | [`task-gw-draft-04-t03-remove-oauth-introspection-client-and-env`](./task-gw-draft-04-t03-remove-oauth-introspection-client-and-env/README.md) | pkg-000046 |
| 4 | [`task-gw-draft-04-t04-remove-require-user-token-route-deps`](./task-gw-draft-04-t04-remove-require-user-token-route-deps/README.md) | pkg-000046 |
| 5 | [`task-gw-draft-04-t05-gauth-contract-tests-and-conftest-cleanup`](./task-gw-draft-04-t05-gauth-contract-tests-and-conftest-cleanup/README.md) | pkg-000046 |
| 6 | [`task-gw-draft-04-t06-simulation-runner-and-seed-docs-alignment`](./task-gw-draft-04-t06-simulation-runner-and-seed-docs-alignment/README.md) | pkg-000046 |
| 7 | [`task-gw-draft-04-t07-story-acceptance-gate`](./task-gw-draft-04-t07-story-acceptance-gate/README.md) | pkg-000046 |
| 8 | [`task-gw-draft-04-t08-architecture-intake-service-only-doc-sync`](./task-gw-draft-04-t08-architecture-intake-service-only-doc-sync/README.md) | audit override (not in pkg-000046) |
| 9 | [`task-gw-draft-04-t09-legacy-intake-trusted-service-channel-security-ssot`](./task-gw-draft-04-t09-legacy-intake-trusted-service-channel-security-ssot/README.md) | audit override (not in pkg-000046) |

## Acceptance Criteria
- [x] Осиротевший код (OAuth-introspection-клиент, env `IDENTITY_INTROSPECT_URL/SERVICE_TOKEN`, GPT-`require_user_token`-путь) удалён; `grep` остаточных потребителей = 0.
- [x] Переиспользуемое (`verification_gate`, `verify_url`, `authoritative_submitter`, `IntrospectionResult`) работает; GW-DRAFT-02 зелёный.
- [x] Тест-суит **зелёный после** удаления (не за счёт удаления живых тестов).
- [x] `/intake/stories` и `/tallinn/issues` — user-слой явно разрешён (переключён/снят) по T01, без «висящих» зависимостей.
- [x] История не тронута: `docs/analysis/audit-gw-gauth-*`, `pkg-000039..042`, run-summary — на месте (D-DRAFT-6).
- [x] `simulation_runner.py`/seed-доки согласованы с новой моделью.

## Швы
[`src/core/identity/`](../../../../../../src/core/identity/) (introspection_client → рефактор/удаление, новый introspection_result), [`api/asgi_app.py`](../../../../../../src/core/api/asgi_app.py) (deps/роуты), [`api/dependencies.py`](../../../../../../src/core/api/dependencies.py), [`config/schema.py`](../../../../../../src/core/config/schema.py) (env), [`tests/conftest.py`](../../../../../../tests/conftest.py) + `test_gw_gauth_0[23]_*`, [`tests/simulation_runner.py`](../../../../../../tests/simulation_runner.py), seed-доки.

## Границы
- **НЕ удалять историю** (аудиты/pkg/run-summary) — D-DRAFT-6.
- **НЕ трогать** переиспользуемое (KEEP-таблица).
- Кросс-репо канон (04-security) — не здесь (GW-DRAFT-03 / identity-задача).
