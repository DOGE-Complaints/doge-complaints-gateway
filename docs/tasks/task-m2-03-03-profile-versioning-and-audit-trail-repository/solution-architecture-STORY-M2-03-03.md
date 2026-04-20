# Solution Architecture — STORY-M2-03-03

- `InMemorySignalProfileRepository` хранит history по `story_id`.
- `SignalProfileService` использует `latest.version + 1` при обновлении.
- Audit tests проверяют порядок и полноту истории.
