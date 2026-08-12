# Итог пакета issues-read-contract: почему доска всё ещё пустая (status vocabulary)

**Дата:** 2026-06-20
**Метод:** `.cursor/rules/analysis.mdc` — выводы по фактическому коду, пути указаны.
**Статус пакета:** RC-01..04 — implemented & verified, **но исходная цель (наполненная доска) НЕ достигнута** из-за дефекта вне scope пакета.

## Связанные отчёты (co-located)
- **Новое расследование (Jun-20, перенесено сюда):** [`investigation-empty-board-status-vocabulary-2026-06-20.md`](./investigation-empty-board-status-vocabulary-2026-06-20.md)
- **Исходный баг-репорт FE (Jun-19, start doc, остаётся в spa-app):** [`spa-app/.../report-empty-dashboard-gfl-driven-2026-06-19.md`](../../../../../spa-app/docs/analysis/report-empty-dashboard-gfl-driven-2026-06-19.md)
- Аудиты RC-01..04: [`audit-gw-rc-01`](../../../analysis/audit-gw-rc-01-read-path-column-merge-2026-06-19.md) · [`rc-02`](../../../analysis/audit-gw-rc-02-type-canonical-on-read-2026-06-19.md) · [`rc-03`](../../../analysis/audit-gw-rc-03-contract-guarantee-legacy-data-2026-06-19.md) · [`rc-04`](../../../analysis/audit-gw-rc-04-columnar-model-migration-2026-06-20.md)

---

## 1. Что произошло (одним абзацем)

Пакет чинил то, что было видно в отчёте Jun-19: «у issue в API **нет** `id`/`status`». RC-01 это починил (merge колонок). Но как только `status` стал **виден**, выяснилось, что в нём лежит **невалидное для доски значение `promoted`** — а это уже другой дефект, которого в scope пакета не было. Доска по-прежнему пустая: SPA раскладывает карточки только по `NEW|IN_REVIEW|PUBLISHED`, а API отдаёт `promoted`.

## 2. Корневая причина (verified по коду)

В gateway **два разных enum статуса**, и они смешались:
- `DOGEIssueStatus` = `NEW/IN_REVIEW/PUBLISHED` — контракт **доски/проекции** ([enums.py:6-11](../../../../src/core/projection/enums.py#L6-L11)).
- `IssueCandidateStatus` = `draft/ready_for_review/in_review/**promoted**/rejected` — **промоушн-пайплайн** ([promotion/types.py:8-13](../../../../src/core/promotion/types.py#L8-L13)).

Write-path записывает **candidate-status** в колонку проекции `doge_issues.status`:
- [issue_create.py:272](../../../../src/core/application/issue_create.py#L272) `status=promoted.status.value`, [:300](../../../../src/core/application/issue_create.py#L300), [:334](../../../../src/core/application/issue_create.py#L334) `status=updated.status.value` → `"promoted"`.
- (create-path [:252](../../../../src/core/application/issue_create.py#L252) корректен — берёт projection status, но другие пути нет.)

Read-path (RC-01, column-as-truth D-RC-2) **честно отдаёт колонку как есть** ([read_filters.py:234](../../../../src/core/projection/read_filters.py#L234) `out["status"]=row_status`) — без канонизации. То есть RC-01 не создал баг, а **сделал видимым** уже записанное неверное значение. RC-04 затем удалил `payload_json` — отката нет.

## 3. Недоработали в чём? (ответ на вопрос)

**И то, и другое — но в разной пропорции. Главное — не хватило материала исходной стори; вторично — одна стори (RC-03) сделана недостаточно строго.**

### 3.1 Главное: пакет построен на неполном корневом анализе (не хватило материала)
Отчёт Jun-19 диагностировал GAP-2 как **«status MISSING»** (read-path роняет колонку). Он **физически не мог** увидеть *значение* статуса — ведь его в ответе не было вообще. Поэтому в scope пакета попало «вернуть status», а **не** «убедиться, что значение валидно для доски». Дефект write-path + два enum'а были **невидимы источнику** → вне scope. Это не ошибка реализации стори — это **под-специфицированный вход**.

### 3.2 Вторично: несимметричная генерализация (методология)
RC-02 ввёл `canonicalize_issue_type_on_read` для ровно такого же класса проблемы — рассинхрон словаря (`improvement` lowercase vs канон). **Тот же риск был у `status`** (candidate-vocab vs board-vocab), но канонизацию на status не распространили. Сильный анализ задал бы вопрос «а у status нет такого же vocab-drift?» — ответ «есть, целых два enum'а». Это упущенная генерализация (RC-02 мог бы покрыть и status).

### 3.3 Точечно: RC-03 сделана недостаточно строго (вот это «стори не так сделана»)
Смысл RC-03 (D-RC-4) — «гарантия контракта против плохих данных». Но её контракт-тест **сидит happy-path `status="PUBLISHED"`** ([test_gw_rc_03:53,91](../../../../tests/test_gw_rc_03_contract_guarantee.py#L53)) вместо реального вывода пайплайна (`promoted`). Поэтому guard проверял «валидное → валидное» и **в принципе не мог поймать** `promoted`. Плюс legacy-аудит RC-03 пометил status «closed (RC-01)», проверив **наличие** поля, а не **валидность значения**. Если бы RC-03 сидила реальный/adversarial статус или брала вывод промоушна — дефект всплыл бы сразу.

### 3.4 Архитектурный усилитель (не причина, но усугубил)
D-RC-2 (column-as-truth) корректна, но делает read настолько хорошим, насколько валидна колонка. Пакет починил read и не провалидировал **write-path vocabulary**. RC-04 убрал payload_json — резерва нет. Итог: колонка стала «истиной», но никто не гарантировал, что в ней board-валидные значения.

## 4. Классификация по слою
| GAP Jun-19 | Что сделал пакет | Реальное состояние Jun-20 |
|---|---|---|
| `id` missing | RC-01 merge | ✅ closed |
| `status` **missing** | RC-01 merge | ⚠️ **reopened как `status` INVALID (`promoted`)** — другой дефект |
| `type` lowercase | RC-02 canon | ✅ closed |
| `created_at` missing | RC-01 merge | ✅ closed |

## 5. Что нужно доделать (follow-up, реализацию не предлагаю — это в investigation §Recommended fixes)
Кратко из investigation-отчёта (детали и команды — там):
- **Fix 1 (write):** писать в `doge_issues.status` projection-status (`PUBLISHED`), не candidate `promoted` ([issue_create.py:272/300/334]).
- **Fix 2 (read, defense-in-depth):** `canonicalize_status_on_read` (`promoted`→`PUBLISHED`) по образцу RC-02 для type.
- **Fix 3 (data):** `UPDATE doge_issues SET status='PUBLISHED' WHERE status='promoted'` на hosted + reproject пустых `title_json`.
- **Fix 4 (gate):** контракт-тест `assert status in {NEW,IN_REVIEW,PUBLISHED}` на **реальных** данных пайплайна (не happy-seed).

**Рекомендация:** оформить отдельной стори (напр. `STORY-GW-RC-05-status-vocabulary-canonicalization`) в этом пакете — это прямое продолжение RC-01..04 и закрывает reopened GAP-2.

## 6. Урок методологии (чтобы не повторять)
1. Когда чиним «поле отсутствует» — сразу проверять **и значение** (presence ≠ validity).
2. Найдя vocab-mismatch в одном поле (type), **проверять симметрию** на всех родственных полях (status, labels…).
3. Контракт-/guard-тесты сидить **реальным/adversarial** выводом пайплайна, а не happy-path значением — иначе guard вакуумный.
