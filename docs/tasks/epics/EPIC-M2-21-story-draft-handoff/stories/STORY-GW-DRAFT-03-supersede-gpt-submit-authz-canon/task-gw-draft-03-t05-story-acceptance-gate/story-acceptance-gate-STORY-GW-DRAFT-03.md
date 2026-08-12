# Story acceptance gate — STORY-GW-DRAFT-03

- **Story:** Пересмотр канона (supersede docs) + identity-задача
- **Package:** `pkg-000045-20260703-gw-draft-03-supersede-gpt-submit-authz-canon.yaml`
- **Result:** PASS
- **Date:** 2026-07-03

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| `gpt-submit-authz/INDEX.md` явно помечает superseded-часть; читатель не примет её за актуальный флоу | PASS | T01 — superseded block + table; historical context strikethrough |
| Переиспользуемое (GAUTH-04, verification_required-канон) явно связано с `story-draft-handoff/` | PASS | T01 — GAUTH-03/04 «reused» rows → GW-DRAFT-02 |
| Gateway runtime-docs отражают browser-submit как as-built; нет gateway-док с «GPT сам сабмитит» без пометки | PASS | T02, T04 — architecture §4.1; legacy labels in seed/simulation manuals |
| Заведена identity-side задача на правку `04-security.md`/`09-gateway-expectations.md`; gateway не редактирует чужой канон сам | PASS | T03 — STORY-IDS-DOC-DRAFT-05 + §4.2 pointer; identity runtime untouched |
| История (аудиты/pkg-000039..042) **не** удалена (D-DRAFT-6) | PASS | T01 explicit preserve; T04 exclude list |

## Commands (live verification 2026-07-03)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
rg -i 'superseded' doge-complaints-gateway/docs/tasks/backlog-stories/gpt-submit-authz/INDEX.md
rg 'story-drafts' doge-complaints-gateway/docs/runtime-docs/architecture-and-layers-as-is.md
test -f doge-identity-service/docs/tasks/backlog-stories/story-draft-handoff/STORY-IDS-DOC-DRAFT-05-browser-submit-security-canon-sync.md
```

**Live run:** verify ok 5 paths; date-check ok (2026-07-03)

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
