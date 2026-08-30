-- STORY-GW-SSR-24: persist StoryGeoSnapshot address depth
-- Omit-probe like geo_admin_*; do not add these to required_columns_ready.

alter table public.stories
    add column if not exists geo_street text,
    add column if not exists geo_house text,
    add column if not exists geo_house_range text,
    add column if not exists geo_houses_json text,
    add column if not exists geo_address_line text;

comment on column public.stories.geo_street is
  'GW-SSR-24: client/pack street; civic geo_filter still uses geo_admin_*';
comment on column public.stories.geo_house is
  'GW-SSR-24: single house; XOR house_range / houses in intake';
comment on column public.stories.geo_house_range is
  'GW-SSR-24: house range string';
comment on column public.stories.geo_houses_json is
  'GW-SSR-24: JSON array of house ids';
comment on column public.stories.geo_address_line is
  'GW-SSR-24: display address line';
