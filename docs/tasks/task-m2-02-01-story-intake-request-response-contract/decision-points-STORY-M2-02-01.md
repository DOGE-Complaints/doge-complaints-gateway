# Decision Points — STORY-M2-02-01

## DP-01: Версия контракта
- Решение: request `m2.story_intake_envelope.v1`, response `m2.story_intake_response.v1`.
- Причина: разделяем версии входа и выхода для безопасной эволюции.

## DP-02: submitter id format
- Решение: `submitter.external_user_id` принимается как opaque string без строгой схемы.
- Причина: соответствует требованиям SSOT и OAuth/IdP вариативности.

## DP-03: Форма response
- Решение: response через `SuccessEnvelope` c `trace_id` + `data` payload.
- Причина: единообразие с boundary-контрактом, реализованным в M2-01-04.
