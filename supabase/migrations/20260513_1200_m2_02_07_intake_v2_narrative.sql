-- REQ-33 / STORY-M2-02-07: multilingual narrative v2 columns on stories
alter table public.stories
  add column if not exists narrative_title_json jsonb,
  add column if not exists narrative_description_json jsonb,
  add column if not exists narrative_session_language text;

comment on column public.stories.narrative_title_json is
  'REQ-33 v2: {et,ru,en} title dict';
comment on column public.stories.narrative_description_json is
  'REQ-33 v2: {et,ru,en} description dict';
comment on column public.stories.narrative_session_language is
  'REQ-33 v2: primary session language (et|ru|en)';
