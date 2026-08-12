# curl verify — GET /tallinn/issues (GW-RC-06 T04)

**Date:** 2026-06-20  
**Gateway:** `http://127.0.0.1:8000` (`DB_BACKEND=supabase`, `make serve`)

## Command

```bash
curl -s http://127.0.0.1:8000/tallinn/issues
```

## Results

| Check | Result |
|-------|--------|
| HTTP 200 | yes |
| Issues returned | 1 |
| Any `status='promoted'` in response | **no** |
| All statuses board-vocab | **yes** (`PUBLISHED`) |
| Non-empty title on displayed card | **yes** (`Road light issue` en/et/ru) |
| Board not empty | **yes** (1 valid card) |

Full JSON response: [`tallinn-issues-live-response.json`](./tallinn-issues-live-response.json)

## Board verify

SPA manual screenshot not captured; API evidence satisfies parent AC#3 for hosted read path. Operator may spot-check SPA board separately.
