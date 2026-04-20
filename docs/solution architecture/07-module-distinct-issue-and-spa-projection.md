# 07. Module: Distinct Issue & SPA Projection

## Responsibilities
- Перевод issue-ready кластера в distinct issue.
- Поддержка issue-candidate lifecycle.
- Генерация SPA-compatible projection без breaking changes.

## Promotion gates
- semantic cohesion threshold;
- repeatability threshold;
- geo/systemic determinacy;
- desired-state completeness;
- operator review acceptance.

## SPA projection rules
- Required: `id,status,type,labels,title,summary,description`.
- Optional: `institution,created_at,arweave_txid,image_txid,image_hash`.
- i18n object mandatory for text: `{et,ru,en}`.
- fallback: `summary <- title`.
- no fake txid.

## Projection architecture
- Projection Engine isolated from cluster engine.
- Policy versioning for reproducibility.
- Contract tests against current SPA consumers.
