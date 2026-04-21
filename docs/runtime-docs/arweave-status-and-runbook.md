# Arweave / On-chain Status and Runbook

## Контекст и управленческий вопрос

Ключевой вопрос:  
**какова фактическая готовность chain-интеграции сейчас, и где проходит граница между pilot-ready интерфейсами и реальным on-chain исполнением?**

## As-is (implemented now)

### 1) Что реально реализовано

- Введены adapter interfaces:
  - `WalletPushAdapter`
  - `SignRequestAdapter`
  - `TxBroadcastAdapter`  
  (файл `src/core/adapters/protocols.py`)
- Реализованы deterministic demo/pilot stubs:
  - `DemoWalletPushAdapter`
  - `DemoSignRequestAdapter`
  - `DemoTxBroadcastAdapter`  
  (файл `src/core/adapters/demo.py`)
- Сборка bundle идет через `build_adapter_bundle(config)`:
  - выбирается профиль из `AppConfig.profile`;
  - для `demo` и `pilot` сейчас используются те же stub-классы.  
  (файл `src/core/adapters/registry.py`)

### 2) Поведение, подтвержденное тестами

- `tests/test_adapters_demo_pilot.py` подтверждает:
  - typed bundle;
  - deterministic ID generation;
  - различие deterministic tx_id между demo/pilot профилями;
  - корректность `adapter_runtime_flags`.

### 3) Что отсутствует в current runtime

- Нет real Arweave client/provider.
- Нет реального ключевого контура подписания и безопасного key custody.
- Нет on-chain finality polling/reconciliation.
- Нет production-grade error/retry/compensation flow для цепочки tx lifecycle.

## Архитектурные последствия и ограничения

- Плюс текущего подхода: протоколы и call sites уже стабилизированы, поэтому замена stub на real adapter возможна без массового переписывания application слоя.
- Минус: operational readiness для chain в production отсутствует; текущий контур — это controlled simulation, а не настоящий blockchain path.
- Риск коммуникации: внешние документы могут восприниматься как «уже есть on-chain», если не держать жесткую метку `stub-only`.

## Planned target (runbook)

### 1) Integration building blocks

1. **Secrets and env**
   - chain endpoint configuration,
   - signing key material (через secret manager),
   - timeout/retry policy.
2. **Lifecycle**
   - payload preparation -> sign -> broadcast -> receipt persist -> confirm/finality reconcile.
3. **Security controls**
   - key isolation и least privilege,
   - immutable audit trail по шагам tx lifecycle.
4. **Ops controls**
   - degraded fallback to stubs,
   - incident runbook для broadcast/finality ошибок.

### 2) Suggested implementation points

- Новые реализации: `src/core/adapters/arweave_*.py`
- Расширение resolver logic: `src/core/adapters/registry.py`
- Конфиг расширения: `src/core/config/schema.py`
- Future tests:
  - `tests/test_adapters_arweave_integration.py`
  - `tests/test_adapters_arweave_failure_modes.py`

## Gaps / risks

- До внедрения real adapters любые on-chain KPI/claims остаются непроверяемыми в runtime.
- Pilot profile сегодня не означает наличие blockchain execution; это только профиль feature defaults.
- При быстром внедрении real adapters без ключевой политики возникает высокий security/operational risk.

## Контрольные проверки

- Проверить текущий stub baseline:  
  `python3 -m pytest tests/test_adapters_demo_pilot.py -q`
- Зафиксировать profile flags snapshot при запуске:
  - `adapter_runtime_flags(config)` из `src/core/adapters/registry.py`
