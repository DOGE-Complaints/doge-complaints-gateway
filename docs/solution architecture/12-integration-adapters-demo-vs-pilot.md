# 12. Integration Adapters: Demo vs Pilot

## Goal
Сразу заложить pilot-ready интеграционные интерфейсы, не включая blockchain runtime в demo.

## Adapter set
- `StorageAdapter` (Supabase/JSON object storage).
- `GeoResolverAdapter`.
- `EmbeddingAdapter`.
- `WalletPushAdapter` (stub in demo).
- `SignRequestAdapter` (in-memory/db stub in demo).
- `TxBroadcasterAdapter` (disabled in demo).

## Demo mode
- wallet flow emulated through stub sender + sign request store.
- no real tx broadcast.
- no on-chain status writes.

## Pilot mode (feature-flag enabled)
- prepare/sign/callback lifecycle active;
- tx broadcast and tx_hash persistence;
- evidence snapshot includes publish references.

## Reference pattern alignment
Используются паттерны из `node`:
- `PrepareResolveService` (domain orchestration).
- `UploadService` (infra state flow).
- `PayloadCache`, `SignRequestStore`, `StubPushSender` abstraction.

## Post-demo (не обязательный scope demo)

Продуктовые сценарии **story-level токенизации** и уведомлений авторам используют те же адаптерные границы, но описаны отдельно с дисклеймером: `docs/requirements/21-post-demo-story-tokenization-and-contributor-notifications.md`, эпик EPIC-M2-12.
