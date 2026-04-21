# Cross-check and quality gates

## Контекст и управленческий вопрос

Этот документ нужен как контрольная точка качества документации:  
**какие утверждения считаются доказанными, где источник правды, и как предотвращать повторное смешение as-is и target.**

## Source-of-truth map

- Architecture/layers: `architecture-and-layers-as-is.md`
- Security/env/access: `security-env-api-access.md`
- Arweave/on-chain status: `arweave-status-and-runbook.md`
- Test strategy and coverage: `test-matrix-by-type-layer-mocks.md`
- Database state/roadmap: `database-state-and-integration-roadmap.md`
- Ops deploy/env/keys: `operations-playbook.md`
- Evidence registry: `appendix/evidence-trace-map-ru.md`
- API standard reference:
  - `api-reference/openapi.yaml`
  - `api-reference/API_REFERENCE.md`

## analysis.mdc quality gates

### Gate 1: Claim provenance

Для каждого нетривиального claim в runtime docs должна быть проверяемая ссылка:

- на runtime code (`src/core/**`),
- или на test evidence (`tests/**`),
- или на delivery/contract doc с явной пометкой, что это не runtime implementation.

Проверочный артефакт: `appendix/evidence-trace-map-ru.md`.

### Gate 2: As-is vs planned separation

Во всех профильных документах обязательны отдельные блоки:

1. `Current state (implemented now)`
2. `Planned target`
3. `Gaps / risks`

Если разделов нет или они смешаны, документ считается не прошедшим quality gate.

### Gate 3: No false implementation claims

Явно подтверждено, что в текущем runtime отсутствуют:

- real Arweave/on-chain execution,
- real DB integration/migrations/DDL,
- transport-level e2e HTTP runtime tests.

### Gate 4: Roadmap traceability

Каждый roadmap-пункт должен иметь:

- target location (какой файл/слой меняется),
- expected verification (какой тест/чек это подтверждает).

## Fast audit checklist (перед публикацией изменений docs)

1. Проверить, что новые тексты не добавляют недоказанные технологии/модули.
2. Проверить консистентность терминов между всеми runtime-docs файлами.
3. Сверить API docs (`openapi.yaml` и `API_REFERENCE.md`) друг с другом.
4. Сверить runtime docs с `appendix/evidence-trace-map-ru.md`.
5. Перечитать разделы рисков — не должны маскировать текущие ограничения.

## Final consistency notes

- Пакет синхронизирован с non post-demo runtime baseline.
- Для любых следующих изменений порядок обновления:
  1. профильный runtime document,
  2. evidence trace map,
  3. этот cross-check файл.
