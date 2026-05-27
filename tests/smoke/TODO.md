Reproduce in smoke this request, launch it via localhost (run it yourself) and debug what's happening
produce detailed report

## Request
POST https://dogestonia-tallinn.up.railway.app/intake/stories — сначала заменить на localhost (который ты сам запускаешь, тут мануал doge-complaints-gateway/docs/runtime-docs/server-env-quickstart.md), после отладки уже сообщаешь, делаешь коммит, я пушу и пишешь мне как вызвать этот наш отладочный smoke тест (новый к тем что есть) чтоыб я сама проверила и потом уже сделаю интеграционно вызов напрямую из GPT
да, если вызов не правильный и не соответствует нашей документации (doge-complaints-gateway/docs/runtime-docs/api-reference) то сразу аларм и описываешь подробно все косяки в отдельной анализ доке в GPT зоне (GPT UI/docs/analysis), так как это там нужно будет править, я взяла этот вызов напрямую из GPT генерации

Authorization: Bearer <GATEWAY_API_TOKEN from env.test>
Content-Type: application/json
Accept: application/json

Body
{
  "schema_version": "m2.story_intake_envelope.v2",
  "submitter": {
    "external_user_id": "test_user_pirita_demo",
    "identity_issuer": "dogestonia.gpt.v1"
  },
  "narrative": {
    "original_text": "В прибрежной парковой зоне Pirita в Таллине, где гуляют семьи с детьми и пожилые люди, по прогулочным дорожкам регулярно ездят электровелосипеды и электросамокаты на высокой скорости. Это создаёт ощущение опасности и постоянного стресса: пешеходам приходится уворачиваться, дети могут внезапно выбежать на дорожку, а пожилым людям сложно быстро реагировать. Нужны понятные ограничения скорости, разделение потоков или контроль в этой зоне, чтобы парк у моря оставался безопасным местом для прогулок.",
    "language": "ru",
    "session_language": "ru",
    "title": {
      "et": "Kiired elektrirattad ja tõukerattad Pirita mereäärses pargialas",
      "ru": "Быстрые электровелосипеды и самокаты в парковой зоне Pirita у моря",
      "en": "Fast e-bikes and scooters in Pirita seaside park area"
    },
    "description": {
      "et": "Tallinnas Pirita mereäärses pargialas sõidavad elektrirattad ja elektritõukerattad jalutusteedel sageli suure kiirusega. Samas liiguvad seal pered lastega ja eakad inimesed. See tekitab praktilise ohu ja pideva stressi: jalakäijad peavad kõrvale põikama, lapsed võivad ootamatult rajale joosta ning eakatel on raske kiiresti reageerida. Soovitud olukord on selgem kiiruspiirang, liikumisvoogude eraldamine või nähtav kontroll, et mereäärne park jääks turvaliseks jalutuskohaks.",
      "ru": "В прибрежной парковой зоне Pirita в Таллине, где гуляют семьи с детьми и пожилые люди, по прогулочным дорожкам регулярно ездят электровелосипеды и электросамокаты на высокой скорости. Это создаёт ощущение опасности и постоянного стресса: пешеходам приходится уворачиваться, дети могут внезапно выбежать на дорожку, а пожилым людям сложно быстро реагировать. Нужны понятные ограничения скорости, разделение потоков или контроль в этой зоне, чтобы парк у моря оставался безопасным местом для прогулок.",
      "en": "In the seaside park area of Pirita in Tallinn, e-bikes and e-scooters often move at high speed along walking paths. Families with children and older people also walk there. This creates practical danger and constant stress: pedestrians have to dodge, children may suddenly run onto the path, and older people may not be able to react quickly. The desired state is clearer speed limits, separated flows, or visible control so that the seaside park remains a safe place for walking."
    },
    "summary": {
      "et": "Pirita mereäärsetel jalutusteedel liiguvad elektrirattad ja tõukerattad liiga kiiresti, tekitades ohtu lastele, eakatele ja jalakäijatele.",
      "ru": "На прогулочных дорожках Pirita у моря электровелосипеды и самокаты едут слишком быстро, создавая риск для детей, пожилых людей и пешеходов.",
      "en": "On Pirita seaside walking paths, e-bikes and scooters move too fast, creating risk for children, older people, and pedestrians."
    },
    "location_query": "Pirita seaside park area, Tallinn",
    "canonical_type": "complaint",
    "canonical_labels": [
      "public_space",
      "transport",
      "safety",
      "unsafe_condition",
      "recurring_issue",
      "city_for_people"
    ]
  },
  "origin": {
    "source": "chatgpt_demo",
    "conversation_id": "demo_pirita_e_scooters",
    "tool_call_id": "manual_story_intake_test_retry_correct_actions_config"
  },
  "privacy": {
    "contains_pii": false,
    "redaction_requested": false
  },
  "gpt_signals": {
    "severity": "HIGH",
    "impact_estimation": "DISTRICT",
    "problem_status": "RECURRING"
  }
}

## Run

```bash
# Terminal 1 (из doge-complaints-gateway/, см. server-env-quickstart.md):
APP_PROFILE=demo DB_BACKEND=in_memory CLUSTER_CRON_ENABLED=false \
  python3 -m uvicorn --app-dir src core.api.asgi_app:app --host 127.0.0.1 --port 8000

# Terminal 2:
cd doge-complaints-gateway
export LOCAL_SERVER_URL=http://127.0.0.1:8000
# токен из .env.test (GATEWAY_API_TOKEN или SERVICE_API_TOKEN)
python3 -m pytest -q tests/smoke/test_gpt_pirita_demo_intake_smoke.py -v
```

Статическая проверка контракта (без сервера):

```bash
cd doge-complaints-gateway
python3 -m pytest -q tests/smoke/test_gpt_pirita_demo_intake_smoke.py::test_gpt_pirita_payload_static_contract_check -v
```