# Solution Architecture — STORY-M2-03-04

- Validation logic вынесена в `core.profile.validation`.
- `SignalProfileService.validate_quality` предоставляет use-case API.
- Consistency tests покрывают pass/fail сценарии качества.
