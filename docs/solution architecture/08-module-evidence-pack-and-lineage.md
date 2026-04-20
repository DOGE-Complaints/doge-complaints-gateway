# 08. Module: Evidence Pack & Lineage

## Responsibilities
- Формировать evidence pack отдельно от публичной issue card.
- Хранить полную связность `story <-> cluster <-> issue`.
- Поддерживать snapshot для будущей tokenization flow.

## Evidence pack structure (logical)
- issue reference
- cluster snapshot (lens/version/time)
- story references list
- supporting artifacts metadata
- privacy classification
- tokenization_readiness marker

## Access model
- public view: minimal evidence summary;
- internal view: expanded evidence;
- export view: pilot bundle (for future Web3/external).

## Lineage guarantees
- 100% reversible path from issue to source stories.
- immutable linkage records.
- audit trail of split/merge/reframe decisions.
