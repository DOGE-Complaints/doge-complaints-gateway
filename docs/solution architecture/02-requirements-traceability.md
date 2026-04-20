# 02. Traceability: Requirements -> Architecture

## Coverage matrix

| FR Group | Архитектурный модуль |
|---|---|
| A Role & Boundaries | `01`, `03`, `04` |
| B Story Intake | `05`, `10` |
| C Story Profile | `06`, `10` |
| D Story Store | `05`, `10` |
| E Dynamic Clusters | `06`, `10` |
| F Distinct Issue | `07`, `10` |
| G SPA Projection | `07`, `04` |
| H Evidence Pack | `08`, `10`, `12` |
| I Multilingual | `07`, `11` |
| J Reviewability | `06`, `07`, `08` |
| K Privacy | `11`, `10` |
| L Post-demo automation (scheduled jobs) | `16`, `10`, `11` |
| M Post-demo story tokenization & notifications | `03`, `08`, `12`, `17` (+ продуктовый дисклеймер `requirements/21-*.md`) |

## Coverage notes
- FR-M2-043..051 (SPA) закрываются projection policy и contract tests.
- FR-M2-052..057 (evidence) закрываются отдельным evidence layer, не встроенным в issue card.
- FR-M2-066..070 (privacy) закрываются data-tier separation и policy-based redaction.

## Explicit non-coverage in demo
- blockchain broadcast и реальная wallet подпись; вместо этого — адаптеры и stub flow (`12`).
- production scheduled-job runtime; зафиксированы только архитектурные принципы (`16`) и post-demo требования `docs/requirements/20-*.md`, `21-*.md`.
