# Solution Architecture — STORY-M2-02-01

## Design

- `core.intake.contracts`:
  - request dataclasses: `Submitter`, `Narrative`, `StoryIntakeRequest`;
  - response dataclass: `StoryIntakeResponse`;
  - parsing API: `parse_story_intake_request(payload)`;
  - response builder: `build_story_intake_response(...)`.

## Validation Policy

- required:
  - `schema_version`;
  - `submitter.external_user_id`;
  - `narrative.original_text`;
- optional:
  - `submitter.identity_issuer`;
  - `narrative.language`, `narrative.title_hint`.

## Error Strategy

- Ошибки валидации: `IntakeValidationError`.
- Ошибки совместимы с общим error envelope слоем.
