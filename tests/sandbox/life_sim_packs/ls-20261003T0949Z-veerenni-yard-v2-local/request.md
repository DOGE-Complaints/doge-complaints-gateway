# life-sim pack request

- utc: `2026-10-03T09:49:42Z`
- pack_id: `ls-20261003T0949Z-veerenni-yard-v2-local`
- profile_id: `local` (local-five: `scripts/shell/local-five-serve-and-health.sh`)
- intent: локальный прогон демо-ноды Уус-Веэрэнни; Full scale; v2 stories richness
- source_users: copy from `ls-20261002T0906Z-veerenni-v2-rich/users.json` (on execute materialize)
- source_params: same scale + story_foci as `ls-20261002T0906Z-veerenni-v2-rich/params.json`
- stories: **regenerate** v2 with same params (not 6-key; not copy stories.json)
- pipeline: cluster_force / threads_seed / spa_verify = on
- wipe content: REQ11-06 Present (`make life-sim-wipe-node-content`)
- provision Auth: `wipe-fixture-users` then create from copied users.json; keep admin `zeya.meysapuu@gmail.com` (outside fixture email set)
- richness target: **Full / Pass** (v2 Narrative-aligned), not Partial sample

## Interview locks (2026-10-03)

1. `node_social_direction` — agreed (see `params.json`)
2. Stories — regenerate with same params
3. Scale — do not narrow (200 / 8.5 / 60·30·10 / calendar 2026)
4. Auth — wipe-fixture-users; new users from copied v2 users.json

## Status

- Interview: **closed**
- Materialize users/stories/meta + wipe/load: **waiting for operator execute**
