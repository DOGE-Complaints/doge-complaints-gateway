-- STORY-GW-SSR-27: persist StoryGeoSnapshot.detail_level (precision index)
-- Omit-probe like SSR-24 geo depth; do not add to required_columns_ready.

alter table public.stories
    add column if not exists geo_detail_level text;

comment on column public.stories.geo_detail_level is
  'GW-SSR-27: precision index (region|settlement|district|street|house|house_range|coordinates)';
