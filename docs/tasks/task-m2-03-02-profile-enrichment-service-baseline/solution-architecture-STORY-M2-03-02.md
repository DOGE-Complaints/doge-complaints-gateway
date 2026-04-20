# Solution Architecture — STORY-M2-03-02

- `core.profile.enrichment` реализует narrative-to-signals inference.
- `SignalProfileService.create_or_update_profile` создает profile snapshot.
- Service интегрирован в DI factory.
