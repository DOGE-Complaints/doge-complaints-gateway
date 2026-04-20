# 10. Functional Requirements: системная спецификация

## Группы FR (из FR-M2-001 ... FR-M2-070)

### A. Role & Boundaries (001-005)
- модуль — operational source of truth до external integration;
- GPT — источник narrative, но не финальной управленческой истины;
- внутренний слой отделён от витринного.

### B. Story Intake (006-011)
- каждая история сохраняется отдельно;
- no forced collapse в существующий issue;
- поддержка неполных/частичных stories и readiness-состояний.

### C. Story Profile (012-018)
- профиль содержит ключевые смысловые оси;
- user statement и system interpretation разделены;
- PII не обязателен по умолчанию.

### D. Story Store (019-023)
- story store — primary asset, не кэш;
- поддержка аналитики/кластеризации/evidence;
- обязательная lineage-связь с origin intake.

### E. Dynamic Clusters (024-033)
- multi-lens и multi-scale кластеризация;
- множественная принадлежность истории;
- отделение analytics cluster от issue-ready.

### F. Distinct Issue Formation (034-042)
- явный статус issue-candidate;
- gate по связности и зрелости;
- поддержка split/merge сценариев.

### G. SPA Projection (043-051)
- строгая контрактная совместимость с текущим UI;
- словари status/type/labels под governance;
- i18n и fallback правила обязательны.

### H. Evidence & Tokenization Prep (052-057)
- evidence pack отдельно от public issue card;
- связность issue-cluster-story обязательна;
- поддержка snapshot readiness для будущего Web3.

### I. Multilingual & Readability (058-061)
- original narrative сохраняется;
- витринная локализация не обесчеловечивает смысл;
- тексты пригодны и для dashboard, и для дальнейшей гос-упаковки.

### J. Reviewability & Human Control (062-065)
- объяснимость кластеризации и issue-проекции;
- поддержка split/merge/reframe;
- возможность отложенной промоции.

### K. Privacy & Data Minimization (066-070)
- PII-min by default;
- публичный issue — производный, не полный дамп story-layer;
- доказательность без избыточной деанонимизации.

## Delivery recommendation
- Реализовывать FR по волнам: `A+B+C` -> `D+E` -> `F+G` -> `H+I+J+K`.
