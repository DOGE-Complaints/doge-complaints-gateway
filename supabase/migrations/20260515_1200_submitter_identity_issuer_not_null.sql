-- GAP-33-02: enforce REQ-33 eID gate at DB layer (backfill NULL before NOT NULL).
update public.stories
set submitter_identity_issuer = 'legacy-unknown'
where submitter_identity_issuer is null;

alter table public.stories
    alter column submitter_identity_issuer set not null;
